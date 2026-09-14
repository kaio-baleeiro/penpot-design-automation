#!/usr/bin/env bash

set -Eeuo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
# shellcheck disable=SC1091
. "$SCRIPT_DIR/common.sh"

require_command docker
load_runtime_env
ensure_external_volumes
"$SCRIPT_DIR/validate.sh"
compose up -d
printf 'Penpot iniciado. Interface: http://localhost:9001 | Mailcatcher: http://localhost:1080\n'
