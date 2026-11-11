# Issue #9 — audit e tre direzioni creative · 11 novembre 2026

**Stato:** proposta per scelta dell'owner, senza approvazione visuale e senza rilascio del redesign. Prototipo isolato sul branch `issue-9-brand-audit-20261111`; sorgenti di produzione in `site/` invariati. La scelta di CTA (contatto per problemi pratici con l'AI) è già stata fatta il 31 ottobre e viene rispettata in ogni direzione.

## 1. Baseline verificata

**Fatti riproducibili, 11/11:** `origin/main` = `3524b11bcfbd9d17ca8c8c6ee66c73bb2109322d`; il deploy [Pages 42589909836](https://github.com/domenicomassafra/DomenicoMassafra.it/actions/runs/42589909836) è `success` sullo stesso SHA. `https://domenicomassafra.it/` risponde HTTP **200**. Sono identici byte per byte al checkout `main` tutti e cinque i file confrontati via HTTPS: `index.html`, `styles.css`, `ritratto-instagram.jpg`, `strumentini-mark.svg`, `dichiarazioni-mark.svg`; SHA-256 dell'HTML `438ee17cfe674fde012247691b9d222106a5705507080a585c0e3fab42d98b9d`. `python3 -m unittest discover -s tests -q` → **5/5 PASS**. Questa è prova del sito **attuale**; non prova la qualità estetica del redesign futuro.

**Ciò che il sito già fa:** nome e profilo reale, una promessa comprensibile, CTA funzionante verso il profilo Instagram verificato, due progetti raggiungibili, la spiegazione degli esperimenti e il loro limite, link a GitHub, HTML statico su Pages, comportamento `details` e riduzione del movimento. Nessun font remoto né JavaScript della homepage; l'azione principale può richiedere il pulsante «Messaggio» su Instagram e un login del visitatore.

**Limiti visibili e mismatch:**

- L'owner ha respinto il redesign del 2 novembre; il tema scuro dell'8 novembre è esplicitamente transitorio. Migliorare margini e colori di quella stessa struttura non risolve il giudizio.
- Il volto è autentico ma il file disponibile misura **150×150 px**, pesa **5.841 byte** e non sostiene una hero fotografica grande o crop mobile diversi. Uno scatto originale approvato sblocca una direzione fotografica più forte.
- L'inizio parla soprattutto della pratica dell'AI, ma il carattere distintivo di Domenico (persona, ritmo, ironia spontanea) resta poco presente nell'esperienza. L'interazione «apri il verdetto» compare dopo le schede: la sorpresa iniziale richiesta non è ancora espressa.
- I progetti sono veri esperimenti personali, non lavori per clienti. Guide, download, moduli, email e casi con risultati misurati non sono attestati come pubblicati: non usarli come promesse o CTA attive.
- Il valore aggiunto oltre i Reel è ancora limitato: i collegamenti a Strumentini e DichiarazioniPubbliche sono reali, ma mancano una prova narrata completa con fonte/limite/verdetto o una guida editoriale pubblicabile e approvata.
- Mancano dati reali su traffico Instagram, conversioni o preferenza di stile: l'ipotesi che la maggior parte delle visite venga da Instagram resta **ipotesi**, non insight analytics.

**Autorità e fonti:** Area privata Obsidian `04-areas/divulgazione/brand/positioning-v2.md`, `BRAND.md`, `tone-of-voice.md` e hub `divulgazione-hub.md` per marca, pubblico e tono; `PRODUCT.md`, `DESIGN.md`, `site/`, issue #9 e i commenti owner 30/10, 31/10, 2/11, 8/11, 9/11 per le decisioni e il sito. Questo documento è un audit tecnico-creativo del repo, non una seconda fonte editoriale canonica.

## 2. Confronto fair play: copy, foto e CTA identici

In tutte le varianti: `Domenico Massafra`; headline **«Provo l'AI sul serio. Poi te la spiego semplice.»**; descrizione «Sono Domenico. Uso agenti e strumenti AI per affrontare problemi pratici, e racconto anche quello che non funziona.»; CTA «Raccontami un problema» verso il profilo Instagram esistente; secondaria «Guarda gli esperimenti»; foto `site/ritratto-instagram.jpg` a grandezza nativa; progetti Strumentini e DichiarazioniPubbliche verificabili. Headline e testi sono **copy proposto**, non contenuto approvato.

**Prototipo navigabile**: [HTML interattivo, confronto A/B/C](prototypes/issue-9-directions-20261111.html) (aprire il file dal checkout del branch e cambiare `?variant=a`, `b`, `c`, oppure usare i tasti freccia e i controlli in basso). È un prototipo eliminabile e marcato `noindex`; non è un percorso pubblico.

| Direzione | Mondo e composizione | Palette, font e contrasto campione | Interazione distintiva da realizzare dopo scelta | Compromesso reale |
|---|---|---|---|---|
| **A — Officina cinetica** | Poster culturale/manifesto di laboratorio, headline forte a sinistra e foto reale come badge centrale su sigillo a destra, in mobile l'interazione segue subito la CTA. Più spontanea e provocatoria, senza un personaggio artificiale. | Fondo `#0D1114`, testo `#F5F0E8`, accento arancio `#FF9B65`; headline Impact, corpo Avenir Next con fallback sans; contrasto testo/fondo **16,72:1**, accento/fondo **9,15:1**. | Un tassello «Cosa ho controllato?» può aprirsi con click/tap/Enter, mostrando prova e limite reali; piccoli movimenti parallax solo quando permessi. | Più memorabile ma tipografia aggressiva; per articoli lunghi servirà un registro editoriale calmo, e va calibrato il grado di irriverenza. |
| **B — Lettera dal laboratorio** | Copertina editoriale su carta, grande frase serif con foto e annotazione laterale; in mobile tutto diventa lettura verticale. Persona e spiegazione davanti all'effetto speciale. | Carta `#F3EBDD`, inchiostro `#241C18`, blu `#1749C9`; Georgia serif e Avenir Next per le azioni; contrasto corpo **14,14:1**, blu/carta **6,26:1**. | Note espandibili su fonte, errore e decisione, con `<details>` nativo e stato leggibile anche senza script. | Alta leggibilità e fiducia; rischia di somigliare troppo a un blog editoriale standard e dipende maggiormente da una fotografia originale ricca. |
| **C — Tavolo delle prove** | Tela modulare: slogan chiaro a sinistra, foto vera + metodo «Funziona?» + due progetti navigabili in una composizione asimmetrica. Mobile a tessere. | Petrolio `#112124`, testo `#F1F4EA`, citrino `#C4EC7B`; sistema sans; contrasto corpo **14,89:1**, accento/fondo **12,34:1**. | La tessera «Funziona?» apre un esempio con **prova → limite → verdetto** e fonte; il contenuto base resta disponibile senza animazione. | Mostra gli esperimenti subito, ma può comunicare «prodotto SaaS» anziché personal brand; evitare KPI, badge e metriche inventate. |

Gli esempi di rapporto di contrasto sopra sono calcolati sui colori indicati secondo WCAG per la coppia specifica, **non** certificano l'intera variante. La tipografia è locale, senza servizi remoti. Le sei PNG sono screenshot **renderizzati da Chrome headless** del prototipo HTML: desktop 1440×950 e mobile con CDP `Emulation.setDeviceMetricsOverride(width=390, height=844, mobile=true)`; in mobile il documento misurava `innerWidth=390` e `scrollWidth=390` per tutte e tre le varianti.

| Direzione | Desktop | Mobile |
|---|---|---|
| A | [Screenshot 1440 px](prototypes/issue-9-a-desktop-20261111.png) | [Screenshot 390 px](prototypes/issue-9-a-mobile-20261111.png) |
| B | [Screenshot 1440 px](prototypes/issue-9-b-desktop-20261111.png) | [Screenshot 390 px](prototypes/issue-9-b-mobile-20261111.png) |
| C | [Screenshot 1440 px](prototypes/issue-9-c-desktop-20261111.png) | [Screenshot 390 px](prototypes/issue-9-c-mobile-20261111.png) |

## 3. Voce e copy: esempi controllabili

**Voce:** uno sperimentatore che prova a costruire e uno spiegatore che rende utile quello che ha visto. Frasi in prima persona, precisione quando parla di prova e una battuta solo quando emerge naturalmente dal fatto. Rivolgersi a chi lavora e non è tecnico senza trattarlo da ingenuo. Usare uno dei due modi editoriali già scelti: notizia/spiegazione fondata su fonti esterne; esperienza diretta, con prova e limiti. Usare «ho provato» solo per un test personale attestato.

**Microcopy candidato:** «Hai un compito ripetitivo o un'idea da mettere alla prova? Raccontamelo.»; «Apri il progetto»; «Ecco dove si è fermato l'esperimento». Un tocco ironico collegato a un errore vero: «La demo sembrava perfetta. Poi ho provato il caso noioso.» Solo dopo che quel caso è realmente documentato. **Anti-esempi:** «Rivoluziono aziende con l'AI», «Automazioni infallibili», «100 clienti soddisfatti», «Ho testato tutto», «Download gratuito» senza risorsa approvata e raggiungibile. Evitare catchphrase seriali, linguaggio artificiale e personaggi/mascotte di terzi usati senza licenze.

## 4. Percorso interattivo, accessibilità e stack

Il gesto iniziale deve **mostrare qualcosa**: il visitatore sceglie una domanda concreta, vede «cosa controllo», «cosa non so», «dove vedere la prova». Ogni elemento resta un link, button o `<details>` nativo con focus visibile, click/tap/Enter/Space; le informazioni di base sono leggibili senza hover o audio. Movimento discreto e facoltativo; con `prefers-reduced-motion:reduce` elimina tilt e transizioni non necessarie. Un eventuale audio deve partire solo dopo attivazione consapevole e avere controlli e alternativa testuale. L'esempio storico «colpire Claude/Codex» non è una feature approvata: nessuna mascotte, logo o animazione di terzi nelle tre proposte.

**Stack candidato:** HTML/CSS statici, JavaScript progressivo solo dove l'interazione ha valore, GitHub Pages da `main`, immagini ottimizzate proprietarie e metadata Open Graph/canonical/sitemap/robots già presenti e da verificare. Prototipi in branch fuori da `main`. QA dopo scelta: a 320/390/768/1440 px nessun overflow, 200/asset bytes sul deploy, tastiera e focus, heading/landmark/alt, contrasto AA per tutti i token e stati, scansione Lighthouse + Web Vitals con misure reali, `prefers-reduced-motion`, touch e fallback senza JavaScript, link Instagram reale e rotte progetti. Nessuna misurazione Lighthouse o prova su screen reader fisico dichiarata in questo round.

## 5. Backlog di implementazione e dipendenze

1. **Decisione design owner**: scegliere A/B/C (o un ibrido specificando cosa prendere), scala dell'ironia e microinterazione; confermare o sostituire foto autentica e crop con file adatto e diritti chiari. Il nome, la promessa, il pubblico, i progetti reali e la CTA contatto restano dati già decisi.
2. **Brand e materiali editoriali**: far registrare la scelta nel canone Divulgazione attraverso il writer responsabile e ottenere approvazione di headline/testi. Per una guida o una storia, usare solo un contenuto già realmente verificato, con fonte e via di pubblicazione autorizzata. Dipende da (1).
3. **Implementazione completa in #9**: riscrivere struttura visiva in `site/` con font, foto, sezioni e microinterazione dell'opzione approvata; conservare i link funzionanti. Dipende da (1), con (2) per materiali editoriali che entrano nel sito.
4. **QA, merge e produzione**: unittest e controllo accessibilità/responsive/performance; CI su commit preciso; merge, GitHub Pages, confronto contenuti distribuiti e prova browser reale. Dipende da (3). Chiusura di #9 soltanto con accettazione owner e readback GitHub CLOSED.

Non vengono creati ticket implementativi separati prima della decisione: le quattro slice sono tracciate nella stessa issue che è il responsabile unico. Eventuali task incrociati (Strumentini #120, DichiarazioniPubbliche #349) hanno autorità indipendente, la sequenza resta coordinata dall'owner.

## 6. Frontier del grilling: una sola decisione necessaria ora

**Quale direzione parla davvero di Domenico?** A (energia e sorpresa), B (persona e calore), C (prove subito esplorabili), oppure un ibrido esplicito. **Parere motivato, non una decisione:** A dà più personalità alla prima visita e usa la foto reale senza ingrandirla artificialmente, a condizione di ammorbidire la tipografia nelle guide. B è più facile da leggere e C rende i progetti tangibili al primo sguardo. Dopo la scelta si decide il gesto preciso e la foto definitiva, evitando di far ripetere all'owner CTA, pubblico, naming e canali già approvati.

**Stato finale di questo round:** audit e mockup consegnabili; redesign pubblico non pubblicato; #9 resta OPEN in attesa della decisione creativa tramite coordinatore.
