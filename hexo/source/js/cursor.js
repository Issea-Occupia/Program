/**
 * cursor.js v10 FINAL
 * - 内置 Physics Engine（粒子-粒子完全弹性 + 边界 + DOM 刚体）
 * - 生命周期独立控制（无闪烁）
 * - 所有 img、代码块、公式块、标题参与碰撞
 * - pointermove 修复（鼠标位置正确更新）
 */

document.addEventListener("DOMContentLoaded", () => {

  //---------------------------------------
  // 基础设置：禁用默认行为
  //---------------------------------------
  document.addEventListener("dragstart", e => e.preventDefault());
  document.addEventListener("selectstart", e => e.preventDefault());

  //---------------------------------------
  // Canvas
  //---------------------------------------
  const canvas = document.createElement("canvas");
  const ctx = canvas.getContext("2d");

  canvas.style.position = "fixed";
  canvas.style.left = "0";
  canvas.style.top = "0";
  canvas.style.pointerEvents = "none";
  canvas.style.zIndex = 9999;
  document.body.appendChild(canvas);

  function resize() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
  }
  resize();
  window.addEventListener("resize", resize);

  //---------------------------------------
  // 鼠标影子（可选）
  //---------------------------------------
  const shadow = document.createElement("div");
  shadow.id = "cursor-shadow";
  document.body.appendChild(shadow);

  //---------------------------------------
  // 状态变量
  //---------------------------------------
  let mouseX = 0, mouseY = 0;
  let pressed = false;
  const particles = [];
  const domBodies = [];

  //---------------------------------------
  // pointermove（你之前缺失的关键部分）
  //---------------------------------------
  document.addEventListener("pointermove", e => {
    mouseX = e.clientX;
    mouseY = e.clientY;

    // shadow 更新位置
    shadow.style.transform = `translate(${mouseX}px, ${mouseY}px)`;

    // 按住拖动时持续生成粒子
    if (pressed) spawnParticle(mouseX, mouseY, false);
  });

  document.addEventListener("pointerdown", () => pressed = true);
  document.addEventListener("pointerup",   () => pressed = false);
  window.addEventListener("mouseup",       () => pressed = false);

  //---------------------------------------
  // DOM 刚体收集
  //---------------------------------------
  function collectDomBodies() {
    domBodies.length = 0;

    // 1. 所有图片
    document.querySelectorAll("img").forEach(el => {
      const r = el.getBoundingClientRect();
      domBodies.push({ x: r.left, y: r.top, w: r.width, h: r.height });
    });

    // 2. 所有代码块
    document.querySelectorAll("pre, .highlight, .code-block, figure.highlight").forEach(el => {
      const r = el.getBoundingClientRect();
      domBodies.push({ x: r.left, y: r.top, w: r.width, h: r.height });
    });

    // 3. 公式块 (KaTeX / MathJax)
    document.querySelectorAll(".katex-display, .katex, .MathJax, .MathJax_Display").forEach(el => {
      const r = el.getBoundingClientRect();
      domBodies.push({ x: r.left, y: r.top, w: r.width, h: r.height });
    });

    // 4. 标题 h1~h6
    document.querySelectorAll("h1,h2,h3,h4,h5,h6").forEach(el => {
      const r = el.getBoundingClientRect();
      domBodies.push({ x: r.left, y: r.top, w: r.width, h: r.height });
    });
  }

  //---------------------------------------
  // 粒子生成
  //---------------------------------------
  function spawnParticle(x, y, strong) {
    particles.push({
      x, y,
      vx: (Math.random() - 0.5) * 2,
      vy: (Math.random() - 0.5) * 2,
      size: strong ? 6 : 4,
      life: strong ? 1.4 : 1.0,
      r: strong ? Math.random() * 255 : 255,
      g: strong ? Math.random() * 255 : 255,
      b: strong ? Math.random() * 255 : 255,
    });
  }

  //---------------------------------------
  // Physics Engine（原 physics.js）
  //---------------------------------------
  function updatePhysics() {
    const W = canvas.width;
    const H = canvas.height;
    const n = particles.length;

    // 粒子 - 粒子
    for (let i = 0; i < n; i++) {
      const A = particles[i];
      for (let j = i + 1; j < n; j++) {
        const B = particles[j];

        let dx = B.x - A.x;
        let dy = B.y - A.y;
        let dist = Math.sqrt(dx*dx + dy*dy);
        const minDist = A.size + B.size;

        if (dist === 0) dist = 0.0001;

        if (dist < minDist) {
          const nx = dx / dist;
          const ny = dy / dist;

          const rvx = B.vx - A.vx;
          const rvy = B.vy - A.vy;
          const relVel = rvx * nx + rvy * ny;

          if (relVel > 0) continue;

          const imp = -relVel;

          A.vx -= imp * nx;
          A.vy -= imp * ny;
          B.vx += imp * nx;
          B.vy += imp * ny;

          const overlap = (minDist - dist) / 2;
          A.x -= nx * overlap;
          A.y -= ny * overlap;
          B.x += nx * overlap;
          B.y += ny * overlap;
        }
      }
    }

    // 粒子 - DOM 矩形
    particles.forEach(p => {
      domBodies.forEach(b => {
        const closestX = clamp(p.x, b.x, b.x + b.w);
        const closestY = clamp(p.y, b.y, b.y + b.h);

        const dx = p.x - closestX;
        const dy = p.y - closestY;
        const distSq = dx*dx + dy*dy;

        if (distSq < p.size * p.size) {
          if (Math.abs(dx) > Math.abs(dy)) {
            p.vx *= -1;
            p.x = dx > 0 ? closestX + p.size : closestX - p.size;
          } else {
            p.vy *= -1;
            p.y = dy > 0 ? closestY + p.size : closestY - p.size;
          }
        }
      });
    });

    // 单粒子更新 + 边界
    particles.forEach(p => {
      p.x += p.vx;
      p.y += p.vy;
      p.vy += 0.015;

      if (p.x - p.size < 0) {
        p.x = p.size;
        p.vx *= -1;
      }
      if (p.x + p.size > W) {
        p.x = W - p.size;
        p.vx *= -1;
      }
      if (p.y - p.size < 0) {
        p.y = p.size;
        p.vy *= -1;
      }
      if (p.y + p.size > H) {
        p.y = H - p.size;
        p.vy *= -1;
      }
    });
  }

  function clamp(v, min, max) {
    return Math.max(min, Math.min(v, max));
  }

  //---------------------------------------
  // 主动画循环
  //---------------------------------------
  function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    if (pressed) spawnParticle(mouseX, mouseY, true);

    collectDomBodies();
    updatePhysics();

    for (let i = particles.length - 1; i >= 0; i--) {
      const p = particles[i];
      p.life -= 0.006;

      if (p.life <= 0) {
        particles.splice(i, 1);
        continue;
      }

      ctx.fillStyle = `rgba(${p.r},${p.g},${p.b},${p.life})`;
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.size, 0, Math.PI*2);
      ctx.fill();
    }

    requestAnimationFrame(animate);
  }

  animate();
});
