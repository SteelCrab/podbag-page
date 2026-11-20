(() => {
  const root = document.documentElement;
  const key = "podbag-theme";
  function readPreference() {
    try {
      const saved = localStorage.getItem(key);
      if (saved === "light" || saved === "dark") root.dataset.theme = saved;
      else delete root.dataset.theme;
    } catch {
      // Keep the current page's selection when storage is unavailable.
    }
  }
  readPreference();

  document.addEventListener("DOMContentLoaded", () => {
    const picker = document.querySelector(".theme-picker");
    if (!picker) return;
    const buttons = picker.querySelectorAll("button");
    const system = matchMedia("(prefers-color-scheme: dark)");
    // Keep the width condition on responsive pictures when overriding their scheme.
    const rules = Array.from(document.querySelectorAll('[media*="prefers-color-scheme"]'), (node) => {
      const conditions = node.media.split(" and ");
      return {
        node,
        theme: conditions.includes("(prefers-color-scheme: dark)") ? "dark" : "light",
        media: conditions.filter((c) => !c.startsWith("(prefers-color-scheme:")).join(" and ") || "all",
      };
    });
    function refresh() {
      const theme = root.dataset.theme || (system.matches ? "dark" : "light");
      for (const button of buttons) {
        button.setAttribute("aria-pressed", String(button.dataset.theme === theme));
      }
      for (const rule of rules) rule.node.media = rule.theme === theme ? rule.media : "not all";
    }

    for (const button of buttons) {
      button.addEventListener("click", () => {
        root.dataset.theme = button.dataset.theme;
        refresh();
        try {
          localStorage.setItem(key, root.dataset.theme);
        } catch {
          // Keep the selected theme for this page.
        }
      });
    }
    system.addEventListener("change", refresh);
    window.addEventListener("pageshow", (event) => {
      if (event.persisted) {
        readPreference();
        refresh();
      }
    });
    refresh();
    picker.hidden = false;
  });
})();
