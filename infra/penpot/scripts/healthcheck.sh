#!/usr/bin/env bash

set -Eeuo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
# shellcheck disable=SC1091
. "$SCRIPT_DIR/common.sh"

require_infrastructure_mode
require_command docker
require_command curl
load_runtime_env
ensure_external_volumes

compose ps
curl --fail --silent --show-error --max-time 10 http://127.0.0.1:9001/ >/dev/null || die "Penpot não respondeu em http://localhost:9001"
curl --fail --silent --show-error --max-time 10 http://127.0.0.1:1080/ >/dev/null || die "Mailcatcher não respondeu em http://localhost:1080"

for service in penpot-postgres penpot-valkey; do
  state="$(compose ps --status running --services | grep -Fx "$service" || true)"
  [[ "$state" == "$service" ]] || die "serviço não está em execução: $service"
done

printf 'Healthcheck OK: HTTP, Mailcatcher, PostgreSQL, Valkey e volumes externos.\n'
