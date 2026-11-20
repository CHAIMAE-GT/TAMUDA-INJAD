/* TAMUDA INJAD – effets : ombre du header, bouton « haut de page », apparition au défilement. */
(function () {
  var d = document;
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var header = d.querySelector(".site-header");
  var topBtn = d.querySelector(".fab-top");
  function onScroll() {
    var y = window.scrollY;
    if (header) header.classList.toggle("scrolled", y > 10);
    if (topBtn) topBtn.classList.toggle("show", y > 600);
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();
  if (topBtn) topBtn.addEventListener("click", function () {
    window.scrollTo({ top: 0, behavior: reduce ? "auto" : "smooth" });
  });
  if (reduce || !("IntersectionObserver" in window)) return;
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (!e.isIntersecting) return;
      var el = e.target;
      io.unobserve(el);
      el.classList.add("in");
      setTimeout(function () { el.classList.remove("reveal", "in"); el.style.removeProperty("--d"); }, 1500);
    });
  }, { threshold: 0.12, rootMargin: "0px 0px -40px 0px" });
  var sel = "main .section h2, main .section .eyebrow, main .card, main .steps li, main details, main .chips li, main .notice, main .form, main .table-wrap";
  [].forEach.call(d.querySelectorAll(sel), function (el) {
    if (el.closest(".hero")) return;
    var i = [].indexOf.call(el.parentNode.children, el);
    el.style.setProperty("--d", Math.min(i, 6) * 0.08 + "s");
    el.classList.add("reveal");
    io.observe(el);
  });
})();