from __future__ import annotations

import unittest

from scripts.penpot_validation.structure import validate_structure_inventory
from scripts.penpot_validation.validator import (
    derive_next_state,
    validate_manifest,
    validate_transition,
)


def _manifest(**overrides):
    value = {
        "schema_version": "1.0",
        "route": "reproduction",
        "state": "VALIDATING",
        "worker_model": "gpt-5.6-luna",
        "source_refs": ["source.png"],
        "target_viewports": [{"width": 80, "height": 60}],
        "screens": [{"id": "home", "viewport": {"width": 80, "height": 60}, "source": "source.png", "penpot_export": "export.png"}],
        "validation_cycle": 0,
        "max_validation_cycles": 3,
        "user_review_round": 0,
        "lesson_refs": [],
        "approvals": {"version": False, "design_system": False},
        "evidence": {"initial_questions": ["answered"], "addendum_question": "não", "ambiguity_analysis": "complete"},
    }
    value.update(overrides)
    return value


class WorkflowGateTests(unittest.TestCase):
    def test_schema_and_worker_are_strict(self):
        validate_manifest(_manifest())
        with self.assertRaisesRegex(ValueError, "worker_model"):
            validate_manifest(_manifest(worker_model="gpt-5.6-sol"))
        with self.assertRaisesRegex(ValueError, "lesson_refs"):
            validate_manifest(_manifest(lesson_refs="not-a-list"))

    def test_fixture_persists_terminal_state_and_lessons(self):
        import json
        from pathlib import Path

        root = Path(__file__).resolve().parents[1]
        manifest = json.loads((root / "runs/katiauinvest-e2e/manifest.json").read_text(encoding="utf-8"))
        delivery = json.loads((root / "runs/katiauinvest-e2e/delivery/manifest.json").read_text(encoding="utf-8"))
        cycle = json.loads((root / "runs/katiauinvest-e2e/cycles/cycle-3/score.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["state"], "NEEDS_REVIEW")
        self.assertEqual(manifest["state"], delivery["state"])
        self.assertEqual(manifest["state"], cycle["next_state"])
        self.assertEqual(manifest["validation_cycle"], 3)
        self.assertTrue(manifest["lesson_refs"])

    def test_validation_state_and_transition(self):
        self.assertTrue(validate_transition("VALIDATING", "REFINEMENT"))
        with self.assertRaises(ValueError):
            validate_transition("BUILDING", "DELIVERED")

    def test_cycle_and_approval_derive_next_state(self):
        result = {"cycle": 1, "passed": False}
        self.assertEqual(derive_next_state(_manifest(), result), "REFINEMENT")
        approved = _manifest(state="DS_REVALIDATING", approvals={"user": True, "design_system": True})
        structural = {"passed": True}
        self.assertEqual(derive_next_state(approved, {"cycle": 1, "passed": True}, structural), "READY_FOR_DELIVERY")
        self.assertEqual(derive_next_state(_manifest(), {"cycle": 3, "passed": False}), "NEEDS_REVIEW")

    def test_structural_gate_blocks_missing_and_detached_instances(self):
        inventory = {
            "tokens": ["color.primary"],
            "components": ["Button"],
            "component_instances": ["Button/home"],
            "detached_instances": [],
            "styles": ["body"],
            "required_component_instances": ["Button/home"],
        }
        self.assertTrue(validate_structure_inventory(inventory, {"required_tokens": ["color.primary"], "required_components": ["Button"]})["passed"])
        inventory["detached_instances"] = ["Button/home"]
        gate = validate_structure_inventory(inventory, {"required_tokens": ["color.primary"], "required_components": ["Button"]})
        self.assertFalse(gate["passed"])
        self.assertIn("detached instances present: 1", gate["errors"])

    def test_ds_gate_rejects_an_empty_inventory(self):
        inventory = {
            "tokens": [], "components": [], "component_instances": [],
            "detached_instances": [], "styles": [], "required_component_instances": [],
        }
        gate = validate_structure_inventory(inventory, _manifest(state="DS_REVALIDATING"))
        self.assertFalse(gate["passed"])
        self.assertIn("design-system inventory has no tokens", gate["errors"])

    def test_regular_validation_cannot_skip_design_system(self):
        manifest = _manifest(approvals={"user": True, "design_system": True})
        self.assertEqual(
            derive_next_state(manifest, {"cycle": 1, "passed": True}, {"passed": True}),
            "READY_FOR_USER_REVIEW",
        )


if __name__ == "__main__":
    unittest.main()
