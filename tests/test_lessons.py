from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path
import unittest


class LessonRecorderTests(unittest.TestCase):
    def test_lesson_requires_verification_before_mitigation(self):
        root = Path(__file__).resolve().parents[1]
        script = root / "skills/penpot-design/scripts/record-lesson.py"
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp)
            skill = project / "skills" / "penpot-validate"
            skill.mkdir(parents=True)
            (skill / "SKILL.md").write_text("---\nname: penpot-validate\n---\n", encoding="utf-8")
            created = subprocess.run(
                [
                    sys.executable,
                    str(script),
                    "--project-root",
                    str(project),
                    "--skill-dir",
                    "skills/penpot-validate",
                    "record",
                    "--title",
                    "A repeatable failure",
                    "--lesson",
                    "Turn the failure into a durable rule.",
                    "--context",
                    "A deterministic test exposed it.",
                    "--evidence",
                    "test-run/cycle-1",
                    "--future-rule",
                    "Run the guard before delivery.",
                    "--kind",
                    "project",
                    "--integration",
                    "tests/test_lessons.py",
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            relative = created.stdout.strip()
            lesson = project / relative
            self.assertIn("status: active", lesson.read_text(encoding="utf-8"))
            resolved = subprocess.run(
                [
                    sys.executable,
                    str(script),
                    "--project-root",
                    str(project),
                    "--skill-dir",
                    "skills/penpot-validate",
                    "resolve",
                    "--lesson",
                    lesson.name,
                    "--countermeasure",
                    "Added a deterministic guard.",
                    "--verification",
                    "The original failing case now passes.",
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertEqual(resolved.stdout.strip(), relative)
            text = lesson.read_text(encoding="utf-8")
            self.assertIn("status: mitigated", text)
            self.assertIn("## Resolution", text)
            self.assertIn("kind: project", text)
            self.assertIn("integration: tests/test_lessons.py", text)
            index = lesson.parent / "README.md"
            self.assertIn("[LL - A repeatable failure]", index.read_text(encoding="utf-8"))

    def test_recorder_rejects_a_path_outside_the_skills_directory(self):
        root = Path(__file__).resolve().parents[1]
        script = root / "skills/penpot-design/scripts/record-lesson.py"
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp)
            (project / "skills" / "penpot-design").mkdir(parents=True)
            (project / "skills" / "penpot-design" / "SKILL.md").write_text(
                "---\nname: penpot-design\n---\n", encoding="utf-8"
            )
            result = subprocess.run(
                [
                    sys.executable,
                    str(script),
                    "--project-root",
                    str(project),
                    "--skill-dir",
                    "../outside",
                    "record",
                    "--title",
                    "Invalid",
                    "--lesson",
                    "x",
                    "--context",
                    "x",
                    "--evidence",
                    "x",
                    "--future-rule",
                    "x",
                    "--kind",
                    "machine",
                ],
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("pasta de skill válida", result.stderr)

    def test_project_lesson_requires_an_integration_target(self):
        root = Path(__file__).resolve().parents[1]
        script = root / "skills/penpot-design/scripts/record-lesson.py"
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp)
            skill = project / "skills" / "penpot-design"
            skill.mkdir(parents=True)
            (skill / "SKILL.md").write_text("---\nname: penpot-design\n---\n", encoding="utf-8")
            result = subprocess.run(
                [
                    sys.executable,
                    str(script),
                    "--project-root",
                    str(project),
                    "record",
                    "--title",
                    "Missing integration",
                    "--lesson",
                    "x",
                    "--context",
                    "x",
                    "--evidence",
                    "x",
                    "--future-rule",
                    "x",
                    "--kind",
                    "project",
                ],
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("exigem --integration", result.stderr)


if __name__ == "__main__":
    unittest.main()
