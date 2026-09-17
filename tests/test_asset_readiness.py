from __future__ import annotations

import unittest

from scripts.validate_asset_readiness import validate_asset_readiness


class AssetReadinessTests(unittest.TestCase):
    def test_exact_ready_asset_passes(self) -> None:
        plan = {"sections": [{"asset_ref": "hero"}]}
        manifest = {"assets": [{"asset_id": "hero", "origin": "https://example.test/hero.png", "acquisition": "uploaded_to_penpot"}]}
        self.assertTrue(validate_asset_readiness(plan, manifest)["passed"])

    def test_deferred_or_missing_asset_blocks_build(self) -> None:
        plan = {"asset_refs": ["hero", "logo"]}
        manifest = {"assets": [{"asset_id": "hero", "url": "https://example.test/hero.png", "acquisition": "deferred"}]}
        result = validate_asset_readiness(plan, manifest)
        self.assertFalse(result["passed"])
        self.assertTrue(any("not build-ready" in error for error in result["errors"]))
        self.assertTrue(any("missing from manifest" in error for error in result["errors"]))


if __name__ == "__main__":
    unittest.main()
