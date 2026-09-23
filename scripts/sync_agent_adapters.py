#!/usr/bin/env python3
"""Generate native subagent wrappers from the canonical portable profiles."""

from __future__ import annotations

import argparse
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROFILE_ROOT = ROOT / "agents" / "profiles"
TARGETS = {
    "claude-code": (ROOT / ".claude" / "agents", "haiku"),
    "devin-cli": (ROOT / ".devin" / "agents", "gemini-3-8-flash-low"),
    "gemini-cli": (ROOT / ".gemini" / "agents", "gemini-3.8-flash"),
}


def metadata(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    parts = text.split("---", 2)
    if len(parts) < 3:
        raise ValueError(f"missing frontmatter: {path}")
    values: dict[str, str] = {}
    for line in parts[1].splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            values[key.strip()] = value.strip()
    return values


def render(runtime: str, profile: Path, model: str | None) -> str:
    values = metadata(profile)
    profile_id = values["name"]
    description = values["description"]
    model_line = f"model: {model}\n" if model else ""
    return (
        "---\n"
        f"name: {profile_id}\n"
        f"description: {description}\n"
        f"{model_line}"
        "---\n\n"
        f"You are the `{profile_id}` worker for the Penpot design workflow.\n\n"
        f"Read `agents/profiles/{profile_id}/AGENT.md` completely and follow it as the\n"
        "canonical profile. Read `agents/contracts/handoff.md` before returning work.\n"
        f"The active runtime is `{runtime}`. Record its resolved model and runtime in the\n"
        "handoff. Before visual work, open an assigned image using native vision or an image tool and record visual_capability_verified plus the image hash. Do not change scores, thresholds, source evidence, or prior cycles.\n"
    )


def expected_files() -> dict[Path, str]:
    profiles = sorted(PROFILE_ROOT.glob("*/AGENT.md"))
    output: dict[Path, str] = {}
    for runtime, (directory, model) in TARGETS.items():
        for profile in profiles:
            profile_id = metadata(profile)["name"]
            output[directory / f"{profile_id}.md"] = render(runtime, profile, model)
    return output


def sync(check: bool = False) -> list[str]:
    mismatches: list[str] = []
    expected = expected_files()
    for path, content in expected.items():
        if not path.is_file() or path.read_text(encoding="utf-8") != content:
            mismatches.append(str(path.relative_to(ROOT)))
            if not check:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content, encoding="utf-8")
    for directory, _ in TARGETS.values():
        if directory.is_dir():
            for path in directory.glob("*.md"):
                if path not in expected:
                    mismatches.append(str(path.relative_to(ROOT)))
                    if not check:
                        path.unlink()
    return sorted(set(mismatches))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    mismatches = sync(check=args.check)
    if args.check and mismatches:
        print("Agent adapters are out of sync:\n" + "\n".join(f"- {item}" for item in mismatches))
        return 1
    action = "Updated" if mismatches else "Verified"
    print(f"{action} {len(expected_files())} native agent adapters")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
