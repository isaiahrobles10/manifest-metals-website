/* Manifest Metals — site behavior */
(function () {
  document.documentElement.classList.add("js");

  // Header state on scroll + mobile call bar
  var header = document.querySelector(".site-header");
  var callbar = document.querySelector(".callbar");
  var onScroll = function () {
    var y = window.scrollY;
    if (header) header.classList.toggle("scrolled", y > 8);
    if (callbar) callbar.classList.toggle("show", y > 480);
  };
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  // Mobile menu
  var toggle = document.querySelector(".menu-toggle");
  var nav = document.getElementById("site-nav");
  if (toggle && nav) {
    var setOpen = function (open) {
      nav.classList.toggle("open", open);
      toggle.setAttribute("aria-expanded", String(open));
      document.body.classList.toggle("menu-open", open);
    };
    toggle.addEventListener("click", function () {
      setOpen(toggle.getAttribute("aria-expanded") !== "true");
    });
    nav.addEventListener("click", function (e) {
      if (e.target.closest("a")) setOpen(false);
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") setOpen(false);
    });
  }

  // Reveal on scroll
  var targets = document.querySelectorAll(".reveal, .bars");
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("in");
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12, rootMargin: "0px 0px -40px 0px" });
    targets.forEach(function (el) { io.observe(el); });
  } else {
    targets.forEach(function (el) { el.classList.add("in"); });
  }

  // Footer year
  var year = document.getElementById("year");
  if (year) year.textContent = new Date().getFullYear();

  // Roof color visualizer: crossfade between pre-rendered colors
  var stage = document.querySelector(".viz-stage");
  if (stage) {
    var label = stage.querySelector(".viz-name");
    var labelChip = stage.querySelector(".viz-label .chip");
    var swatches = document.querySelectorAll(".swatch");
    var preload = function (btn) {
      if (btn._img) return btn._img;
      var im = new Image();
      im.sizes = stage.querySelector("img").sizes;
      im.srcset = btn.getAttribute("data-srcset");
      im.src = btn.getAttribute("data-src");
      im.alt = stage.querySelector("img").alt;
      im.className = "viz-img fading";
      btn._img = im;
      return im;
    };
    swatches.forEach(function (btn) {
      btn.addEventListener("pointerenter", function () { preload(btn); });
      btn.addEventListener("click", function () {
        if (btn.classList.contains("active")) return;
        swatches.forEach(function (b) {
          b.classList.toggle("active", b === btn);
          b.setAttribute("aria-pressed", String(b === btn));
        });
        label.textContent = btn.getAttribute("data-name");
        labelChip.style.setProperty("--c", btn.querySelector(".chip").style.getPropertyValue("--c"));
        var next = preload(btn).cloneNode();
        var show = function () {
          var olds = stage.querySelectorAll("img");
          stage.insertBefore(next, stage.querySelector(".viz-label"));
          requestAnimationFrame(function () {
            requestAnimationFrame(function () { next.classList.remove("fading"); });
          });
          setTimeout(function () { olds.forEach(function (o) { o.remove(); }); }, 700);
        };
        if (next.complete && next.naturalWidth) show(); else next.onload = show;
      });
    });
  }

  // Quote form (Web3Forms). The access key is set in _build/build.py.
  var form = document.getElementById("quote-form");
  if (!form) return;
  var status = form.querySelector(".form-status");
  var msg = function (key) { return form.getAttribute("data-msg-" + key); };

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var ok = true;
    form.querySelectorAll("[required]").forEach(function (field) {
      var valid = field.value.trim() !== "" && field.checkValidity();
      field.setAttribute("aria-invalid", valid ? "false" : "true");
      if (!valid && ok) { field.focus(); ok = false; }
    });
    if (!ok) {
      status.textContent = msg("invalid");
      status.className = "form-status err";
      return;
    }

    var key = form.getAttribute("data-key");
    if (!key) {
      status.textContent = msg("offline");
      status.className = "form-status err";
      return;
    }

    var data = Object.fromEntries(new FormData(form).entries());
    data.access_key = key;
    var button = form.querySelector("button[type=submit]");
    button.disabled = true;
    status.textContent = msg("sending");
    status.className = "form-status";

    fetch("https://api.web3forms.com/submit", {
      method: "POST",
      headers: { "Content-Type": "application/json", Accept: "application/json" },
      body: JSON.stringify(data)
    })
      .then(function (r) { return r.json(); })
      .then(function (res) {
        if (!res.success) throw new Error(res.message);
        form.reset();
        status.textContent = msg("ok");
        status.className = "form-status ok";
      })
      .catch(function () {
        status.textContent = msg("fail");
        status.className = "form-status err";
      })
      .finally(function () { button.disabled = false; });
  });
})();
