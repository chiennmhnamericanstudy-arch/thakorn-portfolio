import { RescueMission, RULES, distance } from './drone-mission.js';

const byId = id => document.getElementById(id);
const canvas = byId('rescue-canvas');
const ctx = canvas.getContext('2d');
const root = byId('rescue-game');
const overlay = byId('game-overlay');
const startButton = byId('game-start');
const restartButton = byId('game-restart');
const dropButton = byId('game-drop');
const pauseButton = byId('game-pause');
const directionButtons = [...root.querySelectorAll('[data-flight]')];
const keyDirections = { ArrowUp: 'up', w: 'up', ArrowDown: 'down', s: 'down', ArrowLeft: 'left', a: 'left', ArrowRight: 'right', d: 'right' };
const keys = new Set();
const pointers = new Map();
const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
let mission = new RescueMission({ tall: window.matchMedia('(max-width: 650px)').matches });
let raf = 0, lastTime = 0, accumulator = 0;
let view = { width: 900, height: 560, scale: 1, x: 0, y: 0 };

function setStatus(text) {
  if (byId('game-status').textContent !== text) byId('game-status').textContent = text;
}
function clearInput() {
  keys.clear(); pointers.clear();
  directionButtons.forEach(b => b.classList.remove('is-held'));
}
function input() {
  const held = new Set([...keys].map(k => keyDirections[k]).concat([...pointers.values()]));
  return { x: Number(held.has('right')) - Number(held.has('left')), y: Number(held.has('down')) - Number(held.has('up')) };
}
function updateHUD() {
  root.dataset.phase = mission.phase;
  const seconds = Math.ceil(mission.remaining);
  byId('game-time').textContent = `${String(Math.floor(seconds / 60)).padStart(2, '0')}:${String(seconds % 60).padStart(2, '0')}`;
  byId('game-time').classList.toggle('is-urgent', seconds <= 15);
  byId('game-rescued').innerHTML = `${mission.rescued} <small>/ 3</small>`;
  byId('game-rings').textContent = mission.rings;
  byId('game-collisions').textContent = mission.collisions;
  const wind = mission.wind;
  const bearing = Math.abs(wind.x) > Math.abs(wind.y) ? (wind.x > 0 ? 'east →' : 'west ←') : (wind.y > 0 ? 'south ↓' : 'north ↑');
  byId('game-wind').textContent = `Light wind: ${bearing}`;
  dropButton.disabled = mission.phase !== 'playing' || !mission.rings;
  pauseButton.disabled = mission.phase !== 'playing';
  directionButtons.forEach(b => { b.disabled = mission.phase !== 'playing'; });
}
function overlayContent(label, title, description, action) {
  byId('overlay-label').textContent = label;
  byId('overlay-title').textContent = title;
  byId('overlay-description').textContent = description;
  startButton.textContent = action;
  overlay.hidden = false;
}
function showResults() {
  clearInput();
  const score = mission.score();
  const complete = mission.reason === 'complete';
  overlayContent(
    `${mission.rescued} of 3 swimmers assisted`,
    complete ? 'Support delivered.' : (mission.reason === 'time' ? 'Time to return.' : 'All rings deployed.'),
    complete ? 'You practiced the search, approach, and support sequence that inspired my rescue-drone project.' : 'Scan, approach, then release. These decisions also connect to my rescue-drone project. Try a steadier approach next time.',
    'Fly again'
  );
  const results = byId('game-results');
  results.hidden = false;
  byId('game-project-link').hidden = false;
  results.innerHTML = `<p class="simulator-result-total">${score.total}<span>points</span></p><dl class="simulator-result-breakdown"><div><dt>Support</dt><dd>+${score.assistance}</dd></div><div><dt>Accuracy</dt><dd>+${score.accuracy}</dd></div><div><dt>Time</dt><dd>+${score.time}</dd></div><div><dt>Collisions</dt><dd>−${score.penalty}</dd></div></dl>`;
  restartButton.hidden = true;
  setStatus(`Mission ended. ${mission.rescued} of 3 assisted. Score: ${score.total}. Fly again or explore the real drone project below.`);
  updateHUD();
  startButton.focus({ preventScroll: true });
}
function pause(moveFocus = true) {
  if (mission.phase !== 'playing') return;
  mission.pause(); clearInput();
  cancelAnimationFrame(raf); raf = 0;
  overlayContent('Flight paused', 'Take your time.', 'Your remaining time and progress are saved for this round.', 'Resume flight');
  restartButton.hidden = false;
  setStatus('Mission paused. Resume when you are ready.');
  updateHUD(); render();
  if (moveFocus) startButton.focus({ preventScroll: true });
}
function launch(fresh = false) {
  if (fresh || mission.phase === 'finished' || mission.phase === 'ready') {
    mission = new RescueMission({ tall: window.matchMedia('(max-width: 650px)').matches });
    mission.start();
    setStatus('Takeoff. Fly to A, B, or C and hold near the marker to scan.');
  } else if (mission.phase === 'paused') {
    mission.resume(); setStatus('Flight resumed. Continue searching and delivering rings.');
  } else return;
  clearInput();
  overlay.hidden = true;
  byId('game-results').hidden = true;
  byId('game-project-link').hidden = true;
  restartButton.hidden = true;
  updateHUD(); resize();
  canvas.focus({ preventScroll: true });
  lastTime = performance.now(); accumulator = 0;
  cancelAnimationFrame(raf);
  raf = requestAnimationFrame(frame);
}
function releaseRing() {
  if (mission.drop()) {
    for (const message of mission.events.splice(0)) setStatus(message);
    updateHUD();
  }
}

// All keyboard handling is scoped to the flight console, so normal page scrolling
// and the main navigation continue to work outside a running, focused mission.
root.addEventListener('keydown', event => {
  if (event.ctrlKey || event.metaKey || event.altKey) return;
  const key = event.key.length === 1 ? event.key.toLowerCase() : event.key;
  if (mission.phase === 'playing' && (key === 'p' || key === 'Escape')) {
    event.preventDefault(); pause(); return;
  }
  if (mission.phase === 'playing' && keyDirections[key]) {
    event.preventDefault(); keys.add(key); return;
  }
  if (mission.phase === 'playing' && event.code === 'Space' && event.target === canvas) {
    event.preventDefault(); if (!event.repeat) releaseRing(); return;
  }
  if (mission.phase === 'paused' && key === 'p' && !event.repeat) { event.preventDefault(); launch(); }
});
window.addEventListener('keyup', event => keys.delete(event.key.length === 1 ? event.key.toLowerCase() : event.key));
window.addEventListener('blur', () => pause(false));
document.addEventListener('visibilitychange', () => { if (document.hidden) pause(false); });
root.addEventListener('focusout', event => {
  if (!root.contains(event.relatedTarget)) { clearInput(); if (mission.phase === 'playing') pause(false); }
});

for (const button of directionButtons) {
  button.addEventListener('pointerdown', event => {
    if (mission.phase !== 'playing' || (event.pointerType === 'mouse' && event.button !== 0)) return;
    event.preventDefault();
    button.setPointerCapture(event.pointerId);
    pointers.set(event.pointerId, button.dataset.flight);
    button.classList.add('is-held');
  });
  const release = event => {
    pointers.delete(event.pointerId);
    if (![...pointers.values()].includes(button.dataset.flight)) button.classList.remove('is-held');
  };
  button.addEventListener('pointerup', release);
  button.addEventListener('pointercancel', release);
  button.addEventListener('lostpointercapture', release);
  button.addEventListener('contextmenu', event => event.preventDefault());
}
dropButton.addEventListener('click', releaseRing);
pauseButton.addEventListener('click', () => pause());
startButton.addEventListener('click', () => launch());
restartButton.addEventListener('click', () => launch(true));

function circle(x, y, radius, fill, stroke, width = 1) {
  ctx.beginPath(); ctx.arc(x, y, radius, 0, Math.PI * 2);
  if (fill) { ctx.fillStyle = fill; ctx.fill(); }
  if (stroke) { ctx.strokeStyle = stroke; ctx.lineWidth = width; ctx.stroke(); }
}
function line(x1, y1, x2, y2, color, width = 1) {
  ctx.beginPath(); ctx.moveTo(x1, y1); ctx.lineTo(x2, y2); ctx.strokeStyle = color; ctx.lineWidth = width; ctx.stroke();
}
function text(label, x, y, size = 18, color = '#d5edf4', align = 'center') {
  ctx.fillStyle = color;
  ctx.font = `500 ${Math.max(size, 10 / view.scale)}px "DM Sans", Arial, sans-serif`;
  ctx.textAlign = align; ctx.textBaseline = 'middle'; ctx.fillText(label, x, y);
}
function render() {
  if (!ctx) return;
  const ratio = Math.min(window.devicePixelRatio || 1, 2);
  ctx.setTransform(ratio, 0, 0, ratio, 0, 0);
  ctx.fillStyle = '#123c50'; ctx.fillRect(0, 0, view.width, view.height);
  ctx.translate(view.x, view.y); ctx.scale(view.scale, view.scale);
  const w = mission.width, h = mission.height;
  const ocean = ctx.createLinearGradient(0, 0, w, h);
  ocean.addColorStop(0, '#205b69'); ocean.addColorStop(1, '#0d3047');
  ctx.fillStyle = ocean; ctx.fillRect(0, 0, w, h);
  // A quiet navigational grid, coastline, and current strokes give spatial cues.
  for (let x = 0; x < w; x += 60) line(x, 0, x, h, '#bde6ef0c');
  for (let y = 0; y < h; y += 60) line(0, y, w, y, '#bde6ef0c');
  ctx.beginPath(); ctx.moveTo(0, 0); ctx.lineTo(50, 0); ctx.bezierCurveTo(4, h * .24, 66, h * .31, 30, h * .55); ctx.bezierCurveTo(0, h * .76, 57, h * .88, 25, h); ctx.lineTo(0, h); ctx.closePath(); ctx.fillStyle = '#9bbaad'; ctx.fill();
  for (let i = 0; i < 35; i++) {
    const x = 85 + (i * 127) % 790, y = 30 + (i * 67) % (h - 60);
    line(x, y, x + 13, y - 3, '#a0cbd12e', 1.5);
  }
  for (const o of mission.obstacles) {
    circle(o.x, o.y, o.radius + 23, '#142f4438', '#98b3b380', 1.5);
    ctx.beginPath();
    for (let i = 0; i < 9; i++) {
      const angle = i * Math.PI * 2 / 9, r = o.radius * (i % 2 ? .82 : 1);
      const x = o.x + Math.cos(angle) * r, y = o.y + Math.sin(angle) * r;
      if (!i) ctx.moveTo(x, y); else ctx.lineTo(x, y);
    }
    ctx.closePath(); ctx.fillStyle = '#63786f'; ctx.fill(); ctx.strokeStyle = '#94a99c'; ctx.lineWidth = 3; ctx.stroke();
    line(o.x - 10, o.y - 10, o.x + 10, o.y + 10, '#d2ded7', 2);
    line(o.x + 10, o.y - 10, o.x - 10, o.y + 10, '#d2ded7', 2);
  }
  for (const t of mission.targets) {
    if (t.rescued) {
      circle(t.x, t.y, 29, '#70e5c928', '#8bedcc', 3);
      line(t.x - 11, t.y, t.x - 3, t.y + 8, '#baffea', 4); line(t.x - 3, t.y + 8, t.x + 13, t.y - 10, '#baffea', 4);
      text(`${t.name} · assisted`, t.x, t.y + 50, 17, '#baffea');
      continue;
    }
    if (!t.found) {
      ctx.setLineDash([5, 7]); circle(t.x, t.y, RULES.scanRadius, '#9ae6e807', '#abdce879', 1.5); ctx.setLineDash([]);
      circle(t.x, t.y, 28, '#123c50', '#c0e4ed', 2);
      text(t.name, t.x, t.y, 23, '#e5f7fc');
      if (t.scan > 0) {
        ctx.beginPath(); ctx.arc(t.x, t.y, 35, -Math.PI / 2, -Math.PI / 2 + Math.PI * 2 * t.scan / RULES.scanTime); ctx.strokeStyle = '#88efe0'; ctx.lineWidth = 5; ctx.stroke();
        text('Scanning…', t.x, t.y + 57, 18, '#baffef');
      }
    } else {
      circle(t.x, t.y, RULES.hitRadius, '#ffdf8d0a', '#ffdf8d95', 1.5);
      circle(t.x, t.y - 10, 8, '#ffe4c2');
      line(t.x, t.y, t.x, t.y + 15, '#ffe4c2', 5);
      line(t.x - 18, t.y - 6, t.x, t.y + 4, '#ffe4c2', 4);
      line(t.x, t.y + 4, t.x + 17, t.y - 14, '#ffe4c2', 4);
      text(`Swimmer ${t.name}`, t.x, t.y + 60, 17, '#ffe4aa');
    }
  }
  for (const ring of mission.drops) {
    const progress = 1 - Math.max(0, ring.life) / RULES.dropTime;
    circle(ring.x, ring.y - (1 - progress) * 24, 8 + (1 - progress) * 8, null, '#ffde90', 5);
    circle(ring.x, ring.y, 4, '#ffeeb5');
  }
  for (const ripple of mission.ripples) circle(ripple.x, ripple.y, 14 + (1.3 - ripple.life) * 28, null, ripple.success ? '#9af2d6' : '#f9ca78', 2);

  const d = mission.drone;
  circle(d.x + 5, d.y + 10, 20, '#051c2c45');
  ctx.save(); ctx.translate(d.x, d.y); ctx.rotate(d.heading + Math.PI / 2);
  line(-18, -18, 18, 18, '#e9f7fb', 5); line(18, -18, -18, 18, '#e9f7fb', 5);
  for (const [x, y] of [[-20, -20], [20, -20], [-20, 20], [20, 20]]) {
    circle(x, y, 12, '#c5eff525', '#cdeef5', 2);
    const angle = reducedMotion.matches || mission.phase !== 'playing' ? .4 : mission.elapsed * 20;
    line(x - Math.cos(angle) * 9, y - Math.sin(angle) * 9, x + Math.cos(angle) * 9, y + Math.sin(angle) * 9, '#e9faff', 2);
  }
  ctx.fillStyle = mission.collisionCooldown > .4 ? '#ffc37b' : '#f3fcff'; ctx.fillRect(-8, -14, 16, 29);
  ctx.beginPath(); ctx.moveTo(0, -25); ctx.lineTo(-6, -15); ctx.lineTo(6, -15); ctx.closePath(); ctx.fillStyle = '#7ceadd'; ctx.fill();
  ctx.restore();
  // Keep the release crosshair above the aircraft so alignment stays readable.
  const aim = mission.aim;
  circle(aim.x, aim.y, 16, '#ffda8210', '#ffe095', 1.5);
  for (const [dx, dy] of [[1, 0], [-1, 0], [0, 1], [0, -1]]) line(aim.x + dx * 11, aim.y + dy * 11, aim.x + dx * 25, aim.y + dy * 25, '#ffe095', 2);
  if (mission.phase === 'playing') {
    const pending = mission.targets.filter(t => !t.rescued).sort((a, b) => distance(d, a) - distance(d, b))[0];
    if (pending && distance(d, pending) > 120) {
      const angle = Math.atan2(pending.y - d.y, pending.x - d.x);
      ctx.save(); ctx.translate(d.x + Math.cos(angle) * 59, d.y + Math.sin(angle) * 59); ctx.rotate(angle);
      ctx.beginPath(); ctx.moveTo(8, 0); ctx.lineTo(-4, -6); ctx.lineTo(-4, 6); ctx.closePath(); ctx.fillStyle = '#91ece1'; ctx.fill(); ctx.restore();
    }
  }
}
function resize() {
  const rect = canvas.getBoundingClientRect();
  if (!rect.width || !rect.height) return;
  const ratio = Math.min(window.devicePixelRatio || 1, 2);
  canvas.width = Math.round(rect.width * ratio); canvas.height = Math.round(rect.height * ratio);
  const scale = Math.min(rect.width / mission.width, rect.height / mission.height);
  view = { width: rect.width, height: rect.height, scale, x: (rect.width - mission.width * scale) / 2, y: (rect.height - mission.height * scale) / 2 };
  render();
}
let lastHUD = -1;
function frame(now) {
  raf = 0;
  if (mission.phase !== 'playing') return;
  accumulator += Math.min((now - lastTime) / 1000, .15); lastTime = now;
  while (accumulator >= 1 / 60 && mission.phase === 'playing') { mission.step(1 / 60, input()); accumulator -= 1 / 60; }
  const events = mission.events.splice(0);
  for (const message of events) setStatus(message);
  if (Math.floor(mission.elapsed * 5) !== lastHUD || events.length) { updateHUD(); lastHUD = Math.floor(mission.elapsed * 5); }
  render();
  if (mission.phase === 'finished') { showResults(); return; }
  raf = requestAnimationFrame(frame);
}

if (ctx) {
  startButton.disabled = false; startButton.textContent = 'Start rescue mission';
  byId('game-load-help').hidden = true;
  if ('ResizeObserver' in window) new ResizeObserver(resize).observe(canvas);
  else window.addEventListener('resize', resize);
  resize();
} else {
  byId('overlay-title').textContent = 'Flight controls unavailable';
  byId('overlay-description').textContent = 'This browser does not support the game canvas. Please try a recent browser, or explore the rescue-drone project below.';
  startButton.hidden = true;
}
