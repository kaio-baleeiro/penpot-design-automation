#!/usr/bin/env bash

set -Eeuo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
# shellcheck disable=SC1091
. "$SCRIPT_DIR/common.sh"

require_command docker
load_runtime_env
tail_lines="${PENPOT_LOG_TAIL:-100}"
[[ "$tail_lines" =~ ^[0-9]+$ ]] || die "PENPOT_LOG_TAIL deve ser numérico"
[[ $# -le 1 ]] || die "uso: ./scripts/logs.sh [serviço]"

if [[ $# -eq 1 ]]; then
  compose logs --follow --tail="$tail_lines" "$1"
else
  compose logs --follow --tail="$tail_lines"
fi
