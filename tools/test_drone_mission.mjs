import test from 'node:test';
import assert from 'node:assert/strict';
import { RescueMission, RULES, distance } from '../dist/assets/drone-mission.js';

function advance(mission, seconds, input = { x: 0, y: 0 }) {
  for (let i = 0; i < Math.ceil(seconds * 60); i++) mission.step(1 / 60, input);
}
function position(m, point) { Object.assign(m.drone, { x: point.x, y: point.y, vx: 0, vy: 0 }); }
function assist(m, target) {
  position(m, target);
  advance(m, .75);
  assert.equal(target.found, true);
  // Compensate for the currently displayed wind offset before release.
  position(m, { x: target.x - m.wind.x * 1.2, y: target.y - m.wind.y * 1.2 });
  assert.equal(m.drop(), true);
  advance(m, .75);
  assert.equal(target.rescued, true);
}

test('a complete round requires scanning, supports three accurate deliveries, and awards a time bonus', () => {
  for (const tall of [false, true]) {
    const m = new RescueMission({ tall }); m.start();
    m.targets.forEach(t => assist(m, t));
    assert.equal(m.phase, 'finished'); assert.equal(m.reason, 'complete');
    assert.equal(m.rings, 5);
    assert.equal(m.score().assistance, 300); assert.equal(m.score().accuracy, 300);
    assert.ok(m.score().time > 0 && m.score().time <= 150);
    assert.ok(m.score().total <= 750);
  }
});
test('unscanned swimmers cannot receive a ring and premature drops are limited by cooldown', () => {
  const m = new RescueMission(); m.start();
  const target = m.targets[0];
  position(m, { x: target.x - m.wind.x * 1.2, y: target.y - m.wind.y * 1.2 });
  assert.equal(m.drop(), true); assert.equal(m.drop(), false);
  advance(m, .66);
  assert.equal(target.found, false); assert.equal(target.rescued, false); assert.equal(m.rings, 7);
});
test('pausing freezes timer, flight, scanning, and in-flight rings; resuming continues them', () => {
  const m = new RescueMission(); m.start(); m.drop(); advance(m, .1); m.pause();
  const before = JSON.stringify(m); advance(m, 10, { x: 1, y: 1 });
  assert.equal(m.drop(), false); assert.equal(JSON.stringify(m), before);
  m.resume(); advance(m, 1, { x: 1, y: 0 });
  assert.equal(m.drops.length, 0); assert.ok(m.elapsed > 1); assert.ok(m.drone.x > 200);
});
test('a missed final ring ends the round only after it lands', () => {
  const m = new RescueMission(); m.start();
  for (let i = 0; i < RULES.rings - 1; i++) { m.drop(); advance(m, .75); }
  m.drop(); assert.equal(m.phase, 'playing'); assert.equal(m.rings, 0);
  advance(m, .75); assert.equal(m.phase, 'finished'); assert.equal(m.reason, 'rings');
  assert.equal(m.score().total, 0); assert.equal(m.drop(), false);
});
test('time expiration finishes an incomplete mission and further input changes nothing', () => {
  const m = new RescueMission(); m.start(); advance(m, 76);
  assert.equal(m.phase, 'finished'); assert.equal(m.reason, 'time'); assert.equal(m.remaining, 0);
  const before = JSON.stringify(m); advance(m, 1, { x: 1, y: 0 });
  assert.equal(JSON.stringify(m), before); assert.equal(m.score().time, 0);
});
test('obstacles resolve penetration and have a collision cooldown instead of per-frame penalties', () => {
  const m = new RescueMission(); m.start(); const o = m.obstacles[0];
  position(m, o); m.step(1 / 60);
  assert.equal(m.collisions, 1); assert.ok(distance(m.drone, o) >= o.radius + 22);
  for (let i = 0; i < 20; i++) { position(m, o); m.step(1 / 60); }
  assert.equal(m.collisions, 1); assert.equal(m.score().total, 0);
});
test('keyboard and diagonal input stay within the world and diagonal travel is normalized', () => {
  const cardinal = new RescueMission(), diagonal = new RescueMission();
  for (const m of [cardinal, diagonal]) { m.start(); position(m, { x: 100, y: 30 }); }
  advance(cardinal, .2, { x: 1, y: 0 }); advance(diagonal, .2, { x: 1, y: 1 });
  assert.ok(diagonal.drone.vx < cardinal.drone.vx);
  advance(cardinal, 20, { x: -1, y: -1 });
  assert.ok(cardinal.drone.x >= 65 && cardinal.drone.y >= 28);
});

test('a keyboard-driven route can finish both map layouts within one round without collisions', () => {
  for (const tall of [false, true]) {
    const m = new RescueMission({ tall }); m.start();
    const move = (x, y) => {
      const waypoint = { x, y: y * m.height / 560 };
      let frames = 0;
      while (distance(m.drone, waypoint) > 14 && frames++ < 1000) {
        const delta = { x: waypoint.x - m.drone.x, y: waypoint.y - m.drone.y };
        m.step(1 / 60, { x: Math.abs(delta.x) > 7 ? Math.sign(delta.x) : 0, y: Math.abs(delta.y) > 7 ? Math.sign(delta.y) : 0 });
      }
      assert.ok(frames < 1000, 'waypoint reachable');
    };
    const deliver = index => {
      advance(m, .75);
      assert.ok(m.targets[index].found);
      let frames = 0;
      while (distance(m.aim, m.targets[index]) > 18 && frames++ < 300) {
        const delta = { x: m.targets[index].x - m.aim.x, y: m.targets[index].y - m.aim.y };
        m.step(1 / 60, { x: Math.abs(delta.x) > 6 ? Math.sign(delta.x) : 0, y: Math.abs(delta.y) > 6 ? Math.sign(delta.y) : 0 });
      }
      assert.ok(frames < 300, 'drop can be aligned against wind');
      m.drop(); advance(m, .75);
      assert.ok(m.targets[index].rescued, 'ring reaches the scanned swimmer');
    };
    move(130, 150); move(250, 125); deliver(0);
    move(650, 70); move(720, 155); deliver(1);
    move(855, 300); move(855, 480); move(600, 440); deliver(2);
    assert.equal(m.reason, 'complete'); assert.equal(m.collisions, 0); assert.ok(m.remaining > 0);
  }
});
