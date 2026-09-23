#!/usr/bin/env bash
set -Eeuo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd -P)"
. "$SCRIPT_DIR/common.sh"
require_infrastructure_mode
require_command curl
load_runtime_env
for attempt in $(seq 1 60); do
  if curl --fail --silent --max-time 3 "${PENPOT_PUBLIC_URI%/}/" >/dev/null; then
    printf 'Penpot API ready.\n'
    exit 0
  fi
  sleep 2
done
die "Penpot não ficou pronto no tempo esperado"
