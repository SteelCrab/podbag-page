// Cloudflare deploy settings for podbag.dev: an assets-only Worker.
// Build the pages first, then deploy the folder:
//   python3 dev/docs/site.py _site && (cd site && npx cf deploy ../_site)
import { defineConfig } from "cf/config";

export default defineConfig({
  worker: {
    name: "podbag-site",
    compatibilityDate: "2026-11-01",
    assets: {
      htmlHandling: "auto-trailing-slash",
      notFoundHandling: "404-page",
    },
    domains: ["podbag.dev", "www.podbag.dev"],
  },
});
