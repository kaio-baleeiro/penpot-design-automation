#!/usr/bin/env python3
"""Export a sanitized structural inventory from the connected Penpot file."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from scripts.penpot_mcp import MCPError, PenpotMCPClient


INVENTORY_CODE = r"""
const lib = penpot.library.local;
const pages = penpot.currentFile.pages;
const shapes = pages.flatMap(page => penpotUtils.findShapes(() => true, page.root));
const components = lib.components.map(component => ({id: component.id, name: component.name}));
const componentInstances = shapes.filter(shape => shape.isComponentInstance()).map(shape => ({
  id: shape.id,
  name: shape.name,
  component: shape.component() ? shape.component().name : null
}));
const mainInstances = shapes.filter(shape => shape.isComponentMainInstance());
const componentNames = new Set(components.map(component => component.name.toLowerCase()));
const detachedInstances = shapes.filter(shape =>
  !shape.isComponentInstance() && !shape.isComponentMainInstance() &&
  componentNames.has((shape.name || '').toLowerCase())
).map(shape => ({id: shape.id, name: shape.name}));
const tokenOverview = penpotUtils.tokenOverview();
const tokens = Object.entries(tokenOverview).flatMap(([setName, groups]) =>
  Object.entries(groups || {}).flatMap(([type, names]) =>
    (names || []).map(name => ({set: setName, type, name}))
  )
);
const styles = [
  ...lib.colors.map(style => ({id: style.id, name: style.name, type: 'color'})),
  ...lib.typographies.map(style => ({id: style.id, name: style.name, type: 'typography'}))
];
const countTypes = list => list.reduce((acc, shape) => {
  const type = shape.type || 'unknown';
  acc[type] = (acc[type] || 0) + 1;
  return acc;
}, {});
const frameSummaries = pages.flatMap(page =>
  page.root.children
    .filter(shape => shape.type === 'board' && /Home — 1440x/.test(shape.name || ''))
    .map(frame => {
      const descendants = penpotUtils.findShapes(() => true, frame);
      const visible = descendants.filter(shape => shape.visible !== false);
      const typeCounts = countTypes(visible);
      const editable = visible.filter(shape => !['board', 'group'].includes(shape.type));
      const imageShapes = visible.filter(shape =>
        shape.type === 'image' || (shape.fills || []).some(fill => fill && fill.fillImage)
      );
      return {
        id: frame.id,
        name: frame.name,
        visible_children: (frame.children || []).filter(shape => shape.visible !== false).length,
        descendant_count: visible.length,
        editable_shape_count: editable.length,
        type_counts: typeCounts,
        image_shape_count: imageShapes.length,
        image_only: editable.length > 0 && editable.every(shape =>
          shape.type === 'image' || (shape.fills || []).some(fill => fill && fill.fillImage)
        )
      };
    })
);
return {
  schema_version: '1.0',
  file: {id: penpot.currentFile.id, name: penpot.currentFile.name},
  pages: pages.map(page => ({id: page.id, name: page.name})),
  shape_count: shapes.length,
  shape_type_counts: countTypes(shapes),
  frame_summaries: frameSummaries,
  main_component_instances: mainInstances.map(shape => ({id: shape.id, name: shape.name})),
  tokens,
  components,
  component_instances: componentInstances,
  detached_instances: detachedInstances,
  styles,
  required_component_instances: []
};
""".strip()


def extract_inventory(response: Any) -> dict[str, Any]:
    """Extract the returned JavaScript value from an execute_code response."""
    if not isinstance(response, dict):
        raise MCPError("Penpot inventory response is not an object")
    content = response.get("content")
    if not isinstance(content, list):
        raise MCPError("Penpot inventory response has no content")
    for item in content:
        if not isinstance(item, dict) or item.get("type") != "text" or not isinstance(item.get("text"), str):
            continue
        try:
            payload = json.loads(item["text"])
        except json.JSONDecodeError:
            continue
        inventory = payload.get("result") if isinstance(payload, dict) else None
        if isinstance(inventory, dict):
            return inventory
    raise MCPError("Penpot inventory response did not contain a result object")


def main() -> int:
    project_root = Path(__file__).resolve().parents[1]
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    from scripts.workflow_guard import require
    require("design")
    parser = argparse.ArgumentParser(description="Export the connected Penpot file's structural inventory")
    parser.add_argument("--output", required=True)
    parser.add_argument("--log-path")
    args = parser.parse_args()
    target = Path(args.output)
    if target.exists():
        raise MCPError(f"inventory output already exists: {target}")
    client = PenpotMCPClient(log_path=args.log_path)
    inventory = extract_inventory(client.execute({"code": INVENTORY_CODE}))
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("x", encoding="utf-8") as handle:
        json.dump(inventory, handle, ensure_ascii=False, indent=2)
    print(json.dumps({
        "saved_inventory": str(target),
        "tokens": len(inventory.get("tokens", [])),
        "components": len(inventory.get("components", [])),
        "component_instances": len(inventory.get("component_instances", [])),
        "detached_instances": len(inventory.get("detached_instances", [])),
        "styles": len(inventory.get("styles", [])),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except MCPError as exc:
        print(f"penpot-inventory: {exc}")
        raise SystemExit(2)
