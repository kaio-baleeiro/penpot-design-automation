#!/usr/bin/env bash

set -Eeuo pipefail

PENPOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)"
PROJECT_ROOT="$(cd "$PENPOT_DIR/../.." && pwd -P)"
if [[ -n "${PENPOT_ENV_FILE:-}" ]]; then
  ENV_FILE="$PENPOT_ENV_FILE"
elif [[ -f "$PROJECT_ROOT/.env" ]]; then
  ENV_FILE="$PROJECT_ROOT/.env"
elif [[ -f "$PENPOT_DIR/.env" ]]; then
  ENV_FILE="$PENPOT_DIR/.env"
else
  ENV_FILE="$PROJECT_ROOT/.env"
fi
COMPOSE_FILE="$PENPOT_DIR/compose.yml"

die() {
  printf 'Erro: %s\n' "$*" >&2
  exit 1
}

require_infrastructure_mode() {
  local python_bin="${PENPOT_AUTOMATION_PYTHON:-$PROJECT_ROOT/.venv/bin/python}"
  [[ -x "$python_bin" ]] || python_bin="$(command -v python3)"
  "$python_bin" "$PROJECT_ROOT/scripts/workflow_guard.py" require infrastructure >/dev/null
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
  PENPOT_POSTGRES_VOLUME="${PENPOT_POSTGRES_VOLUME:-penpot-design-automation_postgres_data}"
  PENPOT_ASSETS_VOLUME="${PENPOT_ASSETS_VOLUME:-penpot-design-automation_assets}"
  PENPOT_CREATE_VOLUMES="${PENPOT_CREATE_VOLUMES:-false}"
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
  for volume in "$PENPOT_POSTGRES_VOLUME" "$PENPOT_ASSETS_VOLUME"; do
    if docker volume inspect "$volume" >/dev/null 2>&1; then
      continue
    fi
    if [[ "$PENPOT_CREATE_VOLUMES" == "true" ]]; then
      docker volume create "$volume" >/dev/null || die "não foi possível criar o volume: $volume"
      printf 'Volume criado: %s\n' "$volume"
    else
      die "volume ausente: $volume (use bootstrap.sh em um clone novo ou crie/restaure o volume explicitamente)"
    fi
  done
}

timestamp() {
  date -u '+%Y%m%dT%H%M%SZ'
}
