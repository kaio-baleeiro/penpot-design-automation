"""Small persistent stdlib-only CLI client for a Penpot MCP HTTP endpoint.

The endpoint and bearer token are read from environment variables and are
never printed. Responses are recursively redacted before display. The client
uses JSON-RPC 2.0, which keeps it compatible with standard MCP HTTP bridges
without requiring a third-party SDK.
"""

from __future__ import annotations

import argparse
import base64
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import shlex
import sys
from typing import Any, Iterable
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


SENSITIVE_KEYS = {
    "token", "access_token", "refresh_token", "authorization", "cookie", "set-cookie",
    "url", "endpoint", "password", "secret", "api_key", "api-key", "client_secret",
    "client-secret", "bearer", "session", "session_id", "session-id",
}
SENSITIVE_KEY_RE = re.compile(r"(?:token|auth|cookie|password|secret|api[_-]?key|client[_-]?secret|endpoint|url|session)", re.I)
BEARER_RE = re.compile(r"(?i)\bbearer\s+[^\s,;]+")
SECRET_ASSIGNMENT_RE = re.compile(r"(?i)(\b(?:password|token|secret|api[_-]?key|client[_-]?secret)\s*[=:]\s*)([^\s,;&]+)")
DATA_URI = re.compile(r"^data:(image/[a-zA-Z0-9.+-]+);base64,(.+)$", re.DOTALL)


class MCPError(RuntimeError):
    pass


def _redact(value: Any, known_strings: Iterable[str] | None = None) -> Any:
    """Recursively redact sensitive keys, URLs and known credential strings."""
    known = tuple(secret for secret in (known_strings or ()) if isinstance(secret, str) and secret)
    if isinstance(value, dict):
        content_type = value.get("type")
        is_binary_content = isinstance(content_type, str) and content_type in {"image", "audio"}
        return {
            key: "[redacted-binary]"
            if is_binary_content and str(key).lower() in {"data", "blob"}
            else "[redacted]"
            if str(key).lower() in SENSITIVE_KEYS or SENSITIVE_KEY_RE.search(str(key))
            else _redact(item, known)
            for key, item in value.items()
        }
    if isinstance(value, list):
        return [_redact(item, known) for item in value]
    if isinstance(value, str):
        if value.startswith(("http://", "https://")):
            return "[redacted-url]"
        redacted = value
        for secret in known:
            redacted = redacted.replace(secret, "[redacted]")
        redacted = BEARER_RE.sub("Bearer [redacted]", redacted)
        redacted = SECRET_ASSIGNMENT_RE.sub(r"\1[redacted]", redacted)
        return redacted
    return value


class _AuditLogger:
    """Small append-only JSONL audit log with a credential-aware redactor."""

    def __init__(self, path: str | Path | None, known_strings: Iterable[str] = ()):
        self.path = Path(path) if path else None
        self.known_strings = {value for value in known_strings if isinstance(value, str) and value}
        if self.path:
            self.path.parent.mkdir(parents=True, exist_ok=True)

    def add_secret(self, value: str | None) -> None:
        if value:
            self.known_strings.add(value)

    def write(self, event: str, tool: str, arguments: Any = None, response: Any = None) -> None:
        if self.path is None:
            return
        record = {
            "event": event,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "tool": tool,
            "arguments": _redact(arguments, self.known_strings),
            "response": _redact(response, self.known_strings),
        }
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, ensure_ascii=False, separators=(",", ":")) + "\n")


def _image_bytes(value: Any) -> tuple[bytes, str] | None:
    if isinstance(value, dict):
        mime = str(value.get("mimeType") or value.get("mime_type") or "image/png")
        data = value.get("data")
        if isinstance(data, str):
            match = DATA_URI.match(data)
            if match:
                mime = match.group(1)
                data = match.group(2)
            try:
                if data and (mime.startswith("image/") or value.get("type") == "image"):
                    return base64.b64decode(data, validate=True), mime
            except (ValueError, base64.binascii.Error):
                pass
        for child in value.values():
            found = _image_bytes(child)
            if found:
                return found
    elif isinstance(value, list):
        for child in value:
            found = _image_bytes(child)
            if found:
                return found
    elif isinstance(value, str):
        match = DATA_URI.match(value)
        if match:
            try:
                return base64.b64decode(match.group(2), validate=True), match.group(1)
            except (ValueError, base64.binascii.Error):
                pass
    return None


def _decode_mcp_payload(raw: bytes) -> dict[str, Any]:
    """Decode either an MCP JSON response or the usual SSE data event."""
    if not raw:
        return {}
    text = raw.decode("utf-8", errors="replace").strip()
    try:
        parsed = json.loads(text)
        if isinstance(parsed, dict):
            return parsed
    except json.JSONDecodeError:
        pass
    for line in text.splitlines():
        if line.startswith("data:"):
            candidate = line[5:].lstrip()
            if not candidate:
                continue
            try:
                parsed = json.loads(candidate)
            except json.JSONDecodeError:
                continue
            if isinstance(parsed, dict):
                return parsed
    raise MCPError("MCP returned non-JSON/SSE response")


class PenpotMCPClient:
    def __init__(self, endpoint: str | None = None, token: str | None = None, timeout: float = 30.0,
                 log_path: str | Path | None = None):
        self.endpoint = endpoint or os.environ.get("PENPOT_MCP_URL")
        self.token = token if token is not None else os.environ.get("PENPOT_MCP_TOKEN")
        self.timeout = timeout
        self.request_id = 0
        self.session_id = ""
        if not self.endpoint:
            raise MCPError("PENPOT_MCP_URL não está definido")
        self.logger = _AuditLogger(log_path, (self.endpoint, self.token or ""))
        self._initialize()

    def _initialize(self) -> None:
        result, headers = self._post("initialize", {
            "protocolVersion": "2025-03-26", "capabilities": {},
            "clientInfo": {"name": "penpot-design-automation", "version": "0.1.0"},
        }, session=False)
        if not isinstance(result, dict) or "result" not in result:
            raise MCPError("MCP initialization failed")
        self.session_id = headers.get("mcp-session-id", "")
        if not self.session_id:
            raise MCPError("MCP did not provide a session id")
        self._post("notifications/initialized", None, notification=True)

    def _post(self, method: str, params: dict[str, Any] | None = None, *, session: bool = True,
              notification: bool = False) -> tuple[dict[str, Any], dict[str, str]]:
        payload: dict[str, Any] = {"jsonrpc": "2.0", "method": method}
        if not notification:
            self.request_id += 1
            payload["id"] = self.request_id
        if params is not None:
            payload["params"] = params
        headers = {"Content-Type": "application/json", "Accept": "application/json, text/event-stream"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        if session and self.session_id:
            headers["mcp-session-id"] = self.session_id
        self.logger.write("request", method, params, None)
        request = Request(self.endpoint, data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST")
        try:
            with urlopen(request, timeout=self.timeout) as response:
                raw = response.read()
                response_headers = {str(key).lower(): str(value) for key, value in response.headers.items()}
        except (HTTPError, URLError, TimeoutError) as exc:
            self.logger.write("error", method, params, {"error": f"MCP request failed: {type(exc).__name__}"})
            raise MCPError(f"MCP request failed: {type(exc).__name__}") from exc

        result = _decode_mcp_payload(raw)
        self.logger.write("response", method, params, result)
        if result.get("error"):
            raise MCPError("MCP returned an error")
        if response_headers.get("mcp-session-id"):
            self.session_id = response_headers["mcp-session-id"]
            self.logger.add_secret(self.session_id)
        return result, response_headers

    def request(self, method: str, params: dict[str, Any] | None = None) -> Any:
        result, _ = self._post(method, params)
        return result.get("result", result)

    def tools(self) -> Any:
        return self.request("tools/list")

    def call(self, name: str, arguments: dict[str, Any] | None = None) -> Any:
        return self.request("tools/call", {"name": name, "arguments": arguments or {}})

    def overview(self, arguments: dict[str, Any] | None = None) -> Any:
        return self.call("high_level_overview", arguments)

    def execute(self, arguments: dict[str, Any] | None = None) -> Any:
        return self.call("execute_code", arguments)

    def export(self, arguments: dict[str, Any] | None = None) -> Any:
        return self.call("export_shape", arguments)


def _json_arg(value: str | None) -> dict[str, Any]:
    if not value:
        return {}
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError as exc:
        raise MCPError(f"argumentos não são JSON: {exc.msg}") from exc
    if not isinstance(parsed, dict):
        raise MCPError("argumentos devem ser um objeto JSON")
    return parsed


def _print_result(result: Any, save_image: str | None = None) -> None:
    output = _redact(result)
    if save_image:
        found = _image_bytes(result)
        if not found:
            raise MCPError("nenhum conteúdo image base64 encontrado na resposta")
        data, mime = found
        suffix = {"image/jpeg": ".jpg", "image/webp": ".webp", "image/svg+xml": ".svg"}.get(mime, ".png")
        target = Path(save_image)
        if target.suffix == "":
            target = target.with_suffix(suffix)
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("xb") as handle:
            handle.write(data)
        output = {"saved_image": str(target), "mime_type": mime}
    print(json.dumps(output, ensure_ascii=False, indent=2))


def _dispatch(client: PenpotMCPClient, argv: list[str]) -> tuple[Any, str | None]:
    parser = argparse.ArgumentParser(prog="penpot_mcp.py")
    parser.add_argument("command", choices=("tools", "call", "overview", "execute", "export"))
    parser.add_argument("name", nargs="?")
    parser.add_argument("--args", default="{}")
    parser.add_argument("--save-image")
    # Parsed here as well as in main so REPL/embedded callers accept the same
    # command syntax. The client owns the logger; this option is consumed by
    # main before construction.
    parser.add_argument("--log-path")
    args = parser.parse_args(argv)
    params = _json_arg(args.args)
    if args.command == "tools":
        return client.tools(), args.save_image
    if args.command == "call":
        if not args.name:
            raise MCPError("call exige o nome da tool")
        return client.call(args.name, params), args.save_image
    return getattr(client, args.command)(params), args.save_image


def _repl(client: PenpotMCPClient) -> int:
    """Keep one client/request-id alive for a sequence of MCP commands."""
    print("penpot-mcp persistent session; use tools, call, overview, execute or export; type quit to exit")
    for line in sys.stdin:
        command = line.strip()
        if not command:
            continue
        if command.lower() in {"quit", "exit"}:
            return 0
        try:
            result, save_image = _dispatch(client, shlex.split(command))
            _print_result(result, save_image)
        except (MCPError, SystemExit) as exc:
            if isinstance(exc, SystemExit):
                print("penpot-mcp: comando inválido", file=sys.stderr)
            else:
                print(f"penpot-mcp: {exc}", file=sys.stderr)
    return 0


def main(argv: list[str] | None = None) -> int:
    if argv is None:
        argv = sys.argv[1:]
    if argv and argv[0].lower() in {"repl", "interactive"}:
        log_path = None
        if "--log-path" in argv:
            index = argv.index("--log-path")
            if index + 1 < len(argv):
                log_path = argv[index + 1]
        return _repl(PenpotMCPClient(log_path=log_path))
    log_path = None
    if "--log-path" in argv:
        index = argv.index("--log-path")
        if index + 1 >= len(argv):
            raise MCPError("--log-path exige um caminho")
        log_path = argv[index + 1]
    client = PenpotMCPClient(log_path=log_path)
    result, save_image = _dispatch(client, argv)
    _print_result(result, save_image)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except MCPError as exc:
        print(f"penpot-mcp: {exc}", file=sys.stderr)
        raise SystemExit(2)
