#!/usr/bin/env bash

set -Eeuo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PENPOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd -P)"
ENV_FILE="${PENPOT_ENV_FILE:-$PENPOT_DIR/.env}"

command -v openssl >/dev/null 2>&1 || {
  printf 'Erro: openssl é necessário para gerar segredos locais.\n' >&2
  exit 1
}

if [[ -f "$ENV_FILE" ]]; then
  printf 'Configuração já existe: %s\n' "$ENV_FILE"
  printf 'Nada foi sobrescrito. Use esse arquivo ou remova-o conscientemente para reconfigurar.\n'
  exit 0
fi

umask 077
secret_key="$(openssl rand -hex 64)"
database_password="$(openssl rand -hex 32)"
sed \
  -e "s|replace-with-a-random-64-byte-hex-secret|$secret_key|" \
  -e "s|replace-with-a-strong-local-database-password|$database_password|" \
  "$PENPOT_DIR/.env.example" > "$ENV_FILE"
chmod 600 "$ENV_FILE"
printf 'Configuração local criada: %s\n' "$ENV_FILE"
printf 'Volumes neutros serão criados automaticamente pelo up.sh.\n'
