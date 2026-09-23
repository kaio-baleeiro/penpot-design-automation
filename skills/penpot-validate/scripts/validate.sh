#!/usr/bin/env bash
set -Eeuo pipefail

skill_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)"
project_root="$(cd "$skill_root/../.." && pwd -P)"
python_bin="${PENPOT_AUTOMATION_PYTHON:-$project_root/.venv/bin/python}"
[[ -x "$python_bin" ]] || python_bin="$(command -v python3)"

cd "$project_root"
for argument in "$@"; do [[ "$argument" != --help && "$argument" != -h ]] || exec "$python_bin" -m scripts.penpot_validation validate "$@"; done
"$python_bin" "$project_root/scripts/workflow_guard.py" require design >/dev/null
run_dir=""
args=("$@")
for ((i=0; i < ${#args[@]}; i++)); do
  if [[ "${args[$i]}" == --run-dir && $((i + 1)) -lt ${#args[@]} ]]; then run_dir="${args[$((i + 1))]}"; break; fi
done
[[ -n "$run_dir" ]] || { printf 'validate.sh exige --run-dir\n' >&2; exit 2; }
"$python_bin" "$project_root/scripts/workflow_guard.py" audit-run --run-dir "$run_dir" --expect-state VALIDATING --expect-state DS_REVALIDATING >/dev/null
exec "$python_bin" -m scripts.penpot_validation validate "$@"
