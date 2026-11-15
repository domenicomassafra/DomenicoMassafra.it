// Interfaccia «chat»: legge le conversazioni scritte in index.html e ci costruisce sopra
// barra laterale, ricerca, risposte che si compongono e campo per scrivere.
// Senza questo script la pagina resta un elenco leggibile di domande e risposte.
(() => {
  const root = document.documentElement;
  const still = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const threads = [...document.querySelectorAll('.thread')];
  const byId = Object.fromEntries(threads.map((thread) => [thread.id, thread]));
  const list = document.querySelector('[data-threads]');
  const crumb = document.querySelector('[data-crumb]');
  const input = document.querySelector('[data-input]');
  const menu = document.querySelector('[data-menu]');
  const backdrop = document.querySelector('[data-close]');
  const search = document.querySelector('[data-search]');
  const played = new Set();
  let timers = [];
  let draft = '';

  const plain = (text) => text.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[^a-z0-9 ]+/g, ' ').replace(/\s+/g, ' ').trim();
  const title = (thread) => thread.querySelector('.ask').dataset.title;

  // Barra laterale: un gruppo per data-group, una voce per conversazione.
  let group = '';
  for (const thread of threads) {
    const ask = thread.querySelector('.ask');
    ask.dataset.title = ask.textContent;
    if (thread.dataset.group !== group) {
      group = thread.dataset.group;
      const heading = document.createElement('p');
      heading.textContent = group;
      list.append(heading);
    }
    const link = document.createElement('a');
    link.href = '#' + thread.id;
    link.dataset.words = plain(ask.textContent + ' ' + thread.dataset.keys);
    const name = document.createElement('span');
    name.textContent = ask.textContent;
    link.append(name);
    if (thread.dataset.badge) {
      const badge = document.createElement('b');
      badge.textContent = thread.dataset.badge;
      badge.className = 'badge badge-' + plain(thread.dataset.badge);
      link.append(badge);
    }
    list.append(link);
  }
  const links = [...list.querySelectorAll('a')];

  function drawer(open) {
    root.classList.toggle('nav-open', open);
    menu.setAttribute('aria-expanded', String(open));
    backdrop.hidden = !open;
  }

  // Una risposta si compone una sola volta; un tocco o un tasto la completa subito.
  function finish(thread) {
    timers.forEach(clearTimeout);
    timers = [];
    thread.classList.remove('playing');
    thread.querySelectorAll('.in').forEach((part) => part.classList.remove('in'));
    const summary = thread.querySelector('.run summary');
    summary.textContent = summary.dataset.done;
  }

  function play(thread) {
    const summary = thread.querySelector('.run summary');
    summary.dataset.done = summary.dataset.done || summary.textContent;
    if (still || played.has(thread.id)) return;
    played.add(thread.id);
    thread.classList.add('playing');
    const steps = [...thread.querySelectorAll('.run li')].map((step) => step.textContent);
    const parts = [...thread.querySelectorAll('.reply > *, .next')];
    let at = 250;
    steps.forEach((step) => {
      timers.push(setTimeout(() => { summary.textContent = step + '…'; }, at));
      at += 420;
    });
    timers.push(setTimeout(() => { summary.textContent = summary.dataset.done; }, at));
    parts.forEach((part) => {
      at += 130;
      timers.push(setTimeout(() => part.classList.add('in'), at));
    });
    timers.push(setTimeout(() => finish(thread), at + 700));
  }

  function open(id, message) {
    const thread = byId[id] || threads[0];
    const current = document.querySelector('.thread.is-open');
    if (current) finish(current);
    threads.forEach((item) => item.classList.toggle('is-open', item === thread));
    links.forEach((link) => link.toggleAttribute('aria-current', link.hash === '#' + thread.id));
    crumb.textContent = thread.dataset.group + ' / ' + title(thread);
    document.title = title(thread) + ' — Domenico Massafra';

    // Passaggio di mano: il messaggio del visitatore diventa la domanda della conversazione di contatto.
    const ask = byId.contatto.querySelector('[data-ask]');
    const handoff = byId.contatto.querySelector('[data-handoff]');
    draft = thread === byId.contatto && message ? message : '';
    ask.textContent = draft || ask.dataset.title;
    byId.contatto.classList.toggle('has-draft', Boolean(draft));
    handoff.firstChild.textContent = draft ? 'Copia il messaggio e apri Instagram ' : 'Scrivimi su Instagram ';
    const lead = byId.contatto.querySelector('[data-handoff-title]');
    lead.dataset.title = lead.dataset.title || lead.textContent;
    lead.textContent = draft ? 'Questa è da Domenico in persona.' : lead.dataset.title;
    const body = byId.contatto.querySelector('[data-handoff-text]');
    body.dataset.title = body.dataset.title || body.textContent;
    body.textContent = draft ? 'Te lo copio io: si apre il mio profilo Instagram, tocchi «Messaggio» e lo incolli. Ti rispondo io, non un bot.' : body.dataset.title;
    if (draft) played.delete('contatto');

    drawer(false);
    scrollTo(0, 0);
    play(thread);
  }

  // Scrivere: la risposta pronta più vicina, altrimenti la mano passa a Domenico.
  function match(text) {
    const words = ' ' + plain(text) + ' ';
    let best = null;
    let top = 0;
    for (const thread of threads) {
      const score = thread.dataset.keys.split(',').map(plain).filter((key) => key && words.includes(' ' + key + ' ')).reduce((sum, key) => sum + key.length, 0);
      if (score > top) { top = score; best = thread; }
    }
    return best;
  }

  function send() {
    const text = input.value.trim();
    if (!text) { input.focus(); return; }
    input.value = '';
    grow();
    // Un problema raccontato (testo lungo) va a Domenico, non a una risposta pronta.
    const found = text.length > 140 || text.split(/\s+/).length > 10 ? null : match(text);
    if (found && found !== byId.contatto) {
      if (location.hash === '#' + found.id) open(found.id); else location.hash = found.id;
    } else {
      history.replaceState(null, '', '#contatto');
      open('contatto', text);
    }
  }

  function grow() {
    input.style.height = 'auto';
    input.style.height = Math.min(input.scrollHeight, 180) + 'px';
  }

  function compose(text) {
    if (text !== undefined) input.value = text;
    grow();
    input.focus();
    const gap = input.value.indexOf('…');
    if (gap >= 0) input.setSelectionRange(gap, gap + 1);
  }

  addEventListener('hashchange', () => { const id = location.hash.slice(1); if (byId[id]) open(id); });
  document.addEventListener('pointerdown', (event) => {
    const playing = document.querySelector('.thread.playing');
    if (playing && !event.target.closest('a, button')) finish(playing);
  });

  input.addEventListener('input', grow);
  input.addEventListener('keydown', (event) => {
    if (event.key === 'Enter' && !event.shiftKey && !event.isComposing) { event.preventDefault(); send(); }
  });
  document.querySelector('[data-send]').addEventListener('click', send);
  document.querySelector('[data-new]').addEventListener('click', () => compose());

  document.addEventListener('click', (event) => {
    const template = event.target.closest('[data-template]');
    if (template) {
      document.getElementById('tracce').hidePopover();
      compose(template.dataset.template);
      return;
    }
    if (event.target.closest('[data-compose]')) {
      event.preventDefault();
      compose();
      return;
    }
    const handoff = event.target.closest('[data-handoff]');
    if (handoff && draft && navigator.clipboard) {
      navigator.clipboard.writeText(draft).then(() => {
        byId.contatto.querySelector('.fine').textContent = 'Messaggio copiato. Si apre il mio profilo: tocca «Messaggio», se disponibile, e incollalo.';
      }, () => {});
    }
  });

  menu.addEventListener('click', () => drawer(!root.classList.contains('nav-open')));
  backdrop.addEventListener('click', () => drawer(false));
  addEventListener('keydown', (event) => {
    if (event.key === 'Escape') drawer(false);
    if (event.key.toLowerCase() === 'k' && (event.metaKey || event.ctrlKey)) {
      event.preventDefault();
      drawer(true);
      search.focus();
    }
  });

  search.addEventListener('input', () => {
    const words = plain(search.value);
    links.forEach((link) => { link.hidden = Boolean(words) && !link.dataset.words.includes(words); });
  });
  search.addEventListener('keydown', (event) => {
    const first = links.find((link) => !link.hidden);
    if (event.key === 'Enter' && first) { search.value = ''; search.dispatchEvent(new Event('input')); first.click(); }
  });

  open(location.hash.slice(1));
})();
