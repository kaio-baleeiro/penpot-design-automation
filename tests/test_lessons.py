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
            vault = Path(temp)
            (vault / "AGENTS.md").write_text("# test vault\n", encoding="utf-8")
            created = subprocess.run(
                [
                    sys.executable,
                    str(script),
                    "--vault-root",
                    str(vault),
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
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            relative = created.stdout.strip()
            lesson = vault / relative
            self.assertIn("status: active", lesson.read_text(encoding="utf-8"))
            resolved = subprocess.run(
                [
                    sys.executable,
                    str(script),
                    "--vault-root",
                    str(vault),
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
            index = lesson.parent / "README.md"
            self.assertIn("[[LL - A repeatable failure]]", index.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
