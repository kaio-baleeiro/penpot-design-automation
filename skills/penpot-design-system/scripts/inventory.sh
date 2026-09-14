#!/usr/bin/env bash
set -Eeuo pipefail

skill_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)"
project_root="$(cd "$skill_root/../.." && pwd -P)"
exec "$project_root/scripts/penpot-inventory.sh" "$@"
