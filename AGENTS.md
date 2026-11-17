## Mappa

- `site/` — il sito statico servito (HTML, CSS, JS, immagini, sitemap); ci scrive chi cambia il sito.
- `scripts/domain-status.sh` — il controllo dello stato del dominio.
- `tests/` — le prove delle pagine e dello script del sito; ci scrive chi cambia `site/`.
- `docs/` — `domain-cutover.md` e la storia del dominio.
- `DESIGN.md` e `PRODUCT.md` — design e prodotto.

## Agent skills

### Issue tracker

GitHub Issues in this repo's `origin` remote, driven with the `gh` CLI. See `docs/agents/issue-tracker.md`.

### Triage labels

The five canonical triage labels, each named exactly as its role. See `docs/agents/triage-labels.md`.

### Domain docs

single-context: `GLOSSARY.md` and `docs/adr/` at the repo root. See `docs/agents/domain.md`.
