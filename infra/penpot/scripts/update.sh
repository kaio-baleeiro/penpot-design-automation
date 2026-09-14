#!/usr/bin/env bash

set -Eeuo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
# shellcheck disable=SC1091
. "$SCRIPT_DIR/common.sh"

require_command docker
load_runtime_env
ensure_external_volumes
[[ $# -eq 1 ]] || die "uso: ./scripts/update.sh VERSÃO (ex.: 2.17.1)"
new_version="$1"
[[ "$new_version" =~ ^[0-9]+\.[0-9]+([.][0-9]+)?$ ]] || die "versão inválida: $new_version"

"$SCRIPT_DIR/validate.sh"
backup_output="$("$SCRIPT_DIR/backup.sh")"
backup_dir="${backup_output#Backup criado em }"
old_version="${PENPOT_VERSION:-}"
[[ -n "$old_version" ]] || die "PENPOT_VERSION ausente em .env"

cp "$ENV_FILE" "$ENV_FILE.before-update"
UPDATE_FAILED=1
trap 'if [[ "$UPDATE_FAILED" == 1 ]]; then mv -f "$ENV_FILE.before-update" "$ENV_FILE"; printf "Versão anterior restaurada em .env; backup: %s\n" "$backup_dir" >&2; fi' EXIT
sed -i.bak -E "s/^PENPOT_VERSION=.*/PENPOT_VERSION=$new_version/" "$ENV_FILE"
rm -f "$ENV_FILE.bak"
PENPOT_VERSION="$new_version"
compose pull
compose up -d
rm -f "$ENV_FILE.before-update"
UPDATE_FAILED=0
printf 'Penpot atualizado de %s para %s; backup: %s\n' "$old_version" "$new_version" "$backup_dir"
