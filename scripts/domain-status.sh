#!/usr/bin/env bash
set -euo pipefail

domains=(
  domenicomassafra.it
  strumentini.it
  dichiarazionipubbliche.it
)

for domain in "${domains[@]}"; do
  printf '\n===== %s =====\n' "$domain"

  status="$(whois "$domain" 2>/dev/null | awk -F: '/^Status:/ {sub(/^[[:space:]]+/, "", $2); print $2; exit}')"
  printf 'registry: %s\n' "${status:-unknown}"

  printf 'NS:\n'
  dig +short NS "$domain" | sed 's/^/  /' || true

  printf 'A:\n'
  dig +short A "$domain" | sed 's/^/  /' || true

  printf 'AAAA:\n'
  dig +short AAAA "$domain" | sed 's/^/  /' || true

  printf 'MX:\n'
  dig +short MX "$domain" | sed 's/^/  /' || true

  printf 'HTTPS:\n'
  if http_status="$(curl -sSIL --max-time 8 -o /dev/null -w '%{http_code}' "https://$domain/" 2>/dev/null)"; then
    printf '  HTTP %s\n' "$http_status"
  else
    printf '  unavailable\n'
  fi
done
