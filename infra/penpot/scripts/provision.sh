#!/usr/bin/env bash
set -Eeuo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd -P)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd -P)"
. "$SCRIPT_DIR/common.sh"
require_infrastructure_mode
python_bin="${PENPOT_AUTOMATION_PYTHON:-$PROJECT_ROOT/.venv/bin/python}"
[[ -x "$python_bin" ]] || python_bin="$(command -v python3)"
exec "$python_bin" "$PROJECT_ROOT/scripts/penpot_provision.py" --env-file "$ENV_FILE" "$@"
