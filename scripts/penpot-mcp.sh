#!/usr/bin/env bash

set -Eeuo pipefail

project_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)"
if [[ -n "${PENPOT_ENV_FILE:-}" ]]; then env_file="$PENPOT_ENV_FILE"
elif [[ -f "$project_root/.env" ]]; then env_file="$project_root/.env"
else env_file="$project_root/infra/penpot/.env"; fi
python_bin="${PENPOT_AUTOMATION_PYTHON:-$project_root/.venv/bin/python}"

[[ -f "$env_file" ]] || {
  printf 'Configuração local ausente: %s\n' "$env_file" >&2
  exit 2
}

[[ -x "$python_bin" ]] || python_bin="$(command -v python3)"
"$python_bin" "$project_root/scripts/workflow_guard.py" require design >/dev/null

set -a
# shellcheck disable=SC1090
source "$env_file"
set +a

exec "$python_bin" "$project_root/scripts/penpot_mcp.py" "$@"
