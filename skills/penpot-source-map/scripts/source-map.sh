#!/usr/bin/env bash
set -Eeuo pipefail

skill_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)"
project_root="$(cd "$skill_root/../.." && pwd -P)"
python_bin="${PENPOT_AUTOMATION_PYTHON:-$project_root/.venv/bin/python}"
[[ -x "$python_bin" ]] || python_bin="$(command -v python3)"

operation="${1:-}"
[[ -n "$operation" ]] || {
  printf 'uso: %s capture|map-screenshot|frame-spec|compile [argumentos]\n' "$0" >&2
  exit 2
}
shift
cd "$project_root"
for argument in "$@"; do
  if [[ "$argument" == --help || "$argument" == -h ]]; then
    case "$operation" in
      capture|map-screenshot|frame-spec) exec "$python_bin" -m scripts.penpot_validation "$operation" "$@" ;;
      compile) exec "$python_bin" -m scripts.penpot_validation.source_map "$@" ;;
    esac
  fi
done
"$python_bin" "$project_root/scripts/workflow_guard.py" require design >/dev/null

case "$operation" in
  capture|map-screenshot|frame-spec)
    exec "$python_bin" -m scripts.penpot_validation "$operation" "$@"
    ;;
  compile)
    exec "$python_bin" -m scripts.penpot_validation.source_map "$@"
    ;;
  *)
    printf 'operação desconhecida: %s\n' "$operation" >&2
    exit 2
    ;;
esac
