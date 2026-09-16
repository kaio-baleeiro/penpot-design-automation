#!/usr/bin/env python3
"""Publish sanitized comparison PNGs from an immutable benchmark run.

Cycle evidence stays untouched. Only the three visual comparison artifacts are
copied into the benchmark's tracked analysis directory, with version/cycle
names so a later reconstruction cannot erase earlier evidence.
"""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path


ARTIFACTS = (
    "home-side-by-side-annotated.png",
    "home-overlay.png",
    "home-heatmap.png",
)
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def publish(run_dir: Path, analysis_dir: Path, version: str, cycle: int) -> list[Path]:
    if not version or not version.replace("-", "").isalnum() or not version[0].isalnum():
        raise ValueError("version must contain only letters, digits or hyphens")
    if cycle not in (1, 2, 3):
        raise ValueError("cycle must be 1, 2 or 3")
    cycle_dir = run_dir / "cycles" / f"cycle-{cycle}"
    score_path = cycle_dir / "score.json"
    issues_path = cycle_dir / "issues.json"
    if not score_path.is_file() or not issues_path.is_file():
        raise ValueError("score and issues must exist before publishing a cycle")
    score = json.loads(score_path.read_text(encoding="utf-8"))
    issues = json.loads(issues_path.read_text(encoding="utf-8"))
    if score.get("cycle") != cycle or issues.get("cycle") != cycle:
        raise ValueError("cycle metadata does not match its directory")

    sources = [cycle_dir / name for name in ARTIFACTS]
    for source in sources:
        if not source.is_file():
            raise ValueError(f"missing or invalid comparison PNG: {source}")
        with source.open("rb") as stream:
            if stream.read(8) != PNG_SIGNATURE:
                raise ValueError(f"missing or invalid comparison PNG: {source}")
    destinations = [analysis_dir / f"{version}-cycle-{cycle}-{name}" for name in ARTIFACTS]
    if any(destination.exists() for destination in destinations):
        raise FileExistsError("published evidence already exists; do not overwrite it")
    analysis_dir.mkdir(parents=True, exist_ok=True)
    for source, destination in zip(sources, destinations):
        shutil.copyfile(source, destination)
    return destinations


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", required=True, type=Path)
    parser.add_argument("--analysis-dir", required=True, type=Path)
    parser.add_argument("--version", required=True)
    parser.add_argument("--cycle", required=True, type=int)
    args = parser.parse_args()
    for destination in publish(args.run_dir, args.analysis_dir, args.version, args.cycle):
        print(destination)


if __name__ == "__main__":
    main()
