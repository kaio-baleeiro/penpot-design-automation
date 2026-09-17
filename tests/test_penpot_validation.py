from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import base64
from scripts.penpot_validation.capture import _capture_metadata, _validate_storage_state

from scripts.penpot_validation.images import draw_rect, solid, write_png
from scripts.penpot_validation.run import start_run
from scripts.penpot_validation.source_map import map_screenshot
from scripts.penpot_validation.validator import validate_run
from scripts.penpot_validation.metrics import METRIC_TABLE, METRIC_TABLE_VERSION, compare_metrics
from scripts.penpot_mcp import PenpotMCPClient, _dispatch, _image_bytes, _redact


class PenpotValidationTests(unittest.TestCase):
    def _fixture(self, directory: Path, divergent: bool = False) -> tuple[Path, Path]:
        source = draw_rect(solid(80, 60, (245, 245, 245)), 15, 12, 35, 24, (30, 120, 220))
        exported = source
        if divergent:
            exported = draw_rect(solid(80, 60, (245, 245, 245)), 43, 26, 32, 25, (220, 45, 50))
        source_path, export_path = directory / "source.png", directory / "export.png"
        write_png(source, str(source_path))
        write_png(exported, str(export_path))
        return source_path, export_path

    def _manifest(self, source: Path, exported: Path) -> dict:
        return {"run_id": "synthetic", "mode": "source", "source": {"type": "screenshot", "path": str(source)},
                "screens": [{"id": "home", "viewport": {"width": 80, "height": 60},
                              "source": str(source), "penpot_export": str(exported)}]}

    def test_identical_export_is_approved_and_explained(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            source, exported = self._fixture(directory)
            run = directory / "run"
            start_run(run, self._manifest(source, exported))
            result = validate_run(run, 1)
            self.assertTrue(result["passed"])
            self.assertEqual(result["aggregate_score"], 100.0)
            self.assertEqual(result["aggregate_coverage"], 1.0)
            self.assertEqual(result["metric_table_version"], METRIC_TABLE_VERSION)
            self.assertEqual(sum(item["weight"] for item in result["metric_table"].values()), 100)
            self.assertEqual(result["screens"][0]["issues"], [])
            self.assertTrue((run / "cycles/cycle-1/report.md").exists())
            self.assertTrue((run / "cycles/cycle-1/home-side-by-side-annotated.png").exists())
            self.assertTrue((run / "cycles/cycle-1/home-detail-board.png").exists())
            history = json.loads((run / "history.json").read_text())
            self.assertEqual([entry["cycle"] for entry in history], [1])
            with self.assertRaises(FileExistsError):
                validate_run(run, 1)

    def test_validator_rejects_prepopulated_cycle_directory(self) -> None:
        """Cycle output is evaluator-owned and must start empty."""
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            source, exported = self._fixture(directory)
            run = directory / "run"
            start_run(run, self._manifest(source, exported))
            cycle = run / "cycles/cycle-1"
            cycle.mkdir(parents=True)
            (cycle / "README.md").write_text("build handoff", encoding="utf-8")
            with self.assertRaisesRegex(FileExistsError, "cycle output already exists and is immutable"):
                validate_run(run, 1)

    def test_divergent_export_fails_with_localized_issues_and_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            source, exported = self._fixture(directory, divergent=True)
            run = directory / "run"
            start_run(run, self._manifest(source, exported))
            result = validate_run(run, 1)
            screen = result["screens"][0]
            self.assertFalse(result["passed"])
            self.assertLess(screen["score"], 90)
            issues = json.loads((run / "cycles/cycle-1/issues.json").read_text())["issues"]
            self.assertTrue(issues)
            self.assertTrue(any(issue["severity"] in {"P0", "P1"} for issue in issues))
            # At least one issue must locate the changed rectangle rather than
            # merely reporting a global failure.
            self.assertTrue(any((issue.get("bounds") or {}).get("x", -1) >= 15 for issue in issues))
            for name in ("home-heatmap.png", "home-overlay.png", "home-side-by-side-annotated.png", "report.md", "score.json"):
                self.assertTrue((run / "cycles/cycle-1" / name).exists(), name)

    def test_failed_cycle_cannot_reuse_the_same_export(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            source, exported = self._fixture(directory, divergent=True)
            run = directory / "run"
            start_run(run, self._manifest(source, exported))
            first = validate_run(run, 1)
            self.assertFalse(first["passed"])
            with self.assertRaisesRegex(ValueError, "reuses the failed prior-cycle export"):
                validate_run(run, 2)
            self.assertFalse((run / "cycles/cycle-2").exists())

    def test_run_resolves_source_and_export_paths_from_run_root(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            source, exported = self._fixture(directory)
            run = directory / "run"
            run.mkdir()
            (run / "source.png").write_bytes(source.read_bytes())
            (run / "export.png").write_bytes(exported.read_bytes())
            manifest = self._manifest(Path("source.png"), Path("export.png"))
            start_run(run, manifest)
            result = validate_run(run, 1)
            self.assertTrue(result["passed"])
            self.assertEqual(result["screens"][0]["source"], "source.png")
            self.assertEqual(result["screens"][0]["penpot_export"], "export.png")
            score = (run / "cycles/cycle-1/score.json").read_text(encoding="utf-8")
            self.assertNotIn(str(directory), score)

    def test_sparse_wrong_layout_does_not_pass_from_white_space(self) -> None:
        source = draw_rect(solid(480, 360, (255, 255, 255)), 20, 20, 180, 100, (20, 20, 20))
        source = draw_rect(source, 260, 220, 180, 100, (40, 110, 220))
        exported = draw_rect(solid(480, 360, (255, 255, 255)), 260, 20, 180, 100, (40, 110, 220))
        exported = draw_rect(exported, 20, 220, 180, 100, (20, 20, 20))
        metrics = compare_metrics(source, exported)
        self.assertLess(metrics["weighted_score"], 90)
        self.assertLess(metrics["regional"]["score"], 90)

    def test_source_map_records_viewport_bounds_and_hash(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            source, _ = self._fixture(directory)
            output = directory / "source-map.json"
            result = map_screenshot(source, output)
            self.assertEqual(result["viewport"], {"width": 80, "height": 60})
            self.assertEqual(result["content_bounds"], {"x": 15, "y": 12, "width": 35, "height": 24})
            self.assertEqual(len(result["sha256"]), 64)
            self.assertTrue(output.exists())

    def test_full_page_screenshot_keeps_observation_viewport_separate(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            image = draw_rect(solid(80, 140, (245, 245, 245)), 15, 90, 35, 24, (30, 120, 220))
            source = directory / "full-page.png"
            output = directory / "source-map.json"
            write_png(image, str(source))
            result = map_screenshot(source, output, viewport=(80, 60), capture_mode="full_page")
            self.assertEqual(result["viewport"], {"width": 80, "height": 60})
            self.assertEqual(result["screenshot_dimensions"], {"width": 80, "height": 140})
            self.assertEqual(result["capture_mode"], "full_page")
            self.assertEqual(result["anchors"][0]["bounds"], {"x": 0, "y": 0, "width": 80, "height": 60})
            self.assertEqual(result["anchors"][1]["bounds"], {"x": 0, "y": 0, "width": 80, "height": 140})

    def test_history_is_limited_to_three_cycles(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            source, exported = self._fixture(directory)
            run = directory / "run"
            start_run(run, self._manifest(source, exported))
            for cycle in (1, 2, 3):
                validate_run(run, cycle)
            history = json.loads((run / "history.json").read_text())
            self.assertEqual([entry["cycle"] for entry in history], [1, 2, 3])
            with self.assertRaises(ValueError):
                validate_run(run, 4)

    def test_strict_validation_requires_inventory_even_when_pixels_pass(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            source, exported = self._fixture(directory)
            run = directory / "strict-run"
            manifest = {
                "schema_version": "1.0",
                "run_id": "strict-inventory",
                "route": "reproduction",
                "state": "VALIDATING",
                "worker_model": "gpt-5.6-luna",
                "source_refs": ["source.png"],
                "target_viewports": [{"width": 80, "height": 60}],
                "screens": [{
                    "id": "home", "viewport": {"width": 80, "height": 60},
                    "frame_spec": {
                        "screen_id": "home", "viewport": {"width": 80, "height": 60},
                        "document": {"width": 80, "height": 60}, "frame": {"width": 80, "height": 60},
                        "vertical_policy": "viewport_bounded", "horizontal_policy": "viewport_bounded",
                        "capture_mode": "viewport", "stable": True, "build_ready": True,
                        "requires_user_decision": False, "evidence": ["capture.json"],
                    },
                    "source": str(source), "penpot_export": str(exported),
                }],
                "validation_cycle": 0, "max_validation_cycles": 3, "user_review_round": 0,
                "lesson_refs": [], "approvals": {"user": False, "design_system": False},
                "evidence": {"initial_questions": ["answered"], "addendum_question": "no", "ambiguity_analysis": "complete"},
            }
            (run / "source").mkdir(parents=True)
            (run / "source/frame-spec.json").write_text(json.dumps({"schema_version": "1.0", "screens": [manifest["screens"][0]["frame_spec"]]}), encoding="utf-8")
            start_run(run, manifest)
            result = validate_run(run, 1)
            self.assertFalse(result["passed"])
            self.assertFalse(result["structure_gate"]["passed"])
            self.assertIn("strict validation requires", result["structure_gate"]["errors"][0])

    def test_long_frame_passes_and_truncated_export_is_blocked(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            source = draw_rect(solid(80, 140, (245, 245, 245)), 15, 90, 35, 24, (30, 120, 220))
            source_path = directory / "source-long.png"
            good_export = directory / "export-long.png"
            truncated_export = directory / "export-truncated.png"
            write_png(source, str(source_path))
            write_png(source, str(good_export))
            write_png(solid(80, 60, (245, 245, 245)), str(truncated_export))
            frame_spec = {
                "screen_id": "home",
                "viewport": {"width": 80, "height": 60},
                "document": {"width": 80, "height": 140},
                "frame": {"width": 80, "height": 140},
                "vertical_policy": "finite_document",
                "horizontal_policy": "viewport_bounded",
                "capture_mode": "full_page",
                "stable": True,
                "build_ready": True,
                "requires_user_decision": False,
                "evidence": ["capture-full-page.json"],
            }
            good_manifest = self._manifest(source_path, good_export)
            good_manifest["screens"][0]["frame_spec"] = frame_spec
            good_run = directory / "good-run"
            start_run(good_run, good_manifest)
            good_result = validate_run(good_run, 1)
            self.assertTrue(good_result["passed"])
            self.assertEqual(good_result["screens"][0]["frame"], {"width": 80, "height": 140})

            bad_manifest = self._manifest(source_path, truncated_export)
            bad_manifest["screens"][0]["frame_spec"] = frame_spec
            bad_run = directory / "bad-run"
            start_run(bad_run, bad_manifest)
            bad_result = validate_run(bad_run, 1)
            self.assertFalse(bad_result["passed"])
            self.assertTrue(any(
                issue["severity"] == "P0" and "truncated" in issue["title"]
                for issue in bad_result["screens"][0]["issues"]
            ))

    def test_versioned_metric_table_has_six_weighted_dimensions(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            source, exported = self._fixture(directory)
            from scripts.penpot_validation.images import read_png
            metrics = compare_metrics(read_png(str(source)), read_png(str(exported)))
            self.assertEqual(metrics["version"], METRIC_TABLE_VERSION)
            self.assertEqual(set(metrics["metrics"]), set(METRIC_TABLE))
            self.assertEqual(sum(item["weight"] for item in metrics["metrics"].values()), 100)
            self.assertEqual(metrics["weighted_score"], 100.0)
            self.assertTrue(all(item["explanation"] for item in metrics["metrics"].values()))

    def test_mcp_parser_redacts_secrets_and_extracts_image_without_network(self) -> None:
        image_data = base64.b64encode(b"synthetic-image").decode()
        response = {"url": "http://secret.example", "token": "do-not-print", "content": [{"type": "image", "mimeType": "image/png", "data": image_data}]}
        redacted = _redact(response)
        self.assertEqual(redacted["url"], "[redacted]")
        self.assertEqual(redacted["token"], "[redacted]")
        self.assertNotIn("do-not-print", json.dumps(redacted))
        decoded, mime = _image_bytes(response)
        self.assertEqual(decoded, b"synthetic-image")
        self.assertEqual(mime, "image/png")

        class FakeClient:
            def call(self, name, arguments):
                return {"called": name, "arguments": arguments}

            def tools(self):
                return {"tools": []}

            def overview(self, arguments):
                return {"called": "overview", "arguments": arguments}

            execute = overview
            export = overview

        result, save_image = _dispatch(FakeClient(), ["call", "penpot_test", "--args", '{"screen":"home"}'])
        self.assertEqual(result["called"], "penpot_test")
        self.assertEqual(result["arguments"], {"screen": "home"})
        self.assertIsNone(save_image)

    def test_mcp_jsonrpc_transport_is_stdlib_and_does_not_print_endpoint(self) -> None:
        class FakeResponse:
            def __init__(self, payload, headers=None):
                self.payload = payload
                self.headers = headers or {}

            def __enter__(self):
                return self

            def __exit__(self, *args):
                return False

            def read(self):
                return self.payload

        responses = [
            FakeResponse(b'data: {"jsonrpc":"2.0","id":1,"result":{"protocolVersion":"2025-03-26"}}\n\n', {"mcp-session-id": "session-1"}),
            FakeResponse(b""),
            FakeResponse(b'{"jsonrpc":"2.0","id":2,"result":{"ok":true,"url":"https://internal"}}'),
        ]
        seen = []

        def fake_urlopen(request, timeout):
            seen.append(request)
            return responses.pop(0)

        with patch("scripts.penpot_mcp.urlopen", side_effect=fake_urlopen):
            client = PenpotMCPClient(endpoint="https://internal.example/mcp", token="secret")
            result = client.request("tools/list")
        self.assertTrue(result["ok"])
        self.assertEqual(result["url"], "https://internal")
        self.assertEqual(len(seen), 3)
        initialize_payload = json.loads(seen[0].data.decode("utf-8"))
        self.assertEqual(initialize_payload["method"], "initialize")
        self.assertEqual(initialize_payload["id"], 1)
        self.assertEqual(json.loads(seen[1].data.decode("utf-8"))["method"], "notifications/initialized")
        self.assertNotIn("id", json.loads(seen[1].data.decode("utf-8")))
        self.assertEqual(json.loads(seen[2].data.decode("utf-8"))["method"], "tools/list")
        self.assertEqual(seen[2].get_header("Mcp-session-id"), "session-1")
        self.assertEqual(seen[2].get_header("Authorization"), "Bearer secret")

    def test_storage_state_is_validated_and_capture_manifest_is_safe(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            missing = directory / "missing-storage-state.json"
            with self.assertRaisesRegex(ValueError, "does not exist"):
                _validate_storage_state(missing)
            invalid = directory / "invalid-storage-state.json"
            invalid.write_text("not-json", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "valid JSON"):
                _validate_storage_state(invalid)
            state = directory / "storage-state.json"
            state.write_text(json.dumps({"cookies": [{"name": "session", "value": "secret-token"}], "origins": []}), encoding="utf-8")
            self.assertEqual(_validate_storage_state(state), state)
            metadata = _capture_metadata("https://private.example", 390, 844, screenshot="source.png", dom="dom.html", styles="styles.json", http_status=200, full_page=False, authenticated=True)
            serialized = json.dumps(metadata, ensure_ascii=False)
            self.assertTrue(metadata["authenticated"])
            self.assertNotIn("storage_state", metadata)
            self.assertNotIn(str(state), serialized)
            self.assertNotIn("secret-token", serialized)


if __name__ == "__main__":
    unittest.main()
