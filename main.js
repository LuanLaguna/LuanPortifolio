(function () {
  const btn = document.querySelector(".nav-toggle");
  const nav = document.querySelector("#site-nav");
  if (!btn || !nav) return;

  btn.addEventListener("click", () => {
    const isOpen = nav.classList.toggle("is-open");
    btn.setAttribute("aria-expanded", String(isOpen));
  });

  nav.addEventListener("click", (e) => {
    if (e.target.tagName === "A" && nav.classList.contains("is-open")) {
      nav.classList.remove("is-open");
      btn.setAttribute("aria-expanded", "false");
    }
  });
})();