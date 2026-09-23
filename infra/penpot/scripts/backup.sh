#!/usr/bin/env bash

set -Eeuo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
# shellcheck disable=SC1091
. "$SCRIPT_DIR/common.sh"

require_infrastructure_mode
require_command docker
load_runtime_env
ensure_external_volumes
compose ps --status running --services | grep -Fxq penpot-postgres || die "penpot-postgres não está em execução"

backup_root="${1:-$PENPOT_DIR/.local/backups}"
mkdir -p "$backup_root"
backup_dir="$backup_root/penpot-$(timestamp)"
mkdir "$backup_dir"
chmod 700 "$backup_dir"

compose exec -T penpot-postgres pg_dump -U penpot -d penpot --format=custom > "$backup_dir/database.dump"
docker run --rm \
  -v "$PENPOT_ASSETS_VOLUME:/source:ro" \
  -v "$backup_dir:/backup" \
  alpine:3.20 tar -czf /backup/assets.tgz -C /source .

cat > "$backup_dir/manifest.env" <<EOF
BACKUP_FORMAT=penpot-local-v1
CREATED_UTC=$(date -u '+%Y-%m-%dT%H:%M:%SZ')
COMPOSE_PROJECT_NAME=$COMPOSE_PROJECT_NAME
PENPOT_VERSION=${PENPOT_VERSION:-unknown}
PENPOT_POSTGRES_VOLUME=$PENPOT_POSTGRES_VOLUME
PENPOT_ASSETS_VOLUME=$PENPOT_ASSETS_VOLUME
EOF

if command -v shasum >/dev/null 2>&1; then
  (cd "$backup_dir" && shasum -a 256 database.dump assets.tgz > SHA256SUMS)
fi
printf 'Backup criado em %s\n' "$backup_dir"
