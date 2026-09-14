#!/usr/bin/env bash

set -Eeuo pipefail

project_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)"
env_file="$project_root/infra/penpot/.env"
python_bin="${PENPOT_AUTOMATION_PYTHON:-$project_root/.venv/bin/python}"

[[ -f "$env_file" ]] || {
  printf 'Configuração local ausente: %s\n' "$env_file" >&2
  exit 2
}

[[ -x "$python_bin" ]] || python_bin="$(command -v python3)"

set -a
# shellcheck disable=SC1090
source "$env_file"
set +a

cd "$project_root"
exec "$python_bin" -m scripts.penpot_inventory "$@"
