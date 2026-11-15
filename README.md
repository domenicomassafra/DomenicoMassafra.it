# DomenicoMassafra.it

Sito personale di Domenico Massafra.

## Obiettivi

- home essenziale per il brand personale;
- link canonici ai progetti [Strumentini.it](https://strumentini.it/) e [DichiarazioniPubbliche.it](https://dichiarazionipubbliche.it/);
- sito statico, veloce e senza dipendenze runtime: l'unico script, `site/board.js` (palette del tabellone), è locale e facoltativo;
- font Archivo e JetBrains Mono serviti dal sito in `site/fonts/` (licenza SIL OFL in `site/fonts/OFL.txt`), nessuna richiesta a servizi di terzi;
- deploy automatico su GitHub Pages a ogni push su `main`;
- dominio canonico `https://domenicomassafra.it/`.

## Sviluppo locale

Non ci sono dipendenze da installare. Per una preview locale:

```bash
python3 -m http.server 8080 --directory site
```

Poi apri `http://localhost:8080`.

## Deploy

Il workflow `.github/workflows/pages.yml` pubblica esclusivamente i file pubblici nella directory `site/` su GitHub Pages.
Il dominio personalizzato viene configurato sul repository tramite GitHub Pages e il DNS viene gestito separatamente su Cloudflare.
