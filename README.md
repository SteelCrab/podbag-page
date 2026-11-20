# podbag-page

The website of [podbag](https://github.com/SteelCrab/podbag): [podbag.dev](https://podbag.dev).

## Contents

- [What is here](#what-is-here)
- [Build it](#build-it)
- [Deploy it](#deploy-it)
- [License](#license)

## What is here

- `site/page.html`: the page template. `site/i18n/<lang>.json`: its text in 7 languages
  (en, ko, ja, zh-CN, fil, es, vi).
- `site/style.css`, `site/main.js`, `site/404.html`, `site/_headers`: the rest of the site.
- `dev/docs/site.py`: builds every language into one folder.
- `site/cloudflare.config.ts`: the Cloudflare Worker that serves the folder.

The build also takes these from the podbag repository:

- the pictures (`docs/images`) and the videos (`docs/media`),
- `install.sh`, served at `https://podbag.dev/install.sh`,
- the version (`Cargo.toml`) and the pictures' texts (`dev/docs/storage.py`).

## Build it

```sh
git clone https://github.com/SteelCrab/podbag ../podbag   # once, next to this folder
python3 dev/docs/site.py _site
python3 -m http.server -d _site 8000                     # look at it
```

- `PODBAG_REPO=/path/to/podbag` uses another clone.
- Every language must have every English string. The build stops if one is missing.

## Deploy it

- GitHub Actions deploys on every push to main, once a day, and by hand (Actions → Deploy →
  Run workflow).
- It needs two secrets: `CLOUDFLARE_API_TOKEN` and `CLOUDFLARE_ACCOUNT_ID`. Without them, the
  job builds the site and stops.
- By hand, with the `cf` CLI logged in:

```sh
python3 dev/docs/site.py _site
(cd site && npm ci && npx cf deploy ../_site)
```

## License

Apache-2.0, like podbag. See [LICENSE](LICENSE).
