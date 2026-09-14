from __future__ import annotations

import subprocess
from pathlib import Path
import unittest

from scripts.validate_skills import REQUIRED_SKILLS, validate_skill


class AgentSkillsPackageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = Path(__file__).resolve().parents[1]
        cls.skills = cls.root / "skills"

    def test_every_skill_is_a_valid_nonempty_package(self):
        for name in sorted(REQUIRED_SKILLS):
            with self.subTest(skill=name):
                self.assertEqual(validate_skill(self.skills / name), [])

    def test_every_skill_subdirectory_has_an_explanatory_readme(self):
        for name in sorted(REQUIRED_SKILLS):
            skill = self.skills / name
            self.assertTrue((skill / "README.md").is_file(), name)
            for child in skill.iterdir():
                if child.is_dir() and child.name != "__pycache__":
                    with self.subTest(skill=name, directory=child.name):
                        self.assertTrue((child / "README.md").is_file())

    def test_non_network_wrappers_resolve_the_project_runtime(self):
        scripts = [
            "penpot-design/scripts/start-run.sh",
            "penpot-intake/scripts/capture.sh",
            "penpot-source-map/scripts/source-map.sh",
            "penpot-validate/scripts/validate.sh",
        ]
        arguments = [["--help"], ["--help"], ["compile", "--help"], ["--help"]]
        for relative, args in zip(scripts, arguments):
            with self.subTest(script=relative):
                result = subprocess.run(
                    [str(self.skills / relative), *args],
                    cwd="/",
                    capture_output=True,
                    text=True,
                )
                self.assertEqual(result.returncode, 0, result.stderr)

    def test_delivery_checker_accepts_the_terminal_fixture(self):
        result = subprocess.run(
            [
                str(self.skills / "penpot-delivery/scripts/check-package.py"),
                str(self.root / "runs/katiauinvest-e2e"),
            ],
            cwd="/",
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
