#!/usr/bin/env python3
"""Block Penpot builds whose planned assets are unresolved or placeholders."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


READY = {"embedded_first_party", "downloaded", "available", "ready", "uploaded_to_penpot", "local_verified", "resolved"}


def _refs(value: Any) -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        for key, item in value.items():
            if key == "asset_ref" and isinstance(item, str):
                found.add(item)
            elif key == "asset_refs" and isinstance(item, list):
                found.update(ref for ref in item if isinstance(ref, str))
            found.update(_refs(item))
    elif isinstance(value, list):
        for item in value:
            found.update(_refs(item))
    return found


def validate_asset_readiness(plan: dict[str, Any], manifest: dict[str, Any]) -> dict[str, Any]:
    refs = _refs(plan)
    assets = {item.get("asset_id"): item for item in manifest.get("assets", []) if isinstance(item, dict) and item.get("asset_id")}
    errors: list[str] = []
    if not refs:
        errors.append("build plan has no asset_ref entries")
    for ref in sorted(refs):
        asset = assets.get(ref)
        if not asset:
            errors.append(f"planned asset is missing from manifest: {ref}")
            continue
        location = asset.get("local_path") or asset.get("path") or asset.get("origin") or asset.get("url")
        if not isinstance(location, str) or not location.strip():
            errors.append(f"asset has no usable URL/path: {ref}")
        status = str(asset.get("acquisition") or asset.get("status") or "").strip().lower()
        if status not in READY:
            errors.append(f"asset is not build-ready: {ref} ({status or 'missing status'})")
    return {"passed": not errors, "asset_refs": sorted(refs), "errors": errors}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", required=True)
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--output")
    args = parser.parse_args()
    plan = json.loads(Path(args.plan).read_text(encoding="utf-8"))
    manifest = json.loads(Path(args.manifest).read_text(encoding="utf-8"))
    result = validate_asset_readiness(plan, manifest)
    rendered = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).write_text(rendered + "\n", encoding="utf-8")
    else:
        print(rendered)
    return 0 if result["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
