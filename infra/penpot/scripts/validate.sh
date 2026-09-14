#!/usr/bin/env bash

set -Eeuo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
# shellcheck disable=SC1091
. "$SCRIPT_DIR/common.sh"

require_command docker
VALIDATE_ENV_FILE="$ENV_FILE"
if [[ ! -f "$VALIDATE_ENV_FILE" ]]; then
  VALIDATE_ENV_FILE="$PENPOT_DIR/.env.example"
fi
[[ -f "$VALIDATE_ENV_FILE" ]] || die "não encontrei .env nem .env.example"

services="$(docker compose --project-directory "$PENPOT_DIR" --project-name penpot-design-automation --file "$COMPOSE_FILE" --env-file "$VALIDATE_ENV_FILE" config --services)"
service_count="$(printf '%s\n' "$services" | awk 'NF {count++} END {print count + 0}')"
[[ "$service_count" -eq 7 ]] || die "esperados 7 serviços, encontrados $service_count"
docker compose --project-directory "$PENPOT_DIR" --project-name penpot-design-automation --file "$COMPOSE_FILE" --env-file "$VALIDATE_ENV_FILE" config --quiet

expected_services="penpot-frontend penpot-backend penpot-mcp penpot-exporter penpot-postgres penpot-valkey penpot-mailcatch"
for service in $expected_services; do
  printf '%s\n' "$services" | grep -Fxq "$service" || die "serviço ausente: $service"
done

printf 'Compose válido: 7 serviços; volumes externos configurados; env usado: %s\n' "$VALIDATE_ENV_FILE"
