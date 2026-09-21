from __future__ import annotations

import os
from pathlib import Path
import subprocess
import tempfile
import unittest


class SelfContainedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = Path(__file__).resolve().parents[1]

    def test_public_entrypoints_and_skill_lessons_are_present(self):
        for relative in ("AGENTS.md", "CLAUDE.md", "GEMINI.md", "README.md", "setup.sh", "infra/penpot/.env.example"):
            self.assertTrue((self.root / relative).is_file(), relative)
        skills = sorted(path for path in (self.root / "skills").iterdir() if path.is_dir())
        self.assertEqual(len(skills), 7)
        for skill in skills:
            self.assertTrue((skill / "SKILL.md").is_file(), skill.name)
            self.assertTrue((skill / "README.md").is_file(), skill.name)
            self.assertTrue((skill / "lessons-learned/README.md").is_file(), skill.name)
            for bucket in ("project", "local"):
                self.assertTrue((skill / "lessons-learned" / bucket / "README.md").is_file())

    def test_bootstrap_creates_secrets_and_is_idempotent(self):
        script = self.root / "infra/penpot/scripts/bootstrap.sh"
        with tempfile.TemporaryDirectory() as temp:
            env_path = Path(temp) / ".env"
            env = os.environ.copy()
            env["PENPOT_ENV_FILE"] = str(env_path)
            first = subprocess.run([str(script)], env=env, capture_output=True, text=True)
            self.assertEqual(first.returncode, 0, first.stderr)
            contents = env_path.read_text(encoding="utf-8")
            self.assertNotIn("replace-with-", contents)
            self.assertIn("PENPOT_CREATE_VOLUMES=true", contents)
            self.assertEqual(env_path.stat().st_mode & 0o777, 0o600)
            second = subprocess.run([str(script)], env=env, capture_output=True, text=True)
            self.assertEqual(second.returncode, 0, second.stderr)
            self.assertEqual(contents, env_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
