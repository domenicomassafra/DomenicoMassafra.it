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
  if curl -fsSIL --max-time 8 "https://$domain/" >/tmp/domain-status-headers.$$ 2>/dev/null; then
    sed -n '1p' /tmp/domain-status-headers.$$ | sed 's/^/  /'
  else
    printf '  unavailable\n'
  fi
  rm -f /tmp/domain-status-headers.$$
done
