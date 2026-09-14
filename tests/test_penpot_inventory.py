from __future__ import annotations

import json
import unittest

from scripts.penpot_inventory import INVENTORY_CODE, extract_inventory
from scripts.penpot_mcp import MCPError


class PenpotInventoryTests(unittest.TestCase):
    def test_extracts_execute_code_result(self):
        inventory = {
            "tokens": [{"name": "color.primary"}],
            "components": [{"name": "Button"}],
            "component_instances": [{"name": "Button/home"}],
            "detached_instances": [],
            "styles": [{"name": "Body"}],
            "required_component_instances": [],
        }
        response = {"content": [{"type": "text", "text": json.dumps({"result": inventory, "log": ""})}]}
        self.assertEqual(extract_inventory(response), inventory)

    def test_rejects_missing_result(self):
        with self.assertRaises(MCPError):
            extract_inventory({"content": [{"type": "text", "text": "not-json"}]})

    def test_inventory_code_uses_real_component_and_token_apis(self):
        self.assertIn("penpot.library.local", INVENTORY_CODE)
        self.assertIn("penpotUtils.tokenOverview()", INVENTORY_CODE)
        self.assertIn("isComponentInstance()", INVENTORY_CODE)
        self.assertIn("detached_instances", INVENTORY_CODE)


if __name__ == "__main__":
    unittest.main()
