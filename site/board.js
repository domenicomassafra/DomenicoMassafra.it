// Palette del tabellone: arricchisce [data-flap]; senza questo script il testo resta leggibile.
(() => {
  const still = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const GLYPHS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
  let audio = null;
  let lastClack = 0;

  function clack() {
    if (!audio || audio.currentTime - lastClack < 0.045) return;
    lastClack = audio.currentTime;
    const length = Math.floor(audio.sampleRate * 0.03);
    const buffer = audio.createBuffer(1, length, audio.sampleRate);
    const data = buffer.getChannelData(0);
    for (let i = 0; i < length; i++) data[i] = (Math.random() * 2 - 1) * (1 - i / length) ** 3;
    const source = audio.createBufferSource();
    const filter = audio.createBiquadFilter();
    const gain = audio.createGain();
    source.buffer = buffer;
    filter.type = 'bandpass';
    filter.frequency.value = 1500 + Math.random() * 700;
    gain.gain.value = 0.12;
    source.connect(filter).connect(gain).connect(audio.destination);
    source.start();
  }

  function build(el) {
    const text = el.textContent.trim();
    const size = Math.max(text.length, (el.dataset.alt || '').length);
    const spoken = document.createElement('span');
    spoken.className = 'sr-only';
    spoken.textContent = text;
    const cells = document.createElement('span');
    cells.className = 'flaps';
    cells.setAttribute('aria-hidden', 'true');
    for (let i = 0; i < size; i++) {
      const cell = document.createElement('span');
      cell.className = 'flap';
      cell.textContent = ' ';
      cells.append(cell);
    }
    el.dataset.flap = text;
    el.replaceChildren(spoken, cells);
  }

  function show(el, text, stagger = 45) {
    const run = (el.flapRun = (el.flapRun || 0) + 1);
    el.querySelectorAll('.flap').forEach((cell, index) => {
      const target = text[index] && text[index] !== ' ' ? text[index] : ' ';
      if (cell.textContent === target) return;
      if (still) { cell.textContent = target; return; }
      const steps = 2 + Math.floor(Math.random() * 4);
      for (let step = 0; step < steps; step++) {
        setTimeout(() => {
          if (el.flapRun !== run) return;
          cell.textContent = step === steps - 1 ? target : GLYPHS[Math.floor(Math.random() * GLYPHS.length)];
          cell.animate(
            [{ transform: 'perspective(140px) rotateX(-85deg)', filter: 'brightness(.45)' }, { transform: 'none', filter: 'none' }],
            { duration: 110, easing: 'cubic-bezier(.2,.8,.2,1)' }
          );
          clack();
        }, index * stagger + step * 75);
      }
    });
  }

  const flaps = [...document.querySelectorAll('[data-flap]')];
  flaps.forEach(build);

  // Tabellone: le righe girano a cascata all'apertura, poi rispondono a puntatore e tastiera.
  document.querySelectorAll('.board .row').forEach((row, index) => {
    const bin = row.querySelector('.bin');
    const state = row.querySelector('.state');
    setTimeout(() => { show(bin, bin.dataset.flap); show(state, state.dataset.flap); }, still ? 0 : 250 + index * 160);
    const swap = (text) => () => show(state, text, 25);
    row.addEventListener('pointerenter', swap(state.dataset.alt));
    row.addEventListener('focus', swap(state.dataset.alt));
    row.addEventListener('pointerleave', swap(state.dataset.flap));
    row.addEventListener('blur', swap(state.dataset.flap));
  });

  // Verdetti: la parola gira ogni volta che una domanda si apre.
  document.querySelectorAll('details[name="verdetto"]').forEach((item) => {
    const verdict = item.querySelector('.verdict');
    const spin = () => { show(verdict, '', 0); setTimeout(() => show(verdict, verdict.dataset.flap, 90), 60); };
    item.addEventListener('toggle', () => { if (item.open) spin(); });
    if (item.open) show(verdict, verdict.dataset.flap, 90);
  });

  // Orologio: l'ora vera del visitatore.
  const clock = document.querySelector('[data-clock]');
  if (clock) {
    const tick = () => {
      const now = new Date();
      const text = String(now.getHours()).padStart(2, '0') + ':' + String(now.getMinutes()).padStart(2, '0');
      clock.querySelector('.sr-only').textContent = text;
      show(clock, text);
    };
    tick();
    setInterval(tick, 15000);
  }

  // Suono: spento finché il visitatore non lo accende.
  const sound = document.querySelector('[data-sound]');
  const AudioContextClass = window.AudioContext || window.webkitAudioContext;
  if (sound && AudioContextClass && !still) {
    const label = sound.querySelector('[data-flap]');
    show(label, label.dataset.flap);
    label.querySelector('.sr-only').textContent = ''; // lo stato lo dice già aria-pressed
    sound.hidden = false;
    sound.addEventListener('click', () => {
      const on = sound.getAttribute('aria-pressed') !== 'true';
      sound.setAttribute('aria-pressed', String(on));
      if (on) { audio = audio || new AudioContextClass(); audio.resume(); } else if (audio) { audio.suspend(); }
      show(label, on ? label.dataset.alt : label.dataset.flap);
    });
  }
})();
