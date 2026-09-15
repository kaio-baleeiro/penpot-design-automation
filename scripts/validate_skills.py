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
VALID_NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
RESOURCE_REFERENCE = re.compile(r"(?<![\w/])((?:scripts|references|assets)/[A-Za-z0-9._-]+)")
OPTIONAL_RESOURCE_DIRS = ("scripts", "references", "assets")
LESSONS_DIR = "lessons-learned"


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
    if not (skill_dir / "README.md").is_file():
        errors.append(f"{skill_dir.name}: missing README.md")
    text = skill_file.read_text(encoding="utf-8")
    try:
        metadata = _frontmatter(text)
    except ValueError as exc:
        return [f"{skill_dir.name}: {exc}"]
    if metadata.get("name") != skill_dir.name:
        errors.append(f"{skill_dir.name}: frontmatter name must match directory")
    if not VALID_NAME.fullmatch(skill_dir.name) or len(skill_dir.name) > 64:
        errors.append(f"{skill_dir.name}: invalid Agent Skills name")
    description = metadata.get("description", "")
    if not description:
        errors.append(f"{skill_dir.name}: missing description")
    elif len(description) > 1024:
        errors.append(f"{skill_dir.name}: description exceeds 1024 characters")
    compatibility = metadata.get("compatibility", "")
    if compatibility and len(compatibility) > 500:
        errors.append(f"{skill_dir.name}: compatibility exceeds 500 characters")
    if PLACEHOLDERS.search(text):
        errors.append(f"{skill_dir.name}: unresolved placeholder")
    if len(text.splitlines()) > 500:
        errors.append(f"{skill_dir.name}: SKILL.md exceeds 500 lines")
    if "../" in text or "<repository-root>/workflow" in text:
        errors.append(f"{skill_dir.name}: SKILL.md contains an external/deep resource path")
    for reference in RESOURCE_REFERENCE.findall(text):
        if not (skill_dir / reference).is_file():
            errors.append(f"{skill_dir.name}: missing referenced resource {reference}")
    for dirname in OPTIONAL_RESOURCE_DIRS:
        resource_dir = skill_dir / dirname
        if resource_dir.exists() and not any(path.is_file() for path in resource_dir.rglob("*")):
            errors.append(f"{skill_dir.name}: optional directory {dirname}/ is empty")
    lessons_dir = skill_dir / LESSONS_DIR
    if not lessons_dir.is_dir():
        errors.append(f"{skill_dir.name}: missing required directory {LESSONS_DIR}/")
    elif not (lessons_dir / "README.md").is_file():
        errors.append(f"{skill_dir.name}: {LESSONS_DIR}/README.md is required")
    else:
        for bucket, expected_kind in (("project", "project"), ("local", "machine")):
            bucket_dir = lessons_dir / bucket
            if not bucket_dir.is_dir():
                errors.append(f"{skill_dir.name}: missing required directory {LESSONS_DIR}/{bucket}/")
                continue
            if not (bucket_dir / "README.md").is_file():
                errors.append(f"{skill_dir.name}: {LESSONS_DIR}/{bucket}/README.md is required")
            for lesson in sorted(path for path in bucket_dir.glob("*.md") if path.name != "README.md"):
                try:
                    lesson_metadata = _frontmatter(lesson.read_text(encoding="utf-8"))
                except ValueError as exc:
                    errors.append(f"{skill_dir.name}: {lesson.name}: {exc}")
                    continue
                kind = lesson_metadata.get("kind")
                if kind != expected_kind:
                    errors.append(f"{skill_dir.name}: {lesson.name}: bucket {bucket}/ requires kind: {expected_kind}")
                if kind == "project" and not lesson_metadata.get("integration"):
                    errors.append(f"{skill_dir.name}: {lesson.name}: project lesson requires integration")
                if kind == "machine" and lesson_metadata.get("integration") not in {None, "", "none"}:
                    errors.append(f"{skill_dir.name}: {lesson.name}: machine lesson cannot declare project integration")
    scripts_dir = skill_dir / "scripts"
    if scripts_dir.is_dir():
        for script in (path for path in scripts_dir.rglob("*") if path.is_file()):
            if "__pycache__" in script.parts or script.suffix == ".pyc" or script.name == "README.md":
                continue
            if not script.stat().st_mode & 0o111:
                errors.append(f"{skill_dir.name}: script is not executable: {script.relative_to(skill_dir)}")
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
    print(f"Validated {len(found)} Agent Skills packages")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
