# podbag-page

The website of [podbag](https://github.com/SteelCrab/podbag): [podbag.dev](https://podbag.dev).

## Contents

- [What is here](#what-is-here)
- [Build it](#build-it)
- [Write a blog post](#write-a-blog-post)
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

## Write a blog post

- A post is one folder: `site/blog/posts/<slug>/`, with one Markdown file per language
  (`en.md`, `ko.md`, …). A language without its file does not list the post, so write all
  seven.
- Each file starts with front matter: title, date, author (a key of
  `site/blog/authors.json`), categories (announcements, engineering, benchmarks, how-to), tags,
  summary, image, image_alt and draft. See the top of `dev/docs/blog.py`.
- For a personal byline, set the author's entry to `{"github": "username"}`.
  The post links the handle to its GitHub profile.
- `{{n:2970}}` writes a number in the page's language (2,970 or 2.970).
- `draft: true` keeps a post out of the build.
- `python3 dev/docs/blog.py cards` draws the sharing pictures (`card-<lang>.png`).
- Check before a push:

```sh
python3 dev/docs/site.py _site
python3 -m unittest dev/docs/test_blog.py
python3 dev/docs/check_links.py _site
```

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
