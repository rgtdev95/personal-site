/* Ron Systems AI: progressive enhancement only. Every page works without this file. */
(function () {
  "use strict";

  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)");

  /* Mobile menu */
  var toggle = document.querySelector(".menu-toggle");
  var nav = document.getElementById("site-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", String(open));
      toggle.querySelector("use").setAttribute("href", open ? "#i-close" : "#i-menu");
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && nav.classList.contains("is-open")) {
        nav.classList.remove("is-open");
        toggle.setAttribute("aria-expanded", "false");
        toggle.querySelector("use").setAttribute("href", "#i-menu");
        toggle.focus();
      }
    });
  }

  /* Process: dockets slide along the rail. */
  var process = document.querySelector("[data-process]");
  if (process) {
    var track = process.querySelector("[data-track]");
    var prev = process.querySelector("[data-prev]");
    var next = process.querySelector("[data-next]");
    var step = function () {
      var item = track.querySelector("li");
      return item ? item.getBoundingClientRect().width + 24 : 320;
    };
    var sync = function () {
      prev.disabled = track.scrollLeft <= 4;
      next.disabled = track.scrollLeft + track.clientWidth >= track.scrollWidth - 4;
    };
    prev.addEventListener("click", function () { track.scrollBy({ left: -step(), behavior: reduced.matches ? "auto" : "smooth" }); });
    next.addEventListener("click", function () { track.scrollBy({ left: step(), behavior: reduced.matches ? "auto" : "smooth" }); });
    track.addEventListener("scroll", sync, { passive: true });
    window.addEventListener("resize", sync);
    sync();
  }
})();
