/**
 * flip.js — Stellar PJAX 兼容最终版
 * 支持无刷新页面、不会重复绑定
 */

function initFlip() {
  const cards = document.querySelectorAll(".flip-card");
  if (!cards.length) return; // ✅ 当前页没有 flip-card 就退出

  cards.forEach(card => {
    let angle = 0;
    let locked = false;
    let hover = false;
    let isBack = false;
    const inner = card.querySelector(".flip-card-inner");
    if (!inner) return;

    function flipOnce() {
      if (locked) return;
      locked = true;

      angle += 180;
      inner.style.transform = `rotateY(${angle}deg)`;

      setTimeout(() => {
        locked = false;
        isBack = !isBack;
        checkNext();
      }, 600);
    }

    function checkNext() {
      if (hover && !isBack) flipOnce();
      else if (!hover && isBack) flipOnce();
    }

    card.addEventListener("mouseenter", () => {
      hover = true;
      checkNext();
    });

    card.addEventListener("mouseleave", () => {
      hover = false;
      checkNext();
    });
  });
}

// ✅ PJAX + 首次加载都执行
document.addEventListener("DOMContentLoaded", initFlip);
document.addEventListener("pjax:complete", initFlip);
