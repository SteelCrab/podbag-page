// podbag.dev: the motion and the copy buttons. The page reads well without this file.
(() => {
  const root = document.documentElement;
  const still = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const wait = (ms) => new Promise((done) => setTimeout(done, ms));
  const GROUP = root.dataset.group || ",";
  const DECIMAL = root.dataset.decimal || ".";

  // One live region tells screen readers what a copy or share button did.
  const status = document.createElement("p");
  status.className = "sr-only";
  status.setAttribute("role", "status");
  document.body.append(status);
  let said = "";
  const say = (message) => {
    // A repeated message gets a no-break space, or some screen readers skip it.
    const text = message === said ? message + " " : message;
    said = text;
    status.textContent = "";
    requestAnimationFrame(() => { status.textContent = text; });
  };
  const timers = new WeakMap();
  const flash = (button, message) => {
    if (!timers.has(button)) button.dataset.label = button.innerHTML;
    clearTimeout(timers.get(button));
    const icon = button.querySelector("svg");
    button.textContent = message;
    if (icon) button.prepend(icon);
    say(message);
    timers.set(button, setTimeout(() => {
      button.innerHTML = button.dataset.label;
      timers.delete(button);
    }, 1800));
  };

  // Copy buttons. Comments after "#" are not copied.
  for (const box of document.querySelectorAll(".code")) {
    const button = box.querySelector("button");
    if (!button) continue;
    button.addEventListener("click", async () => {
      const code = box.querySelector("code");
      const text = box.classList.contains("code-file")
        ? code.textContent + "\n"
        : code.innerText.replace(/[ \t]+#.*$/gm, "");
      try {
        await navigator.clipboard.writeText(text);
        flash(button, button.dataset.copied);
      } catch {
        flash(button, button.dataset.fail);
      }
    });
  }

  // Share buttons: the system's share sheet where there is one, else copy the link.
  // data-native: only the share sheet; data-copy: only the copy.
  if (navigator.share) root.classList.add("can-share");
  for (const button of document.querySelectorAll("[data-share]")) {
    button.addEventListener("click", async () => {
      const { url, title } = button.dataset;
      if (navigator.share && !("copy" in button.dataset)) {
        try {
          await navigator.share({ title, url });
          return;
        } catch (error) {
          if (error.name === "AbortError") return;
          if ("native" in button.dataset) return;
        }
      }
      try {
        await navigator.clipboard.writeText(url);
        flash(button, button.dataset.done);
      } catch {
        flash(button, button.dataset.fail);
      }
    });
  }

  // Numbers count up to the value the page shows.
  function format(value, decimals) {
    const [whole, part] = value.toFixed(decimals).split(".");
    const grouped = whole.replace(/\B(?=(\d{3})+(?!\d))/g, GROUP);
    return part ? grouped + DECIMAL + part : grouped;
  }
  function count(el, ms = 1100) {
    const end = el.textContent;
    const to = parseFloat(el.dataset.to);
    const decimals = parseInt(el.dataset.dec || "0", 10);
    if (still || !Number.isFinite(to)) return;
    const start = performance.now();
    const step = (now) => {
      const t = Math.min(1, (now - start) / ms);
      el.textContent = t < 1 ? format(to * (1 - Math.pow(1 - t, 3)), decimals) : end;
      if (t < 1) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
  }

  // Reveal on scroll. Bars grow and their numbers count when they appear.
  const reveal = new IntersectionObserver((entries) => {
    for (const e of entries) {
      if (!e.isIntersecting) continue;
      e.target.classList.add("in");
      e.target.querySelectorAll("[data-to]").forEach((n) => count(n));
      reveal.unobserve(e.target);
    }
  }, { rootMargin: "0px 0px -8% 0px" });
  document.querySelectorAll(".reveal").forEach((el) => reveal.observe(el));

  // Loops run only while they are on screen.
  const onScreen = new Set();
  const playing = new IntersectionObserver((entries) => {
    for (const e of entries) {
      e.target.classList.toggle("play", e.isIntersecting);
      if (e.isIntersecting) onScreen.add(e.target); else onScreen.delete(e.target);
    }
  }, { threshold: 0.15 });
  document.querySelectorAll("[data-loop], .term").forEach((el) => playing.observe(el));

  // The terminal types its session, again and again, while it is on screen.
  const term = document.querySelector(".term");
  const data = document.getElementById("session");
  if (!term || !data || still) return;
  const session = JSON.parse(data.textContent);
  const live = term.querySelector(".live");
  const caret = document.createElement("span");
  caret.className = "caret";
  const add = (cls, text) => {
    const span = document.createElement("span");
    span.className = cls;
    span.textContent = text;
    live.insertBefore(span, caret);
    return span;
  };
  const shown = async (ms) => {
    await wait(ms);
    while (!onScreen.has(term)) await wait(250);
  };
  term.classList.add("typing");
  (async () => {
    for (;;) {
      live.textContent = "";
      live.append(caret);
      for (const [kind, text] of session) {
        if (kind === "c") {
          add("p", "$ ");
          const cmd = add("c", "");
          for (const ch of text) {
            cmd.textContent += ch;
            await shown(14 + Math.random() * 32);
          }
          await shown(450);
        } else {
          add(kind, text);
          await shown(280);
        }
        live.insertBefore(document.createTextNode("\n"), caret);
      }
      await shown(4500);
    }
  })();
})();
