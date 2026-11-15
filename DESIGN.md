Mondo: Tabellone (Impeccable, seed:d77c7ff179f644ee)

# Sistema visivo del sito — «Tabellone», 15 novembre 2026

## Perché

Tre direzioni sono state bocciate dall'owner: la homepage del 2 novembre («pessima»), «Officina cinetica» il 14 novembre (arancione fuori palette, aspetto peggiore) e il 15 novembre il redesign della #18, che applicava il canone alla lettera ed è stato giudicato «troppo naif». Serviva un mondo davvero riconoscibile, senza uscire dal canone di marca. Redesign della issue #19 (brief completo lì), fatto con la skill Impeccable 4.9.1, percorso new-work, mondo visivo sostituito.

## Il mondo

Il tabellone partenze a palette delle stazioni italiane. Il mondo è stato scelto tra sette candidati presi dal mondo del pubblico; il seme ha assegnato il terzo. Ogni italiano lo conosce a memoria e porta il meccanismo senza gergo: un compito parte, lavora, arriva, e lo stato si stampa da solo sul tabellone. È nero con lettere bianche e un solo colore d'allarme, quindi coincide con Carbon, White e Signal del canone: nessun colore fuori palette. Evita sia la landing scura da prodotto AI con terminale finto sia il blog personale caldo. Discipline prese dalle alternative scartate:
1. Un solo elemento acceso in rosso per schermata: nel tabellone è accesa solo la prima riga (`.row-live`).
2. Una sola griglia di caratteri regge la composizione: le celle mono del tabellone.
3. Gli stati si stampano sul tabellone invece di comparire come decorazione; descrivono cose vere («in servizio», «aperto»).

## Colori

Token in `:root` di `site/styles.css`, con `color-scheme:dark`. Un test blocca ogni valore del canone diverso da questo.

| Token | Valore | Uso |
|---|---|---|
| `--carbon` | `#0b0b0d` | fondo pagina; testo su Paper e sul pulsante Signal Bright |
| `--panel` | `#151517` | corpo del tabellone, fascia dei verdetti |
| `--flap` | `#29292e` | fondo delle celle a palette; fondo della riga al passaggio |
| `--line` | `#2c2c30` | filetti su scuro, binario del metodo (decorazione) |
| `--paper` | `#f5f0e8` | barra «Partenze», frase di fondo, orario dei progetti, tessera |
| `--paper-line` | `#cfc7b8` | filetti su chiaro (decorazione) |
| `--white` | `#ffffff` | testo su scuro e su Signal, lettere delle palette |
| `--signal` | `#d63f28` | campitura del contatto, accenti grandi su Paper |
| `--signal-bright` | `#ff5a3c` | riga accesa, verdetto «No», parole chiave, pulsante principale, focus |
| `--ash` | `#9a948b` | testo secondario su scuro |
| `--graphite` | `#66615b` | testo secondario su chiaro |

## Tipografia

Font serviti dal sito, licenza SIL OFL in `site/fonts/OFL.txt`; nessuna richiesta a terzi.
- Archivo 400–800 (`site/fonts/archivo.woff2`) per tutte le frasi, in maiuscolo e minuscolo: titoli 700 con tracking negativo, testo 500–600.
- JetBrains Mono 700 (`site/fonts/jetbrains-mono.woff2`) solo nelle celle a palette e nelle label mono brevi (colonne del tabellone, «// limite», tessera). Il maiuscolo vive solo lì: il canone vieta le frasi tutte maiuscole.

## Struttura

1. **Intestazione** fissa su Carbon: wordmark «Domenico Massafra//», Verdetti, Progetti, Chi sono e il pulsante Paper «Scrivimi» verso `#contatti` (ultimo link del menu).
2. **Apertura**: promessa approvata come h1, frase di sostegno, due azioni (profilo Instagram, poi `#esperimenti`), nota «se disponibile». Sotto, `<nav class="board">`: barra Paper con «Partenze», orologio con l'ora del visitatore e interruttore del suono; cinque righe che sono la navigazione vera (binario, destinazione, cosa trovi, stato): il tuo problema, i verdetti, Strumentini.it, DichiarazioniPubbliche.it, chi sono.
3. **Frase di fondo** su Paper: «Non devi saper programmare. Devi capirne abbastanza.»
4. **Metodo**: una linea con tre fermate (cosa conta, come funziona, cosa farne).
5. **Vale il tuo tempo?** (`#verdetti`): quattro `<details name="verdetto">` esclusivi, il primo aperto; verdetto a palette grandi e limite.
6. **Progetti** (`#esperimenti`): orario stampato su Paper (`ul.timetable`) con i marchi reali e il link a GitHub.
7. **Chi sono** (`#chi-sono`): tessera personale (`.pass`) con il ritratto Instagram, studi, «Programmatore: No».
8. **Contatto** (`#contatti`) su campitura Signal, pulsante verso il profilo Instagram.
9. **Piè di pagina**: wordmark, Instagram, GitHub, torna su.

Sotto 900 px tutto va in colonna e le righe del tabellone si compattano; sotto 640 px il menu mostra solo «Scrivimi», i pulsanti occupano la larghezza e l'interruttore del suono sparisce; sotto 350 px wordmark e pulsante si stringono senza nascondere il contatto.

## Le palette

`site/board.js` (differito, senza dipendenze) trasforma ogni `[data-flap]` in celle, tiene il testo vero in uno span nascosto per i lettori di schermo e fa girare le celle. Le palette stanno in tre posti e solo lì, perché se sono troppe il sito diventa un giocattolo:
- **tabellone**: gli stati girano a cascata al caricamento e, al passaggio o al focus su una riga, mostrano la parola di `data-alt`;
- **barra**: orologio aggiornato ogni 15 secondi e interruttore del suono;
- **verdetti**: la parola Sì / Dipende / No gira ogni volta che una domanda si apre.

## Miglioramento progressivo

- Senza script: il testo di ogni `[data-flap]` è già nel sorgente e si legge in mono maiuscolo; il suono resta nascosto.
- Con `prefers-reduced-motion: reduce`: le celle mostrano subito la parola, animazioni e transizioni sono spente, la linea del metodo è piena, la tessera non è ruotata, il suono non compare.
- Dove `animation-timeline:view()` non è supportato la linea del metodo è mostrata piena; dove lo è si riempie con lo scorrimento.

## Suono

Spento di default. È sintetizzato con Web Audio (un breve rumore filtrato per ogni cella), senza file audio. L'`AudioContext` nasce solo al clic sull'interruttore; un secondo clic lo sospende.

## Verificato dai test

`tests/test_pages_artifact.py`, eseguito dalla CI prima del deploy: file pubblicati esatti (con `board.js`); promessa, payoff e sezioni; quattro verdetti con uno aperto; `board.js` caricato con `defer`; tabellone con cinque righe nell'ordine giusto e una sola accesa; ogni `[data-flap]` ha testo nel sorgente; suono nascosto e non premuto nel sorgente; script senza URL, rete, archiviazione, cookie, `eval` o `innerHTML`, con movimento ridotto e `AudioContext` creato solo nel clic (e `node --check` dove c'è Node); nessuna email né form; nessun font remoto; ogni riferimento locale e ogni icona `#freccia` esistono; token uguali al canone; contrasti WCAG, celle `--flap` comprese; rotte HTTP e file privati non pubblicati.

## Limiti noti

- Il ritratto è la foto profilo Instagram da 150×150 px (recuperata il 7 novembre), usata alla sua misura naturale sulla tessera. Con l'originale ad alta risoluzione si potrebbe ingrandire.
- I contrasti sono verificati sui token, non su ogni coppia usata nel CSS.
- `site/share.png` è ancora l'immagine di condivisione della #18 (Carbon, promessa in Archivo, nessuna foto).
