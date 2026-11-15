Mondo: Chat (direzione scelta dall'owner il 15/11/2026, riferimento T3 Code)

# Sistema visivo del sito — «Chat», issue #20

## Perché

In questo mese l'owner ha bocciato tre direzioni: «Officina cinetica» (14/11, arancione fuori palette), il redesign della #18 sul canone alla lettera («troppo naif») e il «Tabellone» della #19, il tabellone partenze a palette. Poi ha scelto lui: il sito come interfaccia di un'app di agenti AI, con la barra delle chat e «domande già risposte». Sue parole: «non scadere nel noioso, già visto», «figo ma che converta», «un'interfaccia che posso intercambiare, il copy, senza fare casino», «pensa all'architettura e alle scelte di UX e UI prima di tutto». Brief completo nella issue #20. Aspetto proprio, sui colori e i caratteri del canone, senza copiare la grafica di altri prodotti; dietro non c'è nessuna AI.

## Architettura: il contenuto sta nell'HTML

Ogni conversazione è un blocco `<article class="thread">` in `site/index.html`: domanda (`h2.ask`), passaggi dell'agente (`details.run`), risposta (`div.reply`), domande suggerite (`nav.next`). `site/app.js` legge quei blocchi e ci costruisce sopra barra laterale, gruppi, etichette, ricerca e campo per scrivere. Cosa ci guadagniamo:
- i testi si cambiano in un solo file, senza toccare lo script;
- ogni conversazione ha un indirizzo da condividere nei Reel (`domenicomassafra.it/#programmare`);
- senza script la pagina è un elenco leggibile di domande e risposte;
- i motori di ricerca leggono tutto il testo.

## Come cambiare i testi

Si lavora solo in `site/index.html`. Ogni conversazione inizia con `<article class="thread"` e finisce con `</article>`.
- **La domanda**: è il testo tra `<h2 class="ask">` e `</h2>`. Compare anche nella barra laterale.
- **La risposta**: sono i paragrafi dentro `<div class="reply">`. Cambia le frasi tra `<p>` e `</p>`; lascia com'è il resto.
- **I passaggi dell'agente**: le righe `<li>…</li>` dentro `<details class="run">`; `Ha lavorato per 3 s` è la riga che resta alla fine.
- **Il verdetto**: `data-badge="Sì"`, `"Dipende"` oppure `"No"` nella riga `<article …>` (l'etichetta nella barra), più la frase grande `<p class="verdict …">` nella risposta. Toglilo del tutto se la domanda non ha un verdetto.
- **Le frasi di ricerca**: `data-keys="…"`, frasi separate da virgole. Se un visitatore scrive una di queste frasi, il sito apre questa conversazione. Più la frase è lunga, più vince.
- **Il gruppo nella barra**: `data-group="…"`. Le conversazioni dello stesso gruppo vanno messe una dopo l'altra.
- **Aggiungere una conversazione**: copia un blocco intero da `<article` a `</article>`, incollalo dove vuoi che compaia, cambia `id="…"` con una parola nuova senza spazi (diventa l'indirizzo) e riscrivi i testi.
- **Le domande suggerite**: in `<nav class="next">`, ogni `<a href="#programmare">` porta alla conversazione con quell'`id`. Con `data-compose` il link apre invece il campo per scrivere.

Il test `test_every_conversation_is_complete_and_its_links_lead_somewhere` blocca la pubblicazione se un link suggerito punta a un `id` che non esiste, se due conversazioni hanno lo stesso `id`, se manca un pezzo o se un verdetto non è Sì, Dipende o No. La prima conversazione resta `chi-sono`, l'ultima `contatto`.

Limite da conoscere: il repository blocca i file oltre 20.000 byte e `site/index.html` è a circa 19.200. Con una o due conversazioni in più si arriva al limite: a quel punto si accorcia o si toglie una conversazione, oppure si chiede di spostare le conversazioni in più file. Le icone stanno in `site/icons.svg`.

## Colori

Token in `:root` di `site/styles.css`, con `color-scheme:dark`. Un test blocca ogni valore del canone diverso da questo.

| Token | Valore | Uso |
|---|---|---|
| `--carbon` | `#0b0b0d` | fondo pagina; testo su Paper e sul pulsante d'invio |
| `--panel` | `#131315` | barra laterale, campo per scrivere, schede dei progetti |
| `--raise` | `#202024` | bolla della domanda, voce attiva e passaggio del mouse, menu delle tracce |
| `--line` | `#2a2a2f` | filetti e bordi (decorazione) |
| `--paper` | `#f5f0e8` | testo principale; pulsanti e domanda «Ho un problema…»; etichetta «Sì» |
| `--white` | `#ffffff` | titoli, domanda, testo forte |
| `--signal` | `#d63f28` | sfondo della selezione del testo |
| `--signal-bright` | `#ff5a3c` | `//` del marchio, verdetto e etichetta «No», «// limite», pulsante d'invio, focus |
| `--ash` | `#9a948b` | testo secondario, verdetto «Dipende», label mono |
| `--graphite` | `#66615b` | pallino dei passaggi a riposo, bordi al focus, barra di scorrimento |

## Tipografia

Font serviti dal sito, licenza SIL OFL in `site/fonts/OFL.txt`; nessuna richiesta a terzi.
- Archivo 400–800 per tutte le frasi: promessa e verdetti 700 grandi con tracking negativo, testo 500–600.
- JetBrains Mono 700 solo per le label brevi (`// verdetto`, gruppi della barra, passaggi dell'agente, etichette Sì/Dipende/No, ⌘K). Il maiuscolo vive solo lì: il canone vieta le frasi tutte maiuscole.

## Impaginazione

- **Telefono (sotto 860 px)**: barra in alto con menu, marchio `Domenico Massafra //` (l'unico `h1`) e «nuova chat»; una conversazione; campo per scrivere fisso in basso, all'altezza del pollice. La barra delle chat scorre da sinistra sopra un velo scuro. Le domande suggerite stanno su una riga che scorre di lato. La prima schermata mostra nome, «Chi è Domenico Massafra?», la promessa in grande e le domande suggerite.
- **Da 860 px**: barra delle chat sempre aperta a sinistra (288 px), percorso «gruppo / domanda» in alto.
- **Da 1180 px**: pannello a destra (`aside.context`, 320 px) con il ritratto vero a 150 px, tre fatti (studi, «Programmatore: No», lavora con gli agenti), il payoff e il link ai video.

## Interazione

- **Una conversazione alla volta**, scelta dall'indirizzo (`#programmare`); senza indirizzo si apre `chi-sono`.
- **La risposta si compone una sola volta**: prima i passaggi dell'agente scorrono nella riga «Ha lavorato per…», poi i blocchi della risposta entrano uno dopo l'altro. Un tocco fuori da link e pulsanti la completa subito. Riaprendola è già pronta.
- **Scrivere**: il testo viene semplificato (minuscole, senza accenti né punteggiatura) e confrontato con le frasi `data-keys`; vince la conversazione con le frasi più lunghe trovate. Se non c'è nulla, o il testo è un problema raccontato (più di 10 parole o di 140 caratteri), si apre `contatto` con il messaggio del visitatore al posto della domanda: il pulsante lo copia negli appunti e apre il profilo Instagram.
- **Il «+»** apre un menu nativo (`popover`) con tre tracce di messaggio; scelta una, il campo si riempie con il primo «…» già selezionato, pronto da sostituire.
- **Barra delle chat**: sul telefono si apre con il menu e si chiude con il velo o Esc. La casella «Cerca» filtra le voci; ⌘K (Ctrl+K) la apre e ci mette il cursore; Invio apre la prima voce rimasta.

## Movimento e movimento ridotto

Domanda che compare con un piccolo rimbalzo, blocchi che entrano dal basso sfocati, pallino rosso che pulsa mentre l'agente «lavora», piccoli spostamenti al passaggio su pulsanti e schede. Con `prefers-reduced-motion: reduce` le risposte sono subito complete e animazioni e transizioni sono spente.

## Senza script

L'`<html>` nel sorgente non ha classi: è lo script in `<head>` ad aggiungere `app`. Senza, tutte le conversazioni sono una sotto l'altra e restano leggibili; barra delle chat, campo per scrivere e pulsanti di menu e nuova chat (classe `only-app`) sono nascosti.

## Cosa garantiscono i test

`tests/test_pages_artifact.py` e `tests/test_app_script.py` (lo script e lo smistamento dei messaggi), eseguiti dalla CI prima del deploy: file pubblicati esatti (con `app.js`, senza `board.js`); un solo `h1`; dieci conversazioni complete, con `id` unici, gruppi, frasi di ricerca, verdetti validi e domande suggerite che portano a conversazioni esistenti; `contatto` con il passaggio a Instagram; promessa, frase di sostegno, payoff, ritratto con il suo testo alternativo, link a Strumentini, DichiarazioniPubbliche e GitHub, «se disponibile»; nessuna email, form o link diretto ai messaggi di Instagram; pagina leggibile senza script; script senza rete, archiviazione, cookie, `eval` o `innerHTML`, con `node --check`; dove c'è Node, frasi vere di visitatori («quanto costa?», «chi sei», «privacy dei clienti», …) passate alla logica vera di `app.js` arrivano alla conversazione giusta; nessun font o file remoto, ogni file locale e ogni icona esistono; token uguali al canone; contrasti WCAG AA; rotte HTTP, `board.js` e file privati non pubblicati.

## Limiti noti

- Il ritratto è la foto profilo Instagram da 150×150 px (recuperata il 7 novembre), mostrata alla sua misura naturale. Con l'originale ad alta risoluzione si potrebbe ingrandire.
- Instagram non accetta un messaggio precompilato: il sito copia il testo e apre il profilo; il visitatore tocca «Messaggio», se disponibile, e incolla.
- La ricerca confronta frasi, non significati: una domanda scritta con parole diverse da quelle in `data-keys` passa la mano a Domenico.
- I contrasti sono verificati sui token, non su ogni coppia usata nel CSS.
- `site/share.png` è ancora l'immagine di condivisione della #18.
