#!/usr/bin/env bash

set -Eeuo pipefail
project_root="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"

command -v python3 >/dev/null 2>&1 || {
  printf 'Erro: python3 é necessário.\n' >&2
  exit 1
}
command -v docker >/dev/null 2>&1 || {
  printf 'Erro: Docker com Compose é necessário para subir o Penpot.\n' >&2
  exit 1
}

if [[ ! -x "$project_root/.venv/bin/python" ]]; then
  python3 -m venv "$project_root/.venv"
fi
"$project_root/.venv/bin/python" -m pip install -r "$project_root/scripts/requirements.txt"

if [[ "${PENPOT_INSTALL_PLAYWRIGHT:-true}" == "true" ]]; then
  "$project_root/.venv/bin/python" -m playwright install chromium
fi

"$project_root/install.sh"
"$project_root/infra/penpot/scripts/bootstrap.sh"
"$project_root/infra/penpot/scripts/validate.sh"

printf '\nPronto para uso. Execute:\n'
printf '  %s/infra/penpot/scripts/up.sh\n' "$project_root"
printf '  %s/infra/penpot/scripts/healthcheck.sh\n' "$project_root"
printf 'Depois configure o MCP local conforme infra/penpot/README.md.\n'
