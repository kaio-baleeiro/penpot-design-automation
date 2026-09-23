#!/usr/bin/env bash

set -Eeuo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
# shellcheck disable=SC1091
. "$SCRIPT_DIR/common.sh"

require_infrastructure_mode
require_command docker
load_runtime_env
ensure_external_volumes

[[ "${PENPOT_RESTORE_CONFIRM:-}" == YES ]] || die "restore destrutivo bloqueado; defina PENPOT_RESTORE_CONFIRM=YES"
[[ $# -eq 1 ]] || die "uso: PENPOT_RESTORE_CONFIRM=YES ./scripts/restore.sh /caminho/do/backup"
backup_dir="$(cd "$1" 2>/dev/null && pwd)" || die "diretório de backup não encontrado: $1"
[[ -f "$backup_dir/manifest.env" && -f "$backup_dir/database.dump" && -f "$backup_dir/assets.tgz" ]] || die "backup incompleto: esperado manifest.env, database.dump e assets.tgz"

manifest_assets="$(awk -F= '$1 == "PENPOT_ASSETS_VOLUME" {print substr($0, index($0, "=") + 1)}' "$backup_dir/manifest.env")"
manifest_postgres="$(awk -F= '$1 == "PENPOT_POSTGRES_VOLUME" {print substr($0, index($0, "=") + 1)}' "$backup_dir/manifest.env")"
[[ "$manifest_assets" == "$PENPOT_ASSETS_VOLUME" ]] || die "volume de assets do backup não corresponde ao volume configurado"
[[ "$manifest_postgres" == "$PENPOT_POSTGRES_VOLUME" ]] || die "volume PostgreSQL do backup não corresponde ao volume configurado"

printf 'ATENÇÃO: este restore substituirá o banco e os assets nos volumes externos configurados.\n'
printf 'Backup: %s\n' "$backup_dir"

compose stop penpot-frontend penpot-backend penpot-exporter penpot-mcp
compose up -d penpot-postgres penpot-valkey
compose exec -T penpot-postgres pg_isready -U penpot -d penpot >/dev/null
compose exec -T penpot-postgres pg_restore -U penpot -d penpot --clean --if-exists --no-owner < "$backup_dir/database.dump"
docker run --rm \
  -v "$PENPOT_ASSETS_VOLUME:/target" \
  -v "$backup_dir:/backup:ro" \
  alpine:3.20 sh -ec 'find /target -mindepth 1 -maxdepth 1 -exec rm -rf {} +; tar -xzf /backup/assets.tgz -C /target'
compose up -d
printf 'Restore concluído; execute ./scripts/healthcheck.sh antes de reabrir o trabalho.\n'
