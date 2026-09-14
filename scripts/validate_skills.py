#!/usr/bin/env python3
"""Validate the repository's Codex skills without external dependencies."""

from __future__ import annotations

import re
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = PROJECT_ROOT / "skills"
REQUIRED_SKILLS = {
    "penpot-design",
    "penpot-intake",
    "penpot-source-map",
    "penpot-build",
    "penpot-validate",
    "penpot-design-system",
    "penpot-delivery",
}
PLACEHOLDERS = re.compile(r"\b(?:TODO|TBD|PLACEHOLDER)\b", re.IGNORECASE)


def _frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        raise ValueError("missing YAML frontmatter")
    try:
        block = text.split("---\n", 2)[1]
    except IndexError as exc:
        raise ValueError("unterminated YAML frontmatter") from exc
    fields: dict[str, str] = {}
    for line in block.splitlines():
        if not line or line.startswith((" ", "\t")) or ":" not in line:
            continue
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip().strip('"\'')
    return fields


def validate_skill(skill_dir: Path) -> list[str]:
    errors: list[str] = []
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.is_file():
        return [f"{skill_dir.name}: missing SKILL.md"]
    text = skill_file.read_text(encoding="utf-8")
    try:
        metadata = _frontmatter(text)
    except ValueError as exc:
        return [f"{skill_dir.name}: {exc}"]
    if metadata.get("name") != skill_dir.name:
        errors.append(f"{skill_dir.name}: frontmatter name must match directory")
    if not metadata.get("description"):
        errors.append(f"{skill_dir.name}: missing description")
    if PLACEHOLDERS.search(text):
        errors.append(f"{skill_dir.name}: unresolved placeholder")
    agent_file = skill_dir / "agents" / "openai.yaml"
    if not agent_file.is_file():
        errors.append(f"{skill_dir.name}: missing agents/openai.yaml")
    elif f"${skill_dir.name}" not in agent_file.read_text(encoding="utf-8"):
        errors.append(f"{skill_dir.name}: default prompt must reference ${skill_dir.name}")
    return errors


def main() -> int:
    found = {path.name for path in SKILLS_ROOT.iterdir() if path.is_dir()}
    errors = [f"missing skill directory: {name}" for name in sorted(REQUIRED_SKILLS - found)]
    for skill_dir in sorted((path for path in SKILLS_ROOT.iterdir() if path.is_dir()), key=lambda path: path.name):
        errors.extend(validate_skill(skill_dir))
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(f"Validated {len(found)} skills")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
