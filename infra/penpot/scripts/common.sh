#!/usr/bin/env bash

set -Eeuo pipefail

PENPOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENV_FILE="${PENPOT_ENV_FILE:-$PENPOT_DIR/.env}"
COMPOSE_FILE="$PENPOT_DIR/compose.yml"

die() {
  printf 'Erro: %s\n' "$*" >&2
  exit 1
}

require_command() {
  command -v "$1" >/dev/null 2>&1 || die "comando ausente: $1"
}

require_env_file() {
  [[ -f "$ENV_FILE" ]] || die "crie $ENV_FILE a partir de .env.example; segredos não são versionados"
}

load_runtime_env() {
  require_env_file
  set -a
  # shellcheck disable=SC1090
  . "$ENV_FILE"
  set +a

  [[ "${PENPOT_SECRET_KEY:-}" != replace-* && -n "${PENPOT_SECRET_KEY:-}" ]] || die "PENPOT_SECRET_KEY não foi preenchida em .env"
  [[ "${PENPOT_POSTGRES_PASSWORD:-}" != replace-* && -n "${PENPOT_POSTGRES_PASSWORD:-}" ]] || die "PENPOT_POSTGRES_PASSWORD não foi preenchida em .env"
  PENPOT_POSTGRES_VOLUME="${PENPOT_POSTGRES_VOLUME:-katiauinvest-penpot_penpot_postgres_data}"
  PENPOT_ASSETS_VOLUME="${PENPOT_ASSETS_VOLUME:-katiauinvest-penpot_penpot_assets}"
  COMPOSE_PROJECT_NAME="${COMPOSE_PROJECT_NAME:-penpot-design-automation}"
}

compose() {
  docker compose \
    --project-directory "$PENPOT_DIR" \
    --project-name "$COMPOSE_PROJECT_NAME" \
    --file "$COMPOSE_FILE" \
    --env-file "$ENV_FILE" \
    "$@"
}

ensure_external_volumes() {
  docker volume inspect "$PENPOT_POSTGRES_VOLUME" >/dev/null 2>&1 || die "volume PostgreSQL ausente: $PENPOT_POSTGRES_VOLUME"
  docker volume inspect "$PENPOT_ASSETS_VOLUME" >/dev/null 2>&1 || die "volume de assets ausente: $PENPOT_ASSETS_VOLUME"
}

timestamp() {
  date -u '+%Y%m%dT%H%M%SZ'
}
