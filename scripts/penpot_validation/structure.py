"""Deterministic structural gates for Penpot exports.

The Penpot MCP/export step can emit an inventory next to the visual export.  A
visual score cannot establish that a design-system instance is still editable,
so this module deliberately keeps that check separate and machine-readable.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable


INVENTORY_KEYS = (
    "tokens",
    "components",
    "component_instances",
    "detached_instances",
    "styles",
    "required_component_instances",
)


def _items(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    if isinstance(value, dict):
        # Exporters occasionally group entries by type/name.
        return [item for key, item in value.items() if key not in {"count", "total"}]
    return [value]


def _names(value: Any) -> set[str]:
    names: set[str] = set()
    for item in _items(value):
        if isinstance(item, str):
            if item.strip():
                names.add(item.strip())
            continue
        if not isinstance(item, dict):
            continue
        for key in ("name", "id", "key", "token", "component", "component_name", "instance", "instance_name"):
            candidate = item.get(key)
            if isinstance(candidate, str) and candidate.strip():
                names.add(candidate.strip())
    return names


def _required(manifest: dict[str, Any], *keys: str) -> list[Any]:
    values: list[Any] = []
    for key in keys:
        if key in manifest:
            values.extend(_items(manifest[key]))
    for container_name in ("design_system", "requirements", "structure"):
        container = manifest.get(container_name)
        if isinstance(container, dict):
            for key in keys:
                if key in container:
                    values.extend(_items(container[key]))
    return values


def _display_name(item: Any) -> str:
    if isinstance(item, str):
        return item.strip()
    if isinstance(item, dict):
        for key in ("name", "id", "key", "token", "component", "component_name", "instance", "instance_name"):
            value = item.get(key)
            if isinstance(value, str) and value.strip():
                return value.strip()
    return str(item)


def load_inventory(path: str | Path) -> dict[str, Any]:
    inventory_path = Path(path)
    try:
        value = json.loads(inventory_path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"Penpot inventory does not exist: {inventory_path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"Penpot inventory is not valid JSON: {inventory_path}") from exc
    if not isinstance(value, dict):
        raise ValueError("Penpot inventory must be a JSON object")
    return value


def validate_structure_inventory(inventory: dict[str, Any], manifest: dict[str, Any] | None = None) -> dict[str, Any]:
    """Return an objective structural gate result.

    Required names can be declared by the manifest (``required_tokens``,
    ``required_components`` and ``required_component_instances``), while the
    inventory's own ``required_component_instances`` is always enforced.
    """

    manifest = manifest or {}
    missing_keys = [key for key in INVENTORY_KEYS if key not in inventory]
    errors: list[str] = []
    if missing_keys:
        errors.append("inventory missing required keys: " + ", ".join(missing_keys))

    token_names = _names(inventory.get("tokens"))
    component_names = _names(inventory.get("components"))
    instance_names = _names(inventory.get("component_instances"))
    required_tokens = [_display_name(item) for item in _required(manifest, "required_tokens", "tokens") if _display_name(item)]
    required_tokens.extend(_display_name(item) for item in _items(inventory.get("required_tokens", [])) if _display_name(item))
    required_components = [_display_name(item) for item in _required(manifest, "required_components", "components") if _display_name(item)]
    required_components.extend(_display_name(item) for item in _items(inventory.get("required_components", [])) if _display_name(item))
    required_instances = [_display_name(item) for item in _required(manifest, "required_component_instances") if _display_name(item)]
    required_instances.extend(_display_name(item) for item in _items(inventory.get("required_component_instances")) if _display_name(item))

    missing_tokens = sorted(set(required_tokens) - token_names)
    missing_components = sorted(set(required_components) - component_names)
    missing_instances = sorted(set(required_instances) - instance_names)
    detached = inventory.get("detached_instances", [])
    if isinstance(detached, dict):
        detached_count = int(detached.get("count", detached.get("total", len(detached))))
    elif isinstance(detached, (int, float)):
        detached_count = int(detached)
    else:
        detached_count = len(_items(detached))

    if missing_tokens:
        errors.append("missing required tokens: " + ", ".join(missing_tokens))
    if missing_components:
        errors.append("missing required components: " + ", ".join(missing_components))
    if missing_instances:
        errors.append("missing required component instances: " + ", ".join(missing_instances))
    if detached_count > 0:
        errors.append(f"detached instances present: {detached_count}")

    # A screenshot can score perfectly while still failing the actual design
    # contract. When the inventory provides frame summaries, require visible
    # editable descendants and reject an image-only frame.
    frame_summaries = _items(inventory.get("frame_summaries"))
    structural_frame_errors: list[str] = []
    for frame in frame_summaries:
        if not isinstance(frame, dict):
            continue
        name = str(frame.get("name") or frame.get("id") or "frame")
        try:
            editable_count = int(frame.get("editable_shape_count", 0))
            visible_children = int(frame.get("visible_children", 0))
        except (TypeError, ValueError):
            editable_count = 0
            visible_children = 0
        if frame.get("image_only") is True:
            structural_frame_errors.append(f"frame is image-only: {name}")
        if visible_children <= 1 or editable_count <= 1:
            structural_frame_errors.append(
                f"frame lacks substantive editable descendants: {name} "
                f"(visible_children={visible_children}, editable_shapes={editable_count})"
            )
    errors.extend(structural_frame_errors)

    if manifest.get("state") == "DS_REVALIDATING":
        if not token_names:
            errors.append("design-system inventory has no tokens")
        if not component_names:
            errors.append("design-system inventory has no components")
        if not instance_names:
            errors.append("design-system inventory has no component instances")
        if not _items(inventory.get("styles")):
            errors.append("design-system inventory has no shared styles")

    return {
        "passed": not errors,
        "errors": errors,
        "missing_inventory_keys": missing_keys,
        "missing_tokens": missing_tokens,
        "missing_components": missing_components,
        "missing_component_instances": missing_instances,
        "detached_instances": detached_count,
        "required_tokens": sorted(set(required_tokens)),
        "required_components": sorted(set(required_components)),
        "required_component_instances": sorted(set(required_instances)),
        "inventory_counts": {
            "tokens": len(token_names),
            "components": len(component_names),
            "component_instances": len(instance_names),
            "styles": len(_items(inventory.get("styles"))),
            "frames": len(frame_summaries),
        },
        "frame_errors": structural_frame_errors,
    }


# Short aliases make the gate convenient for callers and keep the public API
# discoverable for integrations that use the term "structure gate".
validate_structure = validate_structure_inventory
structure_gate = validate_structure_inventory
