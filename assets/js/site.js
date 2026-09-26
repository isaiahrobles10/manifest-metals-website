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
    var quote = document.getElementById("viz-quote");
    var quoteName = quote && quote.querySelector(".viz-name-cta");
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
        if (quote) {
          quote.href = quote.getAttribute("data-base") + "?color=" + encodeURIComponent(btn.getAttribute("data-value")) + "#quote";
          quoteName.textContent = btn.getAttribute("data-name");
        }
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

  // Photo lightbox
  var lb = document.querySelector(".lightbox");
  if (lb && lb.showModal) {
    var lbImg = lb.querySelector("img");
    document.querySelectorAll(".g-tile").forEach(function (t) {
      t.addEventListener("click", function () {
        lbImg.src = t.getAttribute("data-full");
        lbImg.alt = t.querySelector("img").alt;
        lb.showModal();
      });
    });
    lb.addEventListener("click", function (e) { if (e.target === lb || e.target.closest(".lb-close")) lb.close(); });
  }

  // Quote form. The endpoint is set in _build/build.py (FORM_ENDPOINT).
  var form = document.getElementById("quote-form");
  if (!form) return;
  var status = form.querySelector(".form-status");
  var msg = function (key) { return form.getAttribute("data-msg-" + key); };

  // Commercial-only fields show when "Commercial / bid" is picked
  var bizFields = form.querySelector(".commercial-only");
  var syncType = function () {
    var picked = form.querySelector("input[name=project_type]:checked");
    var biz = picked && picked.value === "Commercial";
    bizFields.hidden = !biz;
    bizFields.querySelectorAll("input").forEach(function (i) { i.disabled = !biz; });
  };
  form.querySelectorAll("input[name=project_type]").forEach(function (r) { r.addEventListener("change", syncType); });

  // Prefill from links like ?color=Light+Stone or ?type=commercial
  var params = new URLSearchParams(window.location.search);
  var color = params.get("color");
  var colorSelect = form.querySelector("select[name=color]");
  if (color && colorSelect) {
    Array.prototype.forEach.call(colorSelect.options, function (o) { if (o.value === color) colorSelect.value = color; });
  }
  if (params.get("type") === "commercial") {
    var biz = form.querySelector("input[name=project_type][value=Commercial]");
    if (biz) biz.checked = true;
  }
  syncType();

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var ok = true;
    form.querySelectorAll("[required], input[type=email], input[type=url]").forEach(function (field) {
      if (field.disabled) return;
      var filled = field.value.trim() !== "";
      var valid = field.required ? filled && field.checkValidity() : !filled || field.checkValidity();
      field.setAttribute("aria-invalid", valid ? "false" : "true");
      if (!valid && ok) { field.focus(); ok = false; }
    });
    if (!ok) {
      status.textContent = msg("invalid");
      status.className = "form-status err";
      return;
    }

    var data = Object.fromEntries(new FormData(form).entries());
    if (data._honey) return;
    var button = form.querySelector("button[type=submit]");
    button.disabled = true;
    status.textContent = msg("sending");
    status.className = "form-status";

    fetch(form.getAttribute("data-endpoint"), {
      method: "POST",
      headers: { "Content-Type": "application/json", Accept: "application/json" },
      body: JSON.stringify(data)
    })
      .then(function (r) { return r.json(); })
      .then(function (res) {
        if (String(res.success) !== "true") throw new Error(res.message);
        form.reset();
        syncType();
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
