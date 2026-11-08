# Direzione visiva del sito — proposta eseguibile, 7 novembre 2026, tema scuro 8 novembre 2026

Stato: candidata implementata sul branch #9, convertita a tema scuro l'8 novembre. La preferenza estetica definitiva dell'owner deve ancora essere verificata.

## Perché il nuovo impianto

Il 2 novembre l'owner ha valutato la precedente homepage «pessima». La nuova versione segue il mandato successivo del 7 novembre di completare i siti. Si presenta come una pagina editoriale personale: Domenico è visibile in una fotografia autentica, il messaggio iniziale è verificabile e la prima azione invita a raccontare un problema concreto attraverso il contatto già funzionante.

## Identità e composizione

- **Modo:** Persuade, con voce da sperimentatore e spiegatore. Nessun immaginario di agenzia, cliente inventato o cruscotto finto.
- **Mondo:** foglio di appunti e album delle prove su fondo scuro. Sfondo Notte #0b0d0e, inchiostro #f2ede2; l'accento Signal è #ff725f sulle superfici scure e torna #a72f21 sulle superfici chiare invertite. I bordi separano sezioni e materiali; l'immagine reale occupa il foglio, affiancata da una nota.
- **Composizione:** titolo e azione immediati; ritratto autentico e nota a destra, poi due progetti pubblici, un piccolo verdetto apribile, spiegazione personale e contatto finale. A 800 px le colonne diventano sequenza verticale.
- **Tipografia:** sans leggibile per interfaccia e messaggio principale, serif soltanto per note e contrappunti. Nessun font remoto che rallenti o tracci il visitatore.
- **Interazione:** navigazione per ancore, HTML details nativo per il verdetto, focus ben visibile, hover leggero; nessun JavaScript di prodotto né audio automatico. La preferenza prefers-reduced-motion elimina il movimento evitabile.
- **Stati e canali:** l'unica CTA di contatto verificata apre il profilo Instagram; la disponibilità del pulsante «Messaggio» dipende dal profilo e dall'accesso del visitatore. Link progetto e codice sono secondari.

## Alternative valutate

1. **Lettera aperta** — pagina molto editoriale, fotografia protagonista, parole calde e gerarchia narrativa. Rischio: senza foto originale grande il cuore visivo perde forza; i progetti diventano troppo discreti.
2. **Album delle prove** — **implementazione candidata**. Ritratto vero in formato contenuto, voce personale, esperimenti raggiungibili, una microesperienza verificabile e percorso diretto al contatto. Rischio: avatar corrente da 150 px; sostituirlo con una foto originale prima di considerare definitiva l'identità.
3. **Rapporto di campo** — schede di verifica, note, limiti e confronti più espliciti. Rischio: per un pubblico non tecnico può sembrare un software o un registro tecnico anziché la homepage di una persona.

Il prototipo del 30 ottobre in docs/prototypes/issue-9-creative-directions.html rimane evidenza storica delle alternative precedenti; le scelte estetiche di quel round sono state superate dalla valutazione del 2 novembre.

## Tema scuro — 8 novembre 2026

L'owner ha chiesto l'inversione della homepage il 8 novembre 12:05: fondo nero, testo chiaro, stesso impianto e stessi contenuti. È una **refinement**, non un nuovo mondo: struttura, copy, fotografia e azioni restano identici, cambia la luce.

Token in `site/styles.css` (`:root`, `color-scheme:dark`):

| Token | Valore | Uso |
|---|---|---|
| `--paper` | `#0b0d0e` | fondo pagina |
| `--ink` | `#f2ede2` | testo principale |
| `--ink-soft` | `#a8a299` | testi secondari |
| `--signal` | `#ff725f` | accento su fondo scuro (stesso corallo del favicon) |
| `--signal-on-light` | `#a72f21` | accento sulle superfici chiare invertite |
| `--sheet` / `--surface` / `--card` | `#14171a` / `#12161a` / `#191d20` | pannelli sollevati |
| `--cream` / `--cream-dim` | `#f7f2e7` / `#e7e2d4` | superfici chiare invertite |
| `--ember` | `#3a120c` | fascia contatti |
| `--footer` | `#06080a` | piè di pagina |
| `--hair` / `--hair-strong` | `#2b2f31` / `#3d4345` | filetti e bordi |

Inversione per superficie: la pagina passa da carta a nero; la fascia statement da scura a crema con inchiostro scuro; la fascia metodo da chiara a pannello scuro; il riquadro "DM" da scuro a crema; la fascia contatti da rosso pieno a bragia profonda con crema. La fotografia mantiene la cornice chiara e un'ombra più profonda, così resta un oggetto fisico appoggiato al foglio.

Correzioni visive incluse nel passaggio: spaziatura ridotta tra le sezioni (padding 78–120 px invece di 85–140 px) e coda più stretta dopo la lista progetti; tracking dei titoli riportato entro −0,035em (era −0,042em) e monogramma "DM" a −0,02em (era −0,105em, lettere compresse); note di contatto a 13 px; testi secondari e filetti con contrasto reale sul fondo scuro; selezione del testo, caret e scrollbar temati dalla palette; intestazioni del foglio ritagliate sotto i 350 px per non spezzare le etichette.

## Anteprime renderizzate

Prima (main precedente): [desktop](docs/prototypes/issue-9-light-desktop.png) e [mobile 390 px](docs/prototypes/issue-9-light-mobile.png). Dopo: [desktop](docs/prototypes/issue-9-dark-desktop.png) e [mobile 390 px](docs/prototypes/issue-9-dark-mobile.png). Le catture sono generate da Chromium headless via CDP con pagina intera, servendo la directory pubblica `site/` in HTTP, con `--force-device-scale-factor=1` e viewport 1440×900 / 390×844.

## Fonti e limiti

Fonti: decisioni owner in [issue #9](https://github.com/domenicomassafra/DomenicoMassafra.it/issues/9), e canone Obsidian 04-areas/divulgazione/brand/positioning-v2.md, BRAND.md, EXECUTION-SYSTEM.md. L'immagine site/ritratto-instagram.jpg deriva il 7 novembre dalla proprietà og:image del profilo pubblico https://www.instagram.com/domenico.massafraa/, verificato da title/description; risoluzione ricevuta 150×150, uso in piccolo formato e nessuna generazione sintetica. Nessun contenuto del vault è copiato come nuova fonte canonica.

I marchi site/strumentini-mark.svg e site/dichiarazioni-mark.svg sono copie esatte dei rispettivi favicon.svg pubblici dei due prodotti di Domenico, scaricati il 7 novembre; entrambe le immagini sono usate come elementi decorativi accanto ai link editoriali, senza creare nuovi simboli fittizi.

## Verifiche

Suite Python sul sito statico esatto pubblicato da GitHub Pages, link interni risolti, HTML/CSS esposti via HTTP, immagine disponibile, fallback del verdetto, supporto a reduced motion. Il test `test_dark_theme_keeps_wcag_aa_contrast` calcola i rapporti di contrasto WCAG dai token di `:root` e impone 4,5:1 su testo normale (inclusi i secondari su fondo e pannelli), verifica che il fondo resti sotto 0,02 di luminanza relativa e che l'inchiostro superi 0,7. Verifica visuale headless e assenza di overflow orizzontale a 320/360/390/414/540/600/768/1024/1440 px. Per il DONE del ticket resta il giudizio owner sulla direzione scura e, se non è soddisfacente, la foto originale scelta.
