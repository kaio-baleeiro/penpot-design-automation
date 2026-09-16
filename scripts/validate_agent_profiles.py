#!/usr/bin/env python3
"""Validate portable agent profiles without third-party packages."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_KEYS = {"name", "description", "model", "phase"}


def _frontmatter(text: str) -> dict[str, str]:
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    result: dict[str, str] = {}
    for line in parts[1].splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            result[key.strip()] = value.strip()
    return result


def validate(root: Path = ROOT) -> list[str]:
    agents = root / "agents"
    errors: list[str] = []
    manifest = agents / "manifest.yaml"
    contract = agents / "contracts" / "handoff.md"
    if not manifest.is_file():
        errors.append("agents/manifest.yaml is missing")
    if not contract.is_file():
        errors.append("agents/contracts/handoff.md is missing")
    profile_ids = re.findall(r"^  - id: ([a-z0-9-]+)$", manifest.read_text(encoding="utf-8"), re.MULTILINE) if manifest.is_file() else []
    if not profile_ids:
        errors.append("agents/manifest.yaml declares no profiles")
    for profile_id in profile_ids:
        directory = agents / "profiles" / profile_id
        if not (directory / "README.md").is_file():
            errors.append(f"{profile_id}: README.md is missing")
        prompt = directory / "AGENT.md"
        if not prompt.is_file():
            errors.append(f"{profile_id}: AGENT.md is missing")
            continue
        metadata = _frontmatter(prompt.read_text(encoding="utf-8"))
        missing = sorted(REQUIRED_KEYS - metadata.keys())
        if missing:
            errors.append(f"{profile_id}: missing frontmatter {', '.join(missing)}")
        if metadata.get("name") != profile_id:
            errors.append(f"{profile_id}: frontmatter name does not match directory")
        if metadata.get("model") != "gpt-5.6-luna":
            errors.append(f"{profile_id}: model must be gpt-5.6-luna")
    return errors


def main() -> int:
    errors = validate()
    if errors:
        print("Agent profile validation failed:\n" + "\n".join(f"- {error}" for error in errors))
        return 1
    count = len(re.findall(r"^  - id: ", (ROOT / "agents/manifest.yaml").read_text(encoding="utf-8"), re.MULTILINE))
    print(f"Validated {count} portable agent profiles")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
