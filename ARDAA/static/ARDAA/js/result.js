document.addEventListener("DOMContentLoaded", () => {
  const atsScore = parseInt(document.querySelector(".inside-circle").innerText);
  const fills = document.querySelectorAll(".fill");

  let angle = (atsScore / 100) * 360;
  let i = 0;
  let current = 0;

  let interval = setInterval(() => {
    if (current >= angle) {
      clearInterval(interval);
    } else {
      current += 3; // speed of animation
      if (current <= 180) {
        fills[0].style.transform = `rotate(${current}deg)`;
      } else {
        fills[0].style.transform = `rotate(180deg)`;
        fills[1].style.transform = `rotate(${current - 180}deg)`;
      }
    }
  }, 15);
});
