#!/usr/bin/env python3
"""Create and resolve lessons inside a versioned Agent Skill package."""

from __future__ import annotations

import argparse
from datetime import date
import os
from pathlib import Path
import re


def project_root(explicit: str | None) -> Path:
    if explicit:
        root = Path(explicit).expanduser().resolve()
    elif os.environ.get("PENPOT_PROJECT_ROOT"):
        root = Path(os.environ["PENPOT_PROJECT_ROOT"]).expanduser().resolve()
    else:
        root = Path(__file__).resolve().parents[3]
    if not (root / "skills").is_dir():
        raise SystemExit(f"erro: raiz do projeto não encontrada: {root}")
    return root


def selected_skill(root: Path, value: str | None) -> Path:
    candidate = Path(value or "skills/penpot-design").expanduser()
    if not candidate.is_absolute():
        candidate = root / candidate
    candidate = candidate.resolve()
    skills_root = (root / "skills").resolve()
    if candidate.parent != skills_root or not (candidate / "SKILL.md").is_file():
        raise SystemExit(f"erro: informe uma pasta de skill válida dentro de {skills_root}")
    return candidate


def lessons_dir(skill: Path) -> Path:
    target = skill / "lessons-learned"
    target.mkdir(parents=True, exist_ok=True)
    return target


def safe_title(value: str) -> str:
    title = re.sub(r"[\\/:*?\"<>|\x00-\x1f]", "-", value).strip(" .-")
    title = re.sub(r"\s+", " ", title)
    if not title:
        raise SystemExit("erro: título da lição está vazio")
    return title[:120].rstrip()


def ensure_index(target: Path, skill_name: str) -> Path:
    index = target / "README.md"
    if not index.exists():
        index.write_text(
            "\n".join(
                [
                    f"# Lições de {skill_name}",
                    "",
                    "Registre falhas reproduzíveis, contramedidas e verificações "
                    "nesta pasta. Consulte o índice transversal em "
                    "`../../penpot-design/lessons-learned/README.md` quando a regra "
                    "afetar mais de uma fase.",
                    "",
                    "## Lessons",
                    "",
                    "<!-- lesson-links -->",
                    "",
                ]
            ),
            encoding="utf-8",
        )
    return index


def add_index_link(index: Path, lesson_path: Path) -> None:
    link = f"- [{lesson_path.stem}]({lesson_path.name})"
    text = index.read_text(encoding="utf-8")
    if link in text:
        return
    marker = "<!-- lesson-links -->"
    if marker not in text:
        raise SystemExit(f"erro: marcador de índice ausente em {index}")
    index.write_text(text.replace(marker, f"{link}\n{marker}"), encoding="utf-8")


def record(args: argparse.Namespace) -> int:
    root = project_root(args.project_root)
    skill = selected_skill(root, args.skill_dir)
    target = lessons_dir(skill)
    title = safe_title(args.title)
    path = target / f"LL - {title}.md"
    if path.exists():
        raise SystemExit(f"erro: lição já existe; atualize a nota existente: {path}")
    today = date.today().isoformat()
    applies = args.applies_to or [skill.name]
    if args.kind == "project" and not args.integration:
        raise SystemExit("erro: lições project exigem --integration")
    body = [
        "---",
        "type: lesson",
        "status: active",
        f"skill: {skill.name}",
        f"kind: {args.kind}",
        f"integration: {args.integration or 'none'}",
        f"created: {today}",
        f"updated: {today}",
        "source_agent: portable-agent",
        "confidence: high",
        "review: false",
        "applies_to:",
        *[f"  - {item}" for item in applies],
        "---",
        "",
        f"# LL - {title}",
        "",
        "## Lesson",
        "",
        args.lesson.strip(),
        "",
        "## Context",
        "",
        args.context.strip(),
        "",
        "## Evidence",
        "",
        args.evidence.strip(),
        "",
        "## Future Rule",
        "",
        args.future_rule.strip(),
        "",
    ]
    path.write_text("\n".join(body), encoding="utf-8")
    add_index_link(ensure_index(target, skill.name), path)
    print(path.relative_to(root))
    return 0


def resolve(args: argparse.Namespace) -> int:
    root = project_root(args.project_root)
    skill = selected_skill(root, args.skill_dir)
    target = lessons_dir(skill).resolve()
    candidate = (target / args.lesson).resolve()
    if candidate.parent != target or not candidate.is_file():
        raise SystemExit("erro: lição deve ser um arquivo existente no pacote da skill")
    text = candidate.read_text(encoding="utf-8")
    if not re.search(r"(?m)^status: active$", text):
        raise SystemExit("erro: somente uma lição ativa pode ser marcada como mitigada")
    if "## Resolution" in text:
        raise SystemExit("erro: lição já possui resolução")
    today = date.today().isoformat()
    text = re.sub(r"(?m)^status: active$", "status: mitigated", text, count=1)
    text = re.sub(r"(?m)^updated: .*?$", f"updated: {today}", text, count=1)
    text += "\n".join(
        [
            "",
            "## Resolution",
            "",
            f"Resolved: {today}",
            "",
            "### Countermeasure",
            "",
            args.countermeasure.strip(),
            "",
            "### Verification",
            "",
            args.verification.strip(),
            "",
        ]
    )
    candidate.write_text(text, encoding="utf-8")
    print(candidate.relative_to(root))
    return 0


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description=__doc__)
    root.add_argument("--project-root")
    root.add_argument("--skill-dir", default="skills/penpot-design")
    commands = root.add_subparsers(dest="command", required=True)
    create = commands.add_parser("record")
    create.add_argument("--title", required=True)
    create.add_argument("--lesson", required=True)
    create.add_argument("--context", required=True)
    create.add_argument("--evidence", required=True)
    create.add_argument("--future-rule", required=True)
    create.add_argument("--applies-to", action="append")
    create.add_argument("--kind", choices=("machine", "project"), required=True)
    create.add_argument("--integration")
    create.set_defaults(handler=record)
    complete = commands.add_parser("resolve")
    complete.add_argument("--lesson", required=True)
    complete.add_argument("--countermeasure", required=True)
    complete.add_argument("--verification", required=True)
    complete.set_defaults(handler=resolve)
    return root


def main() -> int:
    args = parser().parse_args()
    return args.handler(args)


if __name__ == "__main__":
    raise SystemExit(main())
