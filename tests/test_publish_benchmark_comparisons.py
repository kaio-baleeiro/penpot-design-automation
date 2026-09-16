import json
import tempfile
import unittest
from pathlib import Path

from scripts.publish_benchmark_comparisons import ARTIFACTS, PNG_SIGNATURE, publish


class PublishBenchmarkComparisonsTests(unittest.TestCase):
    def test_publishes_three_versioned_images_without_mutating_cycle(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            run = root / "run"
            cycle = run / "cycles" / "cycle-3"
            cycle.mkdir(parents=True)
            (cycle / "score.json").write_text(json.dumps({"cycle": 3}), encoding="utf-8")
            (cycle / "issues.json").write_text(json.dumps({"cycle": 3}), encoding="utf-8")
            for name in ARTIFACTS:
                (cycle / name).write_bytes(PNG_SIGNATURE + b"evidence")

            destinations = publish(run, root / "analysis", "v2", 3)

            self.assertEqual(len(destinations), 3)
            self.assertTrue(all(path.name.startswith("v2-cycle-3-") for path in destinations))
            self.assertTrue(all(path.read_bytes() == PNG_SIGNATURE + b"evidence" for path in destinations))
            self.assertTrue(all((cycle / name).exists() for name in ARTIFACTS))
            with self.assertRaises(FileExistsError):
                publish(run, root / "analysis", "v2", 3)

    def test_rejects_missing_score_and_unversioned_artifacts(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            cycle = root / "run" / "cycles" / "cycle-1"
            cycle.mkdir(parents=True)
            with self.assertRaises(ValueError):
                publish(root / "run", root / "analysis", "v2", 1)
            self.assertFalse((root / "analysis").exists())


if __name__ == "__main__":
    unittest.main()
