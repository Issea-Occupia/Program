/**
 * cursor.js — 按下即可持续喷射（无需鼠标移动）
 * ✅ 全局生效 + Stellar PJAX 支持
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

  // 状态
  const particles = [];
  let pressed = false;
  let mouseX = 0, mouseY = 0;

  const G = 0.045;
  const FRICTION = 0.993;

  // ✅ 随机亮色（避免黑灰）
  function randomBrightColor() {
    const h = Math.random() * 360;
    const s = 60 + Math.random() * 35;
    const l = 60 + Math.random() * 30;
    return `hsl(${h} ${s}% ${l}%)`;
  }

  function spawn(x, y) {
    particles.push({
      x,
      y,
      vx: (Math.random() - 0.5) * 3,
      vy: (Math.random() - 0.5) * 3,
      size: 2.8 + Math.random() * 2.5,
      life: 1.25,
      color: randomBrightColor()
    });
  }

  // ✅ 只负责更新坐标
  document.addEventListener("pointermove", e => {
    mouseX = e.clientX;
    mouseY = e.clientY;
  });

  // ✅ 按下开始喷射
  document.addEventListener("pointerdown", e => {
    pressed = true;
    mouseX = e.clientX;
    mouseY = e.clientY;
    spawn(mouseX, mouseY); // 当下立即喷一颗
  });

  // ✅ 松开停止喷射
  document.addEventListener("pointerup", () => pressed = false);
  document.addEventListener("pointerleave", () => pressed = false);

  // ✅ 动画循环
  function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // ✅ 连续喷射逻辑：只看 pressed
    if (pressed) spawn(mouseX, mouseY);

    for (let i = particles.length - 1; i >= 0; i--) {
      const p = particles[i];

      p.vy += G;
      p.x += p.vx;
      p.y += p.vy;

      p.vx *= FRICTION;
      p.vy *= FRICTION;

      // 屏幕反弹
      if (p.x < 0 || p.x > canvas.width) p.vx *= -1;
      if (p.y < 0 || p.y > canvas.height) p.vy *= -1;

      p.life -= 0.011;
      if (p.life <= 0) {
        particles.splice(i, 1);
        continue;
      }

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
