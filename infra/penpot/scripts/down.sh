#!/usr/bin/env bash

set -Eeuo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
# shellcheck disable=SC1091
. "$SCRIPT_DIR/common.sh"

require_infrastructure_mode
require_command docker
load_runtime_env
compose down
printf 'Penpot parado; volumes preservados.\n'
