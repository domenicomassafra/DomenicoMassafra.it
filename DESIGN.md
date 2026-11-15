# Sistema visivo del sito — 15 novembre 2026

Stato: redesign completo della issue #18, sul canone di marca applicato alla lettera.

## Perché

L'owner ha bocciato due direzioni: la homepage del 2 novembre («pessima») e «Officina cinetica» il 14 novembre, per un arancione fuori palette e un aspetto peggiore. Il 15 novembre ha chiesto un redesign completo. Decisione: nessuna interpretazione creativa dei colori o dei caratteri. Il sito usa esattamente la palette, la tipografia, le label e le frasi approvate del canone di marca (`~/Obsidian/04-areas/divulgazione/brand/BRAND.md`, `EXECUTION-SYSTEM.md`, `positioning-v2.md`); un test blocca ogni valore diverso.

## Colori

Token in `:root` di `site/styles.css`, con `color-scheme:dark`.

| Token | Valore | Uso |
|---|---|---|
| `--carbon` | `#0b0b0d` | fondo pagina; testo su Paper, su White e sul pulsante Signal Bright |
| `--panel` | `#151517` | pannelli sollevati: quadro «Come lavoro», fascia dei verdetti |
| `--line` | `#2c2c30` | filetti e bordi su scuro (decorazione) |
| `--paper` | `#f5f0e8` | fasce chiare: frase di fondo e progetti; pulsante del menu |
| `--paper-line` | `#d9d2c5` | bordi delle schede su chiaro (decorazione) |
| `--white` | `#ffffff` | testo su scuro e su Signal; fondo delle schede progetto |
| `--signal` | `#d63f28` | campiture (fascia contatti, chip «No»), testo grande su chiaro |
| `--signal-bright` | `#ff5a3c` | accento su scuro: parole chiave, label `// `, pulsante principale, focus |
| `--ash` | `#9a948b` | testo secondario su scuro |
| `--graphite` | `#66615b` | testo secondario su chiaro |

Regole del canone: Signal non va mai come testo normale su scuro (4,31:1), si usa Signal Bright; un solo rosso per inquadratura.

## Tipografia

- Archivo variabile 400–800 (`site/fonts/archivo.woff2`): titoli 700 con tracking −0,03em, testo 500–600.
- JetBrains Mono 700 (`site/fonts/jetbrains-mono.woff2`): solo label maiuscole che iniziano con `// ` e il `//` del wordmark.
- Font serviti dal sito stesso, licenza SIL OFL in `site/fonts/OFL.txt`; nessuna richiesta a Google Fonts o a terzi. Fallback: Arial/Helvetica e ui-monospace/Menlo.

## Struttura della pagina

1. **Intestazione** fissa e traslucida: wordmark «Domenico Massafra//», ancore Verdetti, Progetti, Chi sono e il pulsante chiaro «Scrivimi» verso `#contatti` (primo link nel codice, mostrato a destra).
2. **Apertura**: label `// AI per chi lavora, anche senza codice`, promessa approvata «Faccio lavorare gli agenti AI su problemi veri. Ti mostro cosa funziona, anche se non programmi.», due azioni (profilo Instagram, poi `#esperimenti`) e nota «se disponibile» sul pulsante «Messaggio». A destra il quadro «Come lavoro»: ritratto, quattro passaggi (richiesta, agenti, controllo, verdetto) e i chip Sì / Dipende / No.
3. **Frase di fondo** su Paper: «Non devi saper programmare. Devi capirne abbastanza.»
4. **Metodo**: tre domande (cosa conta, come funziona, cosa farne) in tre colonne.
5. **Vale il tuo tempo?** (`#verdetti`, su pannello): quattro domande con verdetto e limite.
6. **Progetti** (`#esperimenti`, su Paper): schede Strumentini.it e DichiarazioniPubbliche.it con i loro marchi reali, link a GitHub.
7. **Chi sono** (`#chi-sono`): presentazione personale e link ai video su Instagram.
8. **Contatto** (`#contatti`, campitura Signal): invito a raccontare un compito ripetitivo, pulsante verso il profilo Instagram.
9. **Piè di pagina**: wordmark, Instagram (`footer-contact`), GitHub, torna su.

Sotto 900 px le colonne diventano una sequenza; sotto 640 px il menu mostra solo «Scrivimi» e i pulsanti occupano tutta la larghezza; sotto 350 px wordmark e pulsante si stringono, senza nascondere il contatto.

## Interazione e movimento

- Entrata dell'apertura: gli elementi salgono di 18 px in dissolvenza, a scaglioni di circa 60 ms; il quadro «Come lavoro» sale insieme con 0,2 s di ritardo.
- Quadro «Come lavoro»: i quattro passaggi si accendono a turno, un ciclo ogni 10 s (2,5 s ciascuno); il ciclo si ferma con il puntatore sopra il quadro.
- Verdetti: `<details name="verdetto">` nativi ed esclusivi, aprirne uno chiude l'altro, il primo è aperto al caricamento; il «+» ruota in «×», nessun JavaScript.
- Schede progetto: al passaggio salgono di 4 px con ombra e sottolineatura Signal crescente; i pulsanti salgono di 2 px.
- Focus visibile con contorno Signal Bright (bianco sulla fascia contatti).
- Con `prefers-reduced-motion: reduce` animazioni, transizioni e scorrimento morbido sono spenti e i quattro passaggi restano tutti accesi.

## Immagine di condivisione

`site/share.png`, 1200×630 px, referenziata da `og:image`: fondo Carbon, label mono Signal Bright, promessa in Archivo bianca con «problemi veri.» in Signal Bright, wordmark e dominio in basso. Nessuna foto.

## Verificato dai test

`tests/test_pages_artifact.py`, eseguito dalla CI prima del deploy: file pubblicati esatti; promessa e payoff presenti; sezioni e ancore; quattro verdetti con uno solo aperto; link Instagram e progetti; ritratto con testo alternativo; nessuna email né form; nessun font remoto o richiesta di terzi; ogni riferimento locale esiste; font WOFF2 e PNG validi; token uguali al canone; contrasti WCAG (4,5:1 per il testo, 3:1 per Signal su Paper solo testo grande); rotte servite in HTTP e file del repository non pubblicati.

## Limiti noti

- Il ritratto è la foto profilo Instagram da 150×150 px (recuperata il 7 novembre dall'`og:image` del profilo pubblico), mostrata a 76 px. Con l'originale ad alta risoluzione si potrebbe usare un ritratto più grande.
- I contrasti sono verificati sui token, non su ogni coppia usata nel CSS.
