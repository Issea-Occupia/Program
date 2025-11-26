/**
 * cursor.js — 修复粒子不在鼠标尖端的最终版
 * ✅ 随机亮色粒子（排除黑色）
 * ✅ 重力 + DOM 碰撞
 * ✅ Stellar / PJAX 全局生效
 */

let cursorInitialized = false;

function initCursor() {
  if (cursorInitialized) return;
  cursorInitialized = true;

  // Canvas
  const canvas = document.createElement("canvas");
  const ctx = canvas.getContext("2d");

  Object.assign(canvas.style, {
    position: "fixed",
    left: "0",
    top: "0",
    pointerEvents: "none",
    zIndex: 9999
  });

  document.body.appendChild(canvas);

  function resize() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
  }
  resize();
  window.addEventListener("resize", resize);

  // 粒子系统
  const particles = [];
  const domBodies = [];
  const G = 0.12;
  const FRICTION = 0.992;

  function randomBrightColor() {
    let h = Math.random() * 360;
    let s = 65 + Math.random() * 35;
    let l = 55 + Math.random() * 35;
    return `hsl(${h} ${s}% ${l}%)`;
  }

  function collectDomBodies() {
    domBodies.length = 0;
    document
      .querySelectorAll("img, pre, code, figure, article, .card, h1,h2,h3,h4,h5,h6")
      .forEach(el => {
        const r = el.getBoundingClientRect();
        domBodies.push({ x: r.left, y: r.top, w: r.width, h: r.height });
      });
  }

  function spawn(x, y) {
    particles.push({
      x,
      y,
      vx: (Math.random() - 0.5) * 3,
      vy: (Math.random() - 0.5) * 3,
      size: 2.5 + Math.random() * 3.5,
      life: 1.3,
      color: randomBrightColor()
    });
  }

  document.addEventListener("pointermove", e => {
    spawn(e.clientX, e.clientY);
  });

  function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    collectDomBodies();

    for (let i = particles.length - 1; i >= 0; i--) {
      const p = particles[i];

      // gravity
      p.vy += G;

      // motion
      p.x += p.vx;
      p.y += p.vy;

      // friction
      p.vx *= FRICTION;
      p.vy *= FRICTION;

      // Screen boundary bounce
      if (p.x < 0 || p.x > canvas.width) p.vx *= -1;
      if (p.y < 0 || p.y > canvas.height) p.vy *= -1;

      // DOM collision
      for (const b of domBodies) {
        if (
          p.x > b.x && p.x < b.x + b.w &&
          p.y > b.y && p.y < b.y + b.h
        ) {
          p.vx *= -1;
          p.vy *= -1.15;
        }
      }

      // life decay
      p.life -= 0.013;
      if (p.life <= 0) {
        particles.splice(i, 1);
        continue;
      }

      // draw
      ctx.globalAlpha = p.life;
      ctx.fillStyle = p.color;
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
      ctx.fill();
    }

    requestAnimationFrame(animate);
  }

  animate();
}

document.addEventListener("DOMContentLoaded", initCursor);
document.addEventListener("pjax:complete", initCursor);
