#!/usr/bin/env bash

set -Eeuo pipefail

project_root="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
source_skill="$project_root/skills/penpot-design"
skills_root="${AGENTS_SKILLS_DIR:-$HOME/.agents/skills}"
target_skill="$skills_root/penpot-design"

[[ -f "$source_skill/SKILL.md" ]] || {
  printf 'Skill canônica ausente: %s\n' "$source_skill" >&2
  exit 1
}

mkdir -p "$skills_root"

if [[ -L "$target_skill" ]]; then
  current_target="$(readlink "$target_skill")"
  if [[ "$current_target" == "$source_skill" ]]; then
    printf 'Skill global já instalada: %s\n' "$target_skill"
    exit 0
  fi
  printf 'Já existe outro vínculo em %s; remova-o conscientemente antes de instalar.\n' "$target_skill" >&2
  exit 1
fi

if [[ -e "$target_skill" ]]; then
  printf 'Já existe uma skill não gerenciada em %s; instalação interrompida.\n' "$target_skill" >&2
  exit 1
fi

ln -s "$source_skill" "$target_skill"
printf 'Skill global instalada: %s -> %s\n' "$target_skill" "$source_skill"
