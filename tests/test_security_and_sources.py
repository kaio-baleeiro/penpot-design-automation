from __future__ import annotations

import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from scripts.penpot_mcp import PenpotMCPClient, _AuditLogger, _redact
from scripts.penpot_validation.capture import _capture_metadata, sanitize_url
from scripts.penpot_validation.images import solid, write_png
from scripts.penpot_validation.source_map import compile_source_map, map_screenshot, sanitize_location


class SecurityAndSourceMapTests(unittest.TestCase):
    def test_capture_metadata_keeps_only_safe_url_and_integral_hash(self) -> None:
        original = "https://alice:password@example.test/app?token=do-not-store#private"
        metadata = _capture_metadata(original, 10, 20, screenshot="source.png", dom="dom.html",
                                     styles="styles.json", http_status=200, full_page=False, authenticated=False)
        self.assertEqual(metadata["url"], "https://example.test/app")
        self.assertEqual(metadata["url_sha256"], hashlib.sha256(original.encode()).hexdigest())
        self.assertNotIn("alice", json.dumps(metadata))
        self.assertNotIn("password", json.dumps(metadata))
        self.assertNotIn("token=", json.dumps(metadata))

    def test_url_and_location_sanitizers_remove_userinfo_query_and_fragment(self) -> None:
        self.assertEqual(sanitize_url("HTTP://u:p@Example.test:8080/a?x=1#frag"), "http://example.test:8080/a")
        self.assertEqual(sanitize_location("https://u:p@example.test/a?secret=1#frag"), "https://example.test/a")

    def test_recursive_redaction_covers_known_strings_and_secret_patterns(self) -> None:
        payload = {"nested": [{"api_key": "key-value"}, "Bearer token-value", "password=pass-value"],
                   "message": "token-value appears here"}
        redacted = _redact(payload, {"token-value", "key-value", "pass-value"})
        serialized = json.dumps(redacted)
        self.assertNotIn("token-value", serialized)
        self.assertNotIn("key-value", serialized)
        self.assertNotIn("pass-value", serialized)
        self.assertEqual(redacted["nested"][0]["api_key"], "[redacted]")

    def test_mcp_jsonl_logging_is_append_only_and_does_not_emit_credentials(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "audit.jsonl"
            logger = _AuditLogger(path, ["https://internal.test/mcp", "bearer-secret"])
            logger.write("request", "tools/call", {"authorization": "bearer-secret", "url": "https://internal.test/mcp"}, None)
            logger.write("response", "tools/call", {"screen": "home"}, {"secret": "bearer-secret", "ok": True})
            lines = path.read_text(encoding="utf-8").splitlines()
            self.assertEqual(len(lines), 2)
            records = [json.loads(line) for line in lines]
            self.assertEqual([record["event"] for record in records], ["request", "response"])
            self.assertEqual(records[0]["arguments"]["authorization"], "[redacted]")
            self.assertNotIn("internal.test", path.read_text(encoding="utf-8"))
            self.assertNotIn("bearer-secret", path.read_text(encoding="utf-8"))

    def test_aliases_use_real_penpot_tool_names(self) -> None:
        class FakeClient:
            def __init__(self):
                self.calls = []

            def call(self, name, arguments):
                self.calls.append((name, arguments))
                return {"tool": name}

        client = FakeClient()
        self.assertEqual(PenpotMCPClient.overview(client, {})["tool"], "high_level_overview")
        self.assertEqual(PenpotMCPClient.execute(client, {"code": "2"})["tool"], "execute_code")
        self.assertEqual(PenpotMCPClient.export(client, {"shape_id": "shape"})["tool"], "export_shape")
        self.assertEqual([call[0] for call in client.calls], ["high_level_overview", "execute_code", "export_shape"])

    def test_redaction_removes_inline_image_payloads(self) -> None:
        redacted = _redact({"content": [{"type": "image", "mimeType": "image/png", "data": "sensitive-base64"}]})
        self.assertEqual(redacted["content"][0]["data"], "[redacted-binary]")
        schema = {"type": {"kind": "object"}, "properties": {}}
        self.assertEqual(_redact(schema), schema)

    def test_source_map_has_stable_ids_safe_locations_and_relationships(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            screenshot = directory / "source.png"
            code = directory / "screen.js"
            write_png(solid(3, 2, (255, 255, 255)), str(screenshot))
            code.write_text("export const screen = {};\n", encoding="utf-8")
            result = compile_source_map(url="https://u:p@example.test/app?token=x#frag",
                                        screenshot=screenshot, code=code)
            self.assertEqual([source["kind"] for source in result["sources"]], ["url", "screenshot", "code"])
            self.assertEqual(result["sources"][0]["location"], "https://example.test/app")
            self.assertEqual(len(result["relationships"]), 2)
            self.assertTrue(all(source["source_id"].startswith("src-") for source in result["sources"]))
            self.assertTrue(all("confidence" in source and "anchors" in source for source in result["sources"]))
            serialized = json.dumps(result)
            self.assertNotIn("u:p", serialized)
            self.assertNotIn("token=x", serialized)
            self.assertNotIn(str(directory), serialized)

    def test_source_map_hashes_code_directories_without_secret_files(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            repo = directory / "app"
            repo.mkdir()
            (repo / "screen.tsx").write_text("export default function Screen() {}\n", encoding="utf-8")
            (repo / ".env.local").write_text("PASSWORD=must-not-affect-hash\n", encoding="utf-8")
            first = compile_source_map(code=repo)
            (repo / ".env.local").write_text("PASSWORD=changed\n", encoding="utf-8")
            second = compile_source_map(code=repo)
            self.assertEqual(first["sources"][0]["sha256"], second["sources"][0]["sha256"])
            self.assertEqual(first["sources"][0]["anchors"][0]["type"], "repository")

    def test_screenshot_map_does_not_persist_absolute_location(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            screenshot = directory / "source.png"
            output = directory / "map.json"
            write_png(solid(3, 2, (255, 255, 255)), str(screenshot))
            result = map_screenshot(screenshot, output)
            self.assertEqual(result["source_type"], "screenshot")
            self.assertNotIn(str(directory), json.dumps(result))
            self.assertEqual(len(result["source_id"]), len("src-screenshot-") + 24)


if __name__ == "__main__":
    unittest.main()
