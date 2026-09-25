from __future__ import annotations

import json
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

from scripts.penpot_validation.validator import STATE_TRANSITIONS, VALID_STATES


ROOT = Path(__file__).resolve().parents[1]


class ArchitectureTests(unittest.TestCase):
    def test_json_architecture_matches_executable_state_machine(self):
        architecture = json.loads((ROOT / "docs/architecture/penpot-workflow.json").read_text(encoding="utf-8"))
        self.assertEqual(
            {state: set(next_states) for state, next_states in architecture["state_machine"]["transitions"].items()},
            STATE_TRANSITIONS,
        )
        self.assertEqual(set(architecture["state_machine"]["states"]), VALID_STATES)
        self.assertEqual(architecture["entry"]["routes"], ["infrastructure", "design"])

    def test_visual_architecture_is_well_formed_svg(self):
        svg = ET.parse(ROOT / "docs/architecture/penpot-workflow-architecture.svg").getroot()
        self.assertEqual(svg.tag, "{http://www.w3.org/2000/svg}svg")
        self.assertEqual(svg.attrib["viewBox"], "0 0 1900 1540")


if __name__ == "__main__":
    unittest.main()
