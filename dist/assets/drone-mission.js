// Deliberately simplified game rules; these values are not prototype measurements.
export const RULES = Object.freeze({ seconds: 75, rings: 8, scanRadius: 88, scanTime: .7, hitRadius: 42, dropTime: .65, collisionPenalty: 15 });
const clamp = (n, min, max) => Math.max(min, Math.min(max, n));
export const distance = (a, b) => Math.hypot(a.x - b.x, a.y - b.y);

export class RescueMission {
  constructor({ tall = false } = {}) {
    this.width = 900;
    this.height = tall ? 900 : 560;
    const point = (x, y) => ({ x, y: y * this.height / 560 });
    this.drone = { ...point(100, 440), vx: 0, vy: 0, heading: -.6 };
    this.targets = [[250, 125], [720, 155], [600, 440]].map(([x, y], i) => ({ ...point(x, y), name: 'ABC'[i], scan: 0, found: false, rescued: false, accuracy: 0 }));
    this.obstacles = [[285, 345, 46], [470, 215, 55], [750, 345, 42]].map(([x, y, radius]) => ({ ...point(x, y), radius }));
    this.phase = 'ready';
    this.elapsed = 0;
    this.rings = RULES.rings;
    this.collisions = 0;
    this.collisionCooldown = 0;
    this.dropCooldown = 0;
    this.drops = [];
    this.ripples = [];
    this.events = [];
    this.wind = { x: 15, y: 5 };
    this.reason = '';
  }
  get remaining() { return Math.max(0, RULES.seconds - this.elapsed); }
  get rescued() { return this.targets.filter(t => t.rescued).length; }
  get aim() { return { x: this.drone.x + this.wind.x * 1.2, y: this.drone.y + this.wind.y * 1.2 }; }
  start() { if (this.phase === 'ready') this.phase = 'playing'; }
  pause() { if (this.phase === 'playing') this.phase = 'paused'; }
  resume() { if (this.phase === 'paused') this.phase = 'playing'; }
  emit(text) { this.events.push(text); }
  finish(reason) { this.reason = reason; this.phase = 'finished'; }
  drop() {
    if (this.phase !== 'playing' || this.rings <= 0 || this.dropCooldown > 0) return false;
    this.rings--;
    this.dropCooldown = .7;
    this.drops.push({ ...this.aim, life: RULES.dropTime });
    this.emit('Ring released. Watch where it lands.');
    return true;
  }
  step(dt, input = { x: 0, y: 0 }) {
    if (this.phase !== 'playing' || !Number.isFinite(dt) || dt <= 0) return;
    dt = Math.min(dt, .05, this.remaining);
    this.elapsed += dt;
    this.collisionCooldown = Math.max(0, this.collisionCooldown - dt);
    this.dropCooldown = Math.max(0, this.dropCooldown - dt);
    this.wind = { x: 17 * Math.cos(this.elapsed / 9), y: 10 * Math.sin(this.elapsed / 7 + .5) };
    const length = Math.hypot(input.x, input.y);
    const ix = length > 1 ? input.x / length : input.x;
    const iy = length > 1 ? input.y / length : input.y;
    const d = this.drone;
    const response = 1 - Math.exp(-7 * dt);
    d.vx += (ix * 190 + this.wind.x - d.vx) * response;
    d.vy += (iy * 190 + this.wind.y - d.vy) * response;
    d.x += d.vx * dt;
    d.y += d.vy * dt;
    if (length > .1) d.heading = Math.atan2(iy, ix);
    d.x = clamp(d.x, 65, this.width - 26);
    d.y = clamp(d.y, 28, this.height - 28);
    for (const o of this.obstacles) {
      const gap = distance(d, o), radius = o.radius + 22;
      if (gap >= radius) continue;
      const nx = gap > .001 ? (d.x - o.x) / gap : 1;
      const ny = gap > .001 ? (d.y - o.y) / gap : 0;
      d.x = o.x + nx * (radius + 1);
      d.y = o.y + ny * (radius + 1);
      d.vx = nx * 70; d.vy = ny * 70;
      if (this.collisionCooldown <= 0) {
        this.collisions++;
        this.collisionCooldown = 1.2;
        this.emit('Obstacle contact. Give the rocky islands more space.');
      }
    }
    for (const t of this.targets) {
      if (t.found) continue;
      t.scan = distance(d, t) < RULES.scanRadius ? Math.min(RULES.scanTime, t.scan + dt) : Math.max(0, t.scan - dt);
      if (t.scan >= RULES.scanTime) {
        t.found = true;
        this.emit(`Swimmer ${t.name} identified. Align the yellow crosshair and release a ring.`);
      }
    }
    const landed = [];
    for (const ring of this.drops) {
      ring.life -= dt;
      if (ring.life <= 0) landed.push(ring);
    }
    this.drops = this.drops.filter(r => r.life > 0);
    for (const ring of landed) {
      const target = this.targets.find(t => t.found && !t.rescued && distance(t, ring) <= RULES.hitRadius);
      if (target) {
        target.rescued = true;
        target.accuracy = Math.round(100 * (1 - distance(target, ring) / RULES.hitRadius));
        this.emit(`Ring delivered to swimmer ${target.name}. ${this.rescued} of 3 assisted.`);
      } else {
        this.emit('Ring missed. Scan the swimmer first, then bring your crosshair closer.');
      }
      this.ripples.push({ x: ring.x, y: ring.y, life: 1.3, success: Boolean(target) });
    }
    this.ripples = this.ripples.filter(r => (r.life -= dt) > 0);
    if (this.rescued === 3) this.finish('complete');
    else if (this.remaining <= 0) this.finish('time');
    else if (!this.rings && !this.drops.length) this.finish('rings');
  }
  score() {
    const assistance = this.rescued * 100;
    const accuracy = this.targets.reduce((sum, t) => sum + t.accuracy, 0);
    const time = this.rescued === 3 ? Math.floor(this.remaining * 2) : 0;
    const penalty = this.collisions * RULES.collisionPenalty;
    return { assistance, accuracy, time, penalty, total: Math.max(0, assistance + accuracy + time - penalty) };
  }
}
