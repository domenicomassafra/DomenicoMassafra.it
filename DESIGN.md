# Direzione visiva del sito — «Officina cinetica», 14 novembre 2026

Stato: direzione unica, implementata in `site/` e pubblicata su autorizzazione dell'owner del 14/11/2026 («pubblica tutto online senza chiedere»). Sostituisce l'«Album delle prove» del 7–8 novembre e le tre proposte della PR #16.

## Audit della versione precedente (live fino al 14/11)

- **Cosa funzionava:** volto vero, contatto Instagram funzionante, due progetti apribili, nessun font remoto né JavaScript, `details` nativo, contrasto AA.
- **Cosa non funzionava:**
  - Il titolo «L'AI fa cose incredibili. Vediamo quali.» non era la promessa approvata il 28/10 («Faccio lavorare gli agenti AI su problemi veri. Ti mostro cosa funziona, anche se non programmi.»).
  - L'elemento interattivo chiesto dall'owner il 30/10 arrivava a metà pagina, con un solo esempio.
  - Il format proprietario «Vale il tuo tempo?» non compariva.
  - Il foglio «appunti» con le etichette decorative («APPUNTI / 001», «DM / 26») era rumore senza contenuto.
  - L'owner l'aveva definita transitoria (8/11).
- **Vincoli rispettati:** nessun cliente, metrica, guida o email inventati; foto 150×150 dal profilo Instagram pubblico, mostrata a grandezza nativa; nessun dato privato del vault.

## Perché questa direzione

Viene da quello che l'owner ha già deciso:

- **Fondo scuro:** richiesto l'8/11 e confermato nella scelta «Officina ribelle» del 30/10.
- **Volto reale e un elemento interattivo subito:** deciso il 30/10.
- **Ironia spontanea:** decisa il 30/10.
- **Ruolo «sperimentatore + spiegatore»:** deciso il 30/10.
- **Promessa e payoff:** approvati il 28/10 (`04-areas/divulgazione/brand/positioning-v2.md`).
- **Format «Vale il tuo tempo?»** con verdetto SÌ / DIPENDE / NO: già nel canone del brand.
- **Base visiva:** delle tre proposte dell'11/11 si sviluppa la A, «Officina cinetica», l'unica coerente con il fondo scuro richiesto.

## Sistema

- **Modo:** Persuade. Il visitatore capisce chi è Domenico, prova il format, apre un progetto o scrive.
- **Colori** (`site/styles.css`, `:root`):
  - fondo `#0d1114`, inchiostro crema `#f5f0e8`, testo secondario `#aea89e`;
  - accento arancio `#ff9b65` sul fondo scuro e `#a33c12` sulla crema;
  - fascia contatti `#3d1a0c`.
  - Il test calcola tutti i rapporti di contrasto WCAG: minimo 4,5:1.
- **Tipografia:**
  - titoli maiuscoli condensati con font di sistema (Impact, Avenir Next Condensed su Apple, Roboto Condensed su Android);
  - testo in `system-ui`;
  - nessun font remoto.
- **Composizione:**
  1. hero con promessa e ritratto in un arco arancio;
  2. subito dopo, «Vale il tuo tempo?» con tre domande apribili;
  3. fascia crema con il payoff;
  4. due progetti;
  5. chi sono;
  6. contatti.
  - Sotto gli 880 px tutto va in colonna.
- **Interazione:**
  - tre `details` nativi, che funzionano senza JavaScript e da tastiera;
  - focus arancio visibile;
  - `prefers-reduced-motion` toglie le transizioni e la rotazione.
- **Verità:** i verdetti sono dichiarati «opinioni mie dall'uso quotidiano, non il risultato di un test misurato».

## Verifiche

- `python3 -m unittest discover -s tests`: promessa, CTA, contatto, contrasti e file pubblici.
- Screenshot a 1440, 390 e 320 px senza scroll orizzontale.
- Prova sul sito pubblico dopo il deploy Pages.
