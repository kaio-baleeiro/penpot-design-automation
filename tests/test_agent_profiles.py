from __future__ import annotations

from pathlib import Path
import unittest

from scripts.validate_agent_profiles import validate


class AgentProfileTests(unittest.TestCase):
    def test_manifested_profiles_are_portable_and_luna_bound(self) -> None:
        root = Path(__file__).resolve().parents[1]
        self.assertEqual(validate(root), [])

    def test_every_profile_has_a_mission_and_stop_rules(self) -> None:
        root = Path(__file__).resolve().parents[1]
        for prompt in sorted((root / "agents/profiles").glob("*/AGENT.md")):
            text = prompt.read_text(encoding="utf-8")
            with self.subTest(profile=prompt.parent.name):
                self.assertIn("description:", text)
                self.assertIn("# Missão", text)
                self.assertTrue("Gate" in text or "Gates" in text)


if __name__ == "__main__":
    unittest.main()
