# Direzione visiva del sito — proposta eseguibile, 7 novembre 2026

Stato: candidata implementata sul branch #9. La preferenza estetica definitiva dell'owner deve ancora essere verificata.

## Perché il nuovo impianto

Il 2 novembre l'owner ha valutato la precedente homepage «pessima». La nuova versione segue il mandato successivo del 7 novembre di completare i siti. Si presenta come una pagina editoriale personale: Domenico è visibile in una fotografia autentica, il messaggio iniziale è verificabile e la prima azione invita a raccontare un problema concreto attraverso il contatto già funzionante.

## Identità e composizione

- **Modo:** Persuade, con voce da sperimentatore e spiegatore. Nessun immaginario di agenzia, cliente inventato o cruscotto finto.
- **Mondo:** foglio di appunti e album delle prove. Sfondo Paper #f6f2e9, inchiostro #182a30, Signal #a72f21 per leggibilità su superfici chiare, superfici a contrasto. I bordi separano sezioni e materiali; l'immagine reale occupa il foglio, affiancata da una nota.
- **Composizione:** titolo e azione immediati; ritratto autentico e nota a destra, poi due progetti pubblici, un piccolo verdetto apribile, spiegazione personale e contatto finale. A 800 px le colonne diventano sequenza verticale.
- **Tipografia:** sans leggibile per interfaccia e messaggio principale, serif soltanto per note e contrappunti. Nessun font remoto che rallenti o tracci il visitatore.
- **Interazione:** navigazione per ancore, HTML details nativo per il verdetto, focus ben visibile, hover leggero; nessun JavaScript di prodotto né audio automatico. La preferenza prefers-reduced-motion elimina il movimento evitabile.
- **Stati e canali:** l'unica CTA di contatto verificata apre il profilo Instagram; la disponibilità del pulsante «Messaggio» dipende dal profilo e dall'accesso del visitatore. Link progetto e codice sono secondari.

## Alternative valutate

1. **Lettera aperta** — pagina molto editoriale, fotografia protagonista, parole calde e gerarchia narrativa. Rischio: senza foto originale grande il cuore visivo perde forza; i progetti diventano troppo discreti.
2. **Album delle prove** — **implementazione candidata**. Ritratto vero in formato contenuto, voce personale, esperimenti raggiungibili, una microesperienza verificabile e percorso diretto al contatto. Rischio: avatar corrente da 150 px; sostituirlo con una foto originale prima di considerare definitiva l'identità.
3. **Rapporto di campo** — schede di verifica, note, limiti e confronti più espliciti. Rischio: per un pubblico non tecnico può sembrare un software o un registro tecnico anziché la homepage di una persona.

Il prototipo del 30 ottobre in docs/prototypes/issue-9-creative-directions.html rimane evidenza storica delle alternative precedenti; le scelte estetiche di quel round sono state superate dalla valutazione del 2 novembre.

Anteprime renderizzate del nuovo codice: [desktop](docs/prototypes/issue-9-new-desktop.png) e [mobile a 390 px](docs/prototypes/issue-9-new-mobile.png), generate da Chrome headless servendo la directory pubblica site/ via HTTP.

## Fonti e limiti

Fonti: decisioni owner in [issue #9](https://github.com/domenicomassafra/DomenicoMassafra.it/issues/9), e canone Obsidian 04-areas/divulgazione/brand/positioning-v2.md, BRAND.md, EXECUTION-SYSTEM.md. L'immagine site/ritratto-instagram.jpg deriva il 7 novembre dalla proprietà og:image del profilo pubblico https://www.instagram.com/domenico.massafraa/, verificato da title/description; risoluzione ricevuta 150×150, uso in piccolo formato e nessuna generazione sintetica. Nessun contenuto del vault è copiato come nuova fonte canonica.

I marchi site/strumentini-mark.svg e site/dichiarazioni-mark.svg sono copie esatte dei rispettivi favicon.svg pubblici dei due prodotti di Domenico, scaricati il 7 novembre; entrambe le immagini sono usate come elementi decorativi accanto ai link editoriali, senza creare nuovi simboli fittizi.

## Verifiche

Suite Python sul sito statico esatto pubblicato da GitHub Pages, link interni risolti, HTML/CSS esposti via HTTP, immagine disponibile, fallback del verdetto, supporto a reduced motion. Verifica visuale headless a 1440 px e verifica dell'assenza di overflow a 320/360/390/540/768 px prima del merge. Per il DONE del ticket resta il giudizio owner sulla nuova direzione e, se non è soddisfacente, la foto originale scelta.
