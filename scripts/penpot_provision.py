#!/usr/bin/env python3
"""Create/reuse local Penpot automation account and MCP token."""
from __future__ import annotations

import argparse
from http.cookiejar import CookieJar
import json
import os
from pathlib import Path
import re
import tempfile
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import HTTPCookieProcessor, Request, build_opener


class ProvisionError(RuntimeError):
    pass


def parse_env(path: Path) -> dict[str, str]:
    result = {}
    for row in path.read_text(encoding="utf-8").splitlines():
        row = row.strip()
        if row and not row.startswith("#") and "=" in row:
            k, v = row.split("=", 1); result[k.strip()] = v.strip().strip("\"'")
    return result


def update_env(path: Path, values: dict[str, str]) -> None:
    content = path.read_text(encoding="utf-8")
    for key, value in values.items():
        if "\n" in value or "\r" in value: raise ProvisionError(f"invalid value for {key}")
        pattern = re.compile(rf"(?m)^{re.escape(key)}=.*$")
        content = pattern.sub(f"{key}={value}", content) if pattern.search(content) else content.rstrip() + f"\n{key}={value}\n"
    fd, temp = tempfile.mkstemp(dir=path.parent, prefix=".env.")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as stream: stream.write(content)
        os.chmod(temp, 0o600); os.replace(temp, path)
    finally:
        if os.path.exists(temp): os.unlink(temp)


class RPC:
    def __init__(self, base: str):
        self.base = base.rstrip("/"); self.opener = build_opener(HTTPCookieProcessor(CookieJar()))

    def call(self, method: str, params: dict | None = None):
        params = params or {}
        is_get = method.startswith("get-")
        prefixes = ("api/main/methods", "api/rpc/command")
        for prefix in prefixes:
            url = f"{self.base}/{prefix}/{method}"
            req = Request(url, data=None if is_get else json.dumps(params).encode(), method="GET" if is_get else "POST",
                          headers={"Content-Type": "application/json", "Accept": "application/json"})
            try:
                with self.opener.open(req, timeout=30) as response: return json.loads(response.read() or b"null")
            except HTTPError as error:
                if error.code == 404: continue
                raise ProvisionError(f"Penpot request {method} failed with HTTP {error.code}") from error
            except (URLError, TimeoutError) as error:
                raise ProvisionError(f"Penpot request {method} unavailable ({type(error).__name__})") from error
        raise ProvisionError(f"Penpot RPC endpoint not found for {method}")


def unwrap(value):
    return value["result"] if isinstance(value, dict) and "result" in value and len(value) <= 2 else value


def login_or_register(rpc: RPC, email: str, password: str) -> str:
    try:
        rpc.call("login-with-password", {"email": email, "password": password}); return "existing"
    except ProvisionError:
        try:
            prepared = unwrap(rpc.call("prepare-register-profile", {"fullname": "Penpot Automation", "email": email,
                "password": password, "acceptNewsletterUpdates": False, "createWelcomeFile": False}))
            token = prepared.get("token") if isinstance(prepared, dict) else None
            if not token: raise ProvisionError("registration preparation returned no token")
            rpc.call("register-profile", {"token": token, "acceptNewsletterUpdates": False})
            # register-profile does not establish a session.
            rpc.call("login-with-password", {"email": email, "password": password})
            return "created"
        except ProvisionError as error:
            raise ProvisionError("account login/registration failed; verify PENPOT_ADMIN_EMAIL/PASSWORD and local registration settings") from error


def ensure_mcp(rpc: RPC) -> str:
    tokens = unwrap(rpc.call("get-access-tokens"))
    if isinstance(tokens, dict): tokens = tokens.get("items", tokens.get("tokens", []))
    if isinstance(tokens, list):
        for token in tokens:
            if isinstance(token, dict) and token.get("type") == "mcp" and token.get("token"):
                result = token["token"]
                rpc.call("update-profile-props", {"props": {"mcp-enabled": True}})
                return result
    token = unwrap(rpc.call("create-access-token", {"name": "Penpot workflow MCP", "type": "mcp"}))
    if not isinstance(token, dict) or not token.get("token"): raise ProvisionError("Penpot returned no MCP token")
    rpc.call("update-profile-props", {"props": {"mcp-enabled": True}})
    return token["token"]


def provision(env_path: Path, show_password: bool) -> None:
    values = parse_env(env_path)
    for key in ("PENPOT_PUBLIC_URI", "PENPOT_ADMIN_EMAIL", "PENPOT_ADMIN_PASSWORD"):
        if not values.get(key) or values[key].startswith("replace-"): raise ProvisionError(f"{key} is not configured")
    rpc = RPC(values["PENPOT_PUBLIC_URI"])
    state = login_or_register(rpc, values["PENPOT_ADMIN_EMAIL"], values["PENPOT_ADMIN_PASSWORD"])
    token = ensure_mcp(rpc)
    endpoint = values["PENPOT_PUBLIC_URI"].rstrip("/") + "/mcp/stream?userToken=" + quote(token, safe="")
    update_env(env_path, {"PENPOT_MCP_URL": endpoint, "PENPOT_MCP_TOKEN": token})
    print(f"Penpot account: {state}; email: {values['PENPOT_ADMIN_EMAIL']}")
    if show_password: print(f"Penpot password: {values['PENPOT_ADMIN_PASSWORD']}")
    print(f"MCP enabled; key and URL saved in {env_path}; key not printed.")


def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--env-file", required=True); parser.add_argument("--show-account-credentials", action="store_true")
    args = parser.parse_args()
    try: provision(Path(args.env_file).resolve(), args.show_account_credentials)
    except (ProvisionError, OSError) as error: print(f"penpot provision: {error}", file=__import__("sys").stderr); return 2
    return 0


if __name__ == "__main__": raise SystemExit(main())
