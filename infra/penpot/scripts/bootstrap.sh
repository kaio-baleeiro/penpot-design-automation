#!/usr/bin/env bash

set -Eeuo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PENPOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd -P)"
PROJECT_ROOT="$(cd "$PENPOT_DIR/../.." && pwd -P)"
ENV_FILE="${PENPOT_ENV_FILE:-$PROJECT_ROOT/.env}"
ENV_EXAMPLE="$PROJECT_ROOT/.env.example"
python_bin="${PENPOT_AUTOMATION_PYTHON:-$PROJECT_ROOT/.venv/bin/python}"
[[ -x "$python_bin" ]] || python_bin="$(command -v python3)"
"$python_bin" "$PROJECT_ROOT/scripts/workflow_guard.py" require infrastructure >/dev/null

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
account_password="$(openssl rand -base64 36 | tr -d '\n' | tr '/+' '_-')"
if [[ -f "$PENPOT_DIR/.env" ]]; then
  # Preserve an existing workstation's volume names and deployment secrets.
  cp "$PENPOT_DIR/.env" "$ENV_FILE"
  chmod 600 "$ENV_FILE"
  for assignment in \
    "PENPOT_ADMIN_EMAIL=penpot-automation@localhost" \
    "PENPOT_ADMIN_PASSWORD=$account_password" \
    "PENPOT_MCP_URL=" \
    "PENPOT_MCP_TOKEN="; do
    key="${assignment%%=*}"
    if ! grep -q "^${key}=" "$ENV_FILE"; then
      printf '%s\n' "$assignment" >> "$ENV_FILE"
    fi
  done
  chmod 600 "$ENV_FILE"
  printf 'Configuração migrada com volumes existentes: %s\n' "$ENV_FILE"
  printf 'Credenciais de automação foram inicializadas; não serão impressas em logs.\n'
  exit 0
fi
sed \
  -e "s|replace-with-a-random-64-byte-hex-secret|$secret_key|" \
  -e "s|replace-with-a-strong-local-database-password|$database_password|" \
  -e "s|replace-with-a-strong-local-account-password|$account_password|" \
  "$ENV_EXAMPLE" > "$ENV_FILE"
chmod 600 "$ENV_FILE"
printf 'Configuração local criada: %s\n' "$ENV_FILE"
printf 'Volumes neutros serão criados automaticamente pelo up.sh.\n'
