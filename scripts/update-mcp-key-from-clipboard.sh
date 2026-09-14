#!/usr/bin/env bash
set -euo pipefail

project_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
env_file="${PENPOT_ENV_FILE:-$project_root/infra/penpot/.env}"
mcp_name="${PENPOT_MCP_NAME:-penpot-design}"

die() {
  printf 'erro: %s\n' "$*" >&2
  exit 1
}

command -v pbpaste >/dev/null 2>&1 || die "pbpaste não está disponível"
command -v codex >/dev/null 2>&1 || die "codex CLI não está disponível"
[[ -f "$env_file" ]] || die "arquivo local não encontrado: $env_file"

token="$(pbpaste)"
[[ "$token" == eyJ* ]] || die "a área de transferência não contém uma chave MCP válida"
[[ "$token" != *$'\n'* && "$token" != *$'\r'* ]] || die "a chave MCP contém quebras de linha"

public_uri="$(awk -F= '$1 == "PENPOT_PUBLIC_URI" {print substr($0, index($0, "=") + 1)}' "$env_file")"
[[ -n "$public_uri" ]] || die "PENPOT_PUBLIC_URI não está definido"
public_uri="${public_uri%/}"
endpoint="$public_uri/mcp/stream?userToken=$token"

tmp_file="$(mktemp "${env_file}.XXXXXX")"
trap 'rm -f "$tmp_file"; unset token endpoint' EXIT
chmod 600 "$tmp_file"

awk -v endpoint="$endpoint" '
  BEGIN { updated = 0 }
  /^PENPOT_MCP_URL=/ {
    print "PENPOT_MCP_URL=" endpoint
    updated = 1
    next
  }
  { print }
  END {
    if (!updated) print "PENPOT_MCP_URL=" endpoint
  }
' "$env_file" >"$tmp_file"

mv "$tmp_file" "$env_file"
chmod 600 "$env_file"

codex mcp remove "$mcp_name" >/dev/null 2>&1 || true
codex mcp add "$mcp_name" --url "$endpoint" >/dev/null

unset token endpoint
printf 'Credencial MCP local atualizada para %s.\n' "$mcp_name"
