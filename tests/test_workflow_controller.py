from __future__ import annotations

from contextlib import redirect_stdout
import io
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from scripts.penpot_provision import provision
from scripts.workflow_guard import atomic_json, begin, main, new_run, require, select, transition


class WorkflowControllerTests(unittest.TestCase):
    def test_new_session_requires_a_user_choice(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = str(Path(temporary) / "session.json")
            with patch.dict(os.environ, {"PENPOT_WORKFLOW_SESSION": path}):
                begin()
                with self.assertRaisesRegex(ValueError, "ENTRYPOINT_PENDING"):
                    require("design")
                selected = select("design", "quero trabalhar nas telas")
                self.assertEqual(selected["user_answer"], "quero trabalhar nas telas")
                require("design")
                begin()
                with self.assertRaisesRegex(ValueError, "ENTRYPOINT_PENDING"):
                    require("design")

    def test_new_run_requires_image_evidence_and_creates_controller_manifest(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            session_file = str(root / "session.json")
            args = type("Args", (), {"run_dir": str(root / "runs/demo"), "route": "directed_creation",
                "runtime": "codex", "orchestrator_model": "gpt-6-sol", "worker_model": "gpt-6-luna",
                "visual_capability_verified": True,
                "visual_evidence": str(Path(__file__).resolve().parents[1] / "workflow/visual-probe.svg"),
                "visual_observation": "mint circle left of navy card with MINT ORBIT 27 text"})()
            with patch.dict(os.environ, {"PENPOT_WORKFLOW_SESSION": session_file}):
                begin(); select("design", "design")
                manifest = new_run(args)
            self.assertTrue(manifest["workflow_controller"])
            self.assertEqual(manifest["execution"]["visual_evidence"]["opened_by_worker"], True)
            self.assertTrue((root / "runs/demo/workflow/events.jsonl").is_file())

    def test_entry_prints_exact_two_route_question(self):
        result = io.StringIO()
        with redirect_stdout(result): self.assertEqual(main(["entry"]), 0)
        self.assertIn("infraestrutura do Penpot", result.getvalue())
        self.assertIn("implementação de designs", result.getvalue())

    def test_blocked_transition_restores_the_entire_previous_manifest(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            original = {"state": "INTAKE_PENDING", "updated_at": "unchanged", "custom": {"keep": True}}
            atomic_json(root / "manifest.json", original)
            with patch.dict(os.environ, {"PENPOT_WORKFLOW_SESSION": str(root / "session.json")}), \
                 patch("scripts.workflow_guard.audit", return_value=["required artifact missing"]):
                begin(); select("design", "design")
                with self.assertRaisesRegex(ValueError, "transition blocked"):
                    transition(root, "INTAKE_REVIEW")
            self.assertEqual(json.loads((root / "manifest.json").read_text(encoding="utf-8")), original)


class ProvisionTests(unittest.TestCase):
    def test_existing_account_reuses_key_and_never_prints_mcp_token(self):
        class FakeRPC:
            def __init__(self, _base): pass
            def call(self, method, params=None):
                if method == "login-with-password": return {}
                if method == "get-access-tokens": return [{"type": "mcp", "token": "super-secret-mcp-key"}]
                return {}

        with tempfile.TemporaryDirectory() as temporary:
            env_file = Path(temporary) / ".env"
            env_file.write_text("PENPOT_PUBLIC_URI=http://localhost:9001\nPENPOT_ADMIN_EMAIL=a@localhost\nPENPOT_ADMIN_PASSWORD=pwd\nPENPOT_MCP_URL=\nPENPOT_MCP_TOKEN=\n", encoding="utf-8")
            result = io.StringIO()
            with patch("scripts.penpot_provision.RPC", FakeRPC), redirect_stdout(result):
                provision(env_file, show_password=False)
            self.assertIn("PENPOT_MCP_TOKEN=super-secret-mcp-key", env_file.read_text(encoding="utf-8"))
            self.assertNotIn("super-secret-mcp-key", result.getvalue())
            self.assertEqual(env_file.stat().st_mode & 0o777, 0o600)


if __name__ == "__main__": unittest.main()
