#!/usr/bin/env python3
"""Create and resolve project lessons in the canonical shared vault."""

from __future__ import annotations

import argparse
from datetime import date
import os
from pathlib import Path
import re


PROJECT_SLUG = "penpot-design-automation"
PROJECT_LINK = "[[P - Penpot Design Automation]]"


def vault_root(explicit: str | None) -> Path:
    if explicit:
        root = Path(explicit).expanduser().resolve()
    elif os.environ.get("AI_SECOND_BRAIN_ROOT"):
        root = Path(os.environ["AI_SECOND_BRAIN_ROOT"]).expanduser().resolve()
    else:
        root = next(
            (parent for parent in Path(__file__).resolve().parents if (parent / "AGENTS.md").is_file()),
            None,
        )
        if root is None:
            raise SystemExit("erro: vault não encontrado; informe --vault-root ou AI_SECOND_BRAIN_ROOT")
    if not (root / "AGENTS.md").is_file():
        raise SystemExit(f"erro: AGENTS.md não encontrado no vault: {root}")
    return root


def lesson_dir(root: Path) -> Path:
    target = root / "35-Lessons-Learned" / "Projects" / PROJECT_SLUG
    target.mkdir(parents=True, exist_ok=True)
    return target


def safe_title(value: str) -> str:
    title = re.sub(r"[\\/:*?\"<>|\x00-\x1f]", "-", value).strip(" .-")
    title = re.sub(r"\s+", " ", title)
    if not title:
        raise SystemExit("erro: título da lição está vazio")
    return title[:120].rstrip()


def ensure_index(target: Path) -> Path:
    index = target / "README.md"
    if not index.exists():
        today = date.today().isoformat()
        index.write_text(
            "\n".join(
                [
                    "---",
                    "type: lesson-index",
                    "status: active",
                    f"created: {today}",
                    f"updated: {today}",
                    "source_agent: codex",
                    "agent_context: penpot-design-automation",
                    "confidence: high",
                    "review: false",
                    "---",
                    "",
                    "# Penpot Design Automation Lessons",
                    "",
                    f"Projeto relacionado: {PROJECT_LINK}",
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


def add_index_link(index: Path, title: str) -> None:
    link = f"- [[LL - {title}]]"
    text = index.read_text(encoding="utf-8")
    if link in text:
        return
    marker = "<!-- lesson-links -->"
    if marker not in text:
        raise SystemExit(f"erro: marcador de índice ausente em {index}")
    today = date.today().isoformat()
    text = re.sub(r"(?m)^updated: .*?$", f"updated: {today}", text, count=1)
    index.write_text(text.replace(marker, f"{link}\n{marker}"), encoding="utf-8")


def record(args: argparse.Namespace) -> int:
    root = vault_root(args.vault_root)
    target = lesson_dir(root)
    title = safe_title(args.title)
    path = target / f"LL - {title}.md"
    if path.exists():
        raise SystemExit(f"erro: lição já existe; atualize a nota existente: {path}")
    today = date.today().isoformat()
    applies = args.applies_to or [PROJECT_LINK]
    body = [
        "---",
        "type: lesson",
        "status: active",
        f"created: {today}",
        f"updated: {today}",
        "source_agent: codex",
        "agent_context: penpot-design-automation",
        f"project: \"{PROJECT_LINK}\"",
        f"confidence: {args.confidence}",
        "review: false",
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
        "## Applies To",
        "",
        *[f"- {item}" for item in applies],
        "",
        "## Links",
        "",
        f"- {PROJECT_LINK}",
        "",
    ]
    with path.open("x", encoding="utf-8") as handle:
        handle.write("\n".join(body))
    add_index_link(ensure_index(target), title)
    print(path.relative_to(root))
    return 0


def resolve(args: argparse.Namespace) -> int:
    root = vault_root(args.vault_root)
    target = lesson_dir(root).resolve()
    candidate = (target / args.lesson).resolve()
    if candidate.parent != target or not candidate.is_file():
        raise SystemExit("erro: lição deve ser um arquivo existente no espaço canônico do projeto")
    text = candidate.read_text(encoding="utf-8")
    if not re.search(r"(?m)^status: active$", text):
        raise SystemExit("erro: somente uma lição ativa pode ser marcada como mitigada")
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
    root.add_argument("--vault-root")
    commands = root.add_subparsers(dest="command", required=True)
    create = commands.add_parser("record")
    create.add_argument("--title", required=True)
    create.add_argument("--lesson", required=True)
    create.add_argument("--context", required=True)
    create.add_argument("--evidence", required=True)
    create.add_argument("--future-rule", required=True)
    create.add_argument("--applies-to", action="append")
    create.add_argument("--confidence", choices=("low", "medium", "high"), default="high")
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
