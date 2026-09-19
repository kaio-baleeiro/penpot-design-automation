from __future__ import annotations

import hashlib
import json
from pathlib import Path
import unittest


class OfficialBenchmarkPackageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = Path(__file__).resolve().parents[1]
        cls.benchmarks = cls.root / "runs/site-benchmarks"
        cls.sites = ("apple-br", "github-kaio-baleeiro", "warframe-en")

    def test_only_canonical_package_is_present(self):
        for site in self.sites:
            with self.subTest(site=site):
                run = self.benchmarks / site
                self.assertFalse((run / "versions").exists())
                expected = {
                    "README.md", "analysis", "approvals", "cycles", "decisions.md",
                    "design", "exports", "history.json", "manifest.json", "questions.md",
                    "source",
                }
                self.assertTrue(expected.issubset({item.name for item in run.iterdir()}))

    def test_canonical_manifest_keeps_human_acceptance_separate_from_gate(self):
        for site in self.sites:
            with self.subTest(site=site):
                run = self.benchmarks / site
                manifest = json.loads((run / "manifest.json").read_text(encoding="utf-8"))
                self.assertEqual(manifest["state"], "NEEDS_REVIEW")
                self.assertEqual(manifest["validation_cycle"], 3)
                self.assertTrue(manifest["approval"]["design"])
                self.assertTrue(manifest["canonical"]["official"])
                self.assertEqual(manifest["canonical"]["version"], "v4")
                self.assertEqual(manifest["canonical"]["automated_gate"], "NEEDS_REVIEW")
                self.assertTrue((run / manifest["canonical"]["acceptance_ref"]).is_file())
                cycle = json.loads((run / "cycles/cycle-3/score.json").read_text(encoding="utf-8"))
                self.assertFalse(cycle["passed"])
                self.assertEqual(cycle["next_state"], "NEEDS_REVIEW")

    def test_source_package_and_cycle_paths_are_self_contained(self):
        for site in self.sites:
            with self.subTest(site=site):
                run = self.benchmarks / site
                manifest = json.loads((run / "manifest.json").read_text(encoding="utf-8"))
                screenshot_refs = [ref for ref in manifest["source_refs"] if ref["type"] == "screenshot"]
                self.assertEqual(len(screenshot_refs), 1)
                source_ref = screenshot_refs[0]
                source = run / source_ref["location"]
                self.assertTrue(source.is_file())
                digest = hashlib.sha256(source.read_bytes()).hexdigest()
                self.assertEqual(source_ref["sha256"], digest)
                screen = manifest["screens"][0]
                for relative in (
                    screen["source"],
                    screen["penpot_export"],
                    manifest["structure_inventory"],
                    *screen["frame_spec"]["evidence"],
                    *manifest["intake"]["evidence"],
                ):
                    self.assertTrue((run / relative).is_file(), relative)
                for cycle_number in (1, 2, 3):
                    cycle_dir = run / "cycles" / f"cycle-{cycle_number}"
                    score = json.loads((cycle_dir / "score.json").read_text(encoding="utf-8"))
                    self.assertEqual(score["cycle"], cycle_number)
                    for evaluated in score["screens"]:
                        self.assertTrue((run / evaluated["source"]).is_file())
                        self.assertTrue((run / evaluated["penpot_export"]).is_file())

    def test_public_gallery_contains_only_official_cycle_artifacts(self):
        suffixes = {
            "home-detail-board.png",
            "home-heatmap.png",
            "home-overlay.png",
            "home-side-by-side-annotated.png",
        }
        for site in self.sites:
            with self.subTest(site=site):
                gallery = self.benchmarks / site / "analysis"
                names = {item.name for item in gallery.iterdir() if item.is_file()}
                expected = {
                    f"v4-cycle-{cycle}-{suffix}"
                    for cycle in (1, 2, 3)
                    for suffix in suffixes
                }
                self.assertEqual(names, expected)


if __name__ == "__main__":
    unittest.main()
