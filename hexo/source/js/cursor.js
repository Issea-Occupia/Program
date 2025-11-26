/**
 * cursor.js — 进阶物理粒子特效（Stellar / PJAX 全局可用）
 * ✅ 站点全局生效
 * ✅ 随机亮色粒子（排除黑暗色）
 * ✅ 含重力、反弹、摩擦、DOM 碰撞体
 * ✅ 性能友好（自动清理）
 */

let cursorInitialized = false;

function initCursor() {
  if (cursorInitialized) return;
  cursorInitialized = true;

  //---------------------------------------
  // Canvas
  //---------------------------------------
  const canvas = document.createElement("canvas");
  const ctx = canvas.getContext("2d");

  Object.assign(canvas.style, {
    position: "fixed",
    left: 0,
    top: 0,
    pointerEvents: "none",
    zIndex: 9999
  });

  document.body.appendChild(canvas);

  function resize() {
    canvas.width = window.innerWidth * devicePixelRatio;
    canvas.height = window.innerHeight * devicePixelRatio;
    ctx.scale(devicePixelRatio, devicePixelRatio);
  }
  resize();
  window.addEventListener("resize", resize);

  //---------------------------------------
  // 粒子状态
  //---------------------------------------
  const particles = [];
  const domBodies = [];
  const G = 0.1;          // ✅ 重力加速度
  const FRICTION = 0.995; // ✅ 空气阻力衰减

  //---------------------------------------
  // 随机亮色（排除黑色/灰色）
  //---------------------------------------
  function randomBrightColor() {
    let h = Math.random() * 360;       // 全色相
    let s = 60 + Math.random() * 40;   // 避免灰
    let l = 55 + Math.random() * 35;   // 保证亮度
    return `hsl(${h}, ${s}%, ${l}%)`;
  }

  //---------------------------------------
  // DOM 碰撞体收集
  //---------------------------------------
  function collectDomBodies() {
    domBodies.length = 0;

    document.querySelectorAll("img, .card, pre, figure, article, h1,h2,h3,h4,h5,h6")
      .forEach(el => {
        const r = el.getBoundingClientRect();
        domBodies.push({ x: r.left, y: r.top, w: r.width, h: r.height });
      });
  }

  //---------------------------------------
  // 粒子生成
  //---------------------------------------
  function spawn(x, y) {
    particles.push({
      x, y,
      vx: (Math.random() - 0.5) * 4,
      vy: (Math.random() - 0.5) * 4,
      size: 3 + Math.random() * 3,
      life: 1.2,
      color: randomBrightColor()
    });
  }

  //---------------------------------------
  // 鼠标
  //---------------------------------------
  document.addEventListener("pointermove", e => {
    spawn(e.clientX, e.clientY);
  });

  //---------------------------------------
  // 动画循环
  //---------------------------------------
  function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    collectDomBodies();

    for (let i = particles.length - 1; i >= 0; i--) {
      const p = particles[i];

      // ✅ 重力
      p.vy += G;

      // ✅ 移动
      p.x += p.vx;
      p.y += p.vy;

      // ✅ 阻尼
      p.vx *= FRICTION;
      p.vy *= FRICTION;

      // ✅ 边界反弹
      if (p.x < 0 || p.x > window.innerWidth)  p.vx *= -1;
      if (p.y < 0 || p.y > window.innerHeight) p.vy *= -1;

      // ✅ DOM 碰撞
      for (const b of domBodies) {
        if (
          p.x > b.x && p.x < b.x + b.w &&
          p.y > b.y && p.y < b.y + b.h
        ) {
          p.vx *= -1;
          p.vy *= -1.1;
        }
      }

      // ✅ 生命周期衰减
      p.life -= 0.01;
      if (p.life <= 0) {
        particles.splice(i, 1);
        continue;
      }

      // ✅ 绘制
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

// ✅ PJAX & 初次加载都执行
document.addEventListener("DOMContentLoaded", initCursor);
document.addEventListener("pjax:complete", initCursor);
