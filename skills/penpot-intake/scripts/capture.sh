#!/usr/bin/env bash
set -Eeuo pipefail

skill_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)"
project_root="$(cd "$skill_root/../.." && pwd -P)"
python_bin="${PENPOT_AUTOMATION_PYTHON:-$project_root/.venv/bin/python}"
[[ -x "$python_bin" ]] || python_bin="$(command -v python3)"

cd "$project_root"
for argument in "$@"; do [[ "$argument" != --help && "$argument" != -h ]] || exec "$python_bin" -m scripts.penpot_validation capture "$@"; done
"$python_bin" "$project_root/scripts/workflow_guard.py" require design >/dev/null
exec "$python_bin" -m scripts.penpot_validation capture "$@"
