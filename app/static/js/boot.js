/* Runs before first paint so the hero can start in its unprinted state. */
document.documentElement.classList.add("js");
if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) document.documentElement.classList.add("rm");
