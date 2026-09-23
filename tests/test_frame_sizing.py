from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

from scripts.penpot_validation.frame import derive_frame_spec


def _capture(
    width: int = 1440,
    height: int = 900,
    *,
    document_width: int = 1440,
    document_height: int = 900,
    stable: bool = True,
    page_horizontal: bool = False,
    containers: list[dict] | None = None,
) -> dict:
    return {
        "viewport": {"width": width, "height": height},
        "document_metrics": {
            "viewport": {"width": width, "height": height},
            "document": {"width": document_width, "height": document_height},
            "stable_after_wait": stable,
            "page_overflow": {"horizontal": page_horizontal, "vertical": document_height > height},
            "scroll_containers": containers or [],
        },
    }


class FrameSizingTests(unittest.TestCase):
    def test_frame_policy_separates_dimension_stability_from_asset_readiness(self):
        root = Path(__file__).resolve().parents[1]
        skill = (root / "skills/penpot-source-map/SKILL.md").read_text(encoding="utf-8")
        policy = (root / "skills/penpot-source-map/references/frame-sizing.md").read_text(encoding="utf-8")
        self.assertIn("Dimensional stability alone is insufficient", skill)
        self.assertIn("stable_after_wait` mede apenas a estabilidade", policy)
        self.assertIn("lazy", policy)

    def test_skill_wrapper_writes_a_frame_spec_outside_repository_cwd(self):
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            capture_path = directory / "capture.json"
            output_path = directory / "frame.json"
            capture_path.write_text(json.dumps(_capture(document_height=2200)), encoding="utf-8")
            wrapper = Path(__file__).resolve().parents[1] / "skills/penpot-source-map/scripts/source-map.sh"
            session_path = directory / "session.json"
            session_path.write_text('{"mode":"design","state":"DESIGN_SELECTED"}', encoding="utf-8")
            environment = os.environ.copy()
            environment["PENPOT_WORKFLOW_SESSION"] = str(session_path)
            result = subprocess.run(
                [
                    str(wrapper), "frame-spec", "--capture", str(capture_path),
                    "--screen-id", "home", "--output", str(output_path),
                ],
                cwd="/",
                env=environment,
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(output_path.read_text(encoding="utf-8"))["frame"]["height"], 2200)

    def test_finite_long_page_grows_only_vertically(self):
        spec = derive_frame_spec(_capture(document_height=2200), screen_id="long-page")
        self.assertEqual(spec["frame"], {"width": 1440, "height": 2200})
        self.assertEqual(spec["vertical_policy"], "finite_document")
        self.assertEqual(spec["horizontal_policy"], "viewport_bounded")
        self.assertEqual(spec["capture_mode"], "full_page")
        self.assertTrue(spec["build_ready"])

    def test_intentional_page_horizontal_requires_evidence_and_grows_width(self):
        capture = _capture(document_width=2200, page_horizontal=True)
        with self.assertRaisesRegex(ValueError, "requires evidence"):
            derive_frame_spec(capture, screen_id="timeline", horizontal_policy="intentional_page")
        spec = derive_frame_spec(
            capture,
            screen_id="timeline",
            horizontal_policy="intentional_page",
            horizontal_evidence=["DOM/code identifies a horizontally navigable timeline"],
        )
        self.assertEqual(spec["frame"]["width"], 2200)
        self.assertEqual(spec["horizontal_policy"], "intentional_page")
        self.assertEqual(spec["capture_mode"], "frame_bounds")

    def test_width_alone_never_authorizes_horizontal_growth(self):
        spec = derive_frame_spec(
            _capture(document_width=1600, page_horizontal=True),
            screen_id="broken-image",
        )
        self.assertEqual(spec["frame"]["width"], 1440)
        self.assertEqual(spec["horizontal_policy"], "accidental_overflow")
        self.assertTrue(spec["requires_user_decision"])
        self.assertFalse(spec["build_ready"])

    def test_explicit_accidental_overflow_keeps_base_width(self):
        spec = derive_frame_spec(
            _capture(document_width=1600, page_horizontal=True),
            screen_id="nowrap",
            horizontal_policy="accidental_overflow",
            horizontal_evidence=["single nowrap child exceeds the root"],
        )
        self.assertEqual(spec["frame"]["width"], 1440)
        self.assertEqual(spec["horizontal_policy"], "accidental_overflow")
        self.assertTrue(spec["build_ready"])

    def test_nested_horizontal_container_does_not_widen_page_frame(self):
        spec = derive_frame_spec(
            _capture(containers=[{"client_width": 900, "scroll_width": 1800, "overflow_x": "auto"}]),
            screen_id="table",
        )
        self.assertEqual(spec["frame"]["width"], 1440)
        self.assertEqual(spec["horizontal_policy"], "container_overflow")

    def test_vertical_only_container_cannot_mask_page_horizontal_overflow(self):
        spec = derive_frame_spec(
            _capture(
                document_width=1600,
                containers=[{"client_width": 900, "scroll_width": 900, "client_height": 400, "scroll_height": 1200}],
            ),
            screen_id="broken-layout",
        )
        self.assertEqual(spec["horizontal_policy"], "accidental_overflow")
        self.assertTrue(spec["requires_user_decision"])

    def test_dynamic_growth_requires_an_approved_finite_boundary(self):
        capture = _capture(document_height=2400, stable=False)
        unresolved = derive_frame_spec(capture, screen_id="feed")
        self.assertFalse(unresolved["build_ready"])
        self.assertTrue(unresolved["requires_user_decision"])
        bounded = derive_frame_spec(capture, screen_id="feed", dynamic_boundary=3000)
        self.assertEqual(bounded["frame"]["height"], 3000)
        self.assertEqual(bounded["vertical_policy"], "dynamic_bounded")
        self.assertEqual(bounded["capture_mode"], "bounded_state")
        self.assertTrue(bounded["build_ready"])


if __name__ == "__main__":
    unittest.main()
