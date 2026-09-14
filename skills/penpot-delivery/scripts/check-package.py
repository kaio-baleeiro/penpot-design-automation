#!/usr/bin/env python3
"""Check the minimum immutable evidence required for Penpot delivery."""

from __future__ import annotations

import json
from pathlib import Path
import sys


def main() -> int:
    if len(sys.argv) != 2:
        print(f"uso: {Path(sys.argv[0]).name} <run-dir>", file=sys.stderr)
        return 2
    run_dir = Path(sys.argv[1]).resolve()
    manifest_path = run_dir / "delivery" / "manifest.json"
    report_path = run_dir / "delivery" / "report.md"
    errors: list[str] = []
    if not manifest_path.is_file():
        errors.append("delivery/manifest.json ausente")
    if not report_path.is_file():
        errors.append("delivery/report.md ausente")
    if errors:
        print("; ".join(errors), file=sys.stderr)
        return 1
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("state") not in {"DELIVERED", "NEEDS_REVIEW"}:
        errors.append("estado terminal inválido")
    if not isinstance(manifest.get("visual_artifacts"), list) or not {
        "side_by_side_annotated", "overlay", "heatmap", "issues"
    }.issubset(manifest["visual_artifacts"]):
        errors.append("evidência visual obrigatória incompleta")
    if "lesson_refs" not in manifest or not isinstance(manifest["lesson_refs"], list):
        errors.append("lesson_refs ausente ou inválido")
    if errors:
        print("; ".join(errors), file=sys.stderr)
        return 1
    print(f"delivery package valid: {run_dir.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
