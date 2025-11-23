/**
 * FlipController
 * 完整满足以下需求：
 * - 单向旋转（角度累积：180 → 360 → 540…）
 * - 不可中断（动画锁）
 * - 旋转结束后再判断鼠标是否在区域
 * - 正→背→正→背 顺序视觉翻转
 */

document.addEventListener("DOMContentLoaded", () => {
  const cards = document.querySelectorAll(".flip-card");

  cards.forEach(card => {
    let angle = 0;               // 单向累积角度
    let isBack = false;          // 当前是否显示背面
    let locked = false;          // 动画锁
    let hover = false;           // 鼠标是否在区域

    const inner = card.querySelector(".flip-card-inner");

    /** 触发一次翻转 */
    function flipOnce() {
      if (locked) return;         // 正在旋转，不能打断
      locked = true;              // 上锁

      angle += 180;               // 单向累积旋转
      inner.style.transform = `rotateY(${angle}deg)`;

      // 动画结束后解锁，并检查下一步
      setTimeout(() => {
        locked = false;
        isBack = !isBack;

        // 根据你的规则判断是否要继续旋转
        checkNext();
      }, 600);
    }

    /** 根据你的逻辑决定是否执行下一次翻转 */
    function checkNext() {
      if (hover) {
        // 鼠标在区域
        if (!isBack) flipOnce();      // 正面 → 翻转
      } else {
        // 鼠标不在区域
        if (isBack) flipOnce();       // 背面 → 翻回
      }
    }

    /** 监听鼠标动作 */
    card.addEventListener("mouseenter", () => {
      hover = true;
      checkNext();
    });

    card.addEventListener("mouseleave", () => {
      hover = false;
      checkNext();
    });
  });
});
