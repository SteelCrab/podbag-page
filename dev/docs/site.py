#!/usr/bin/env python3
"""Build the website into OUT: one page per language from site/page.html and site/i18n/*.json.

English is at /, the other languages at /<lang>/. Every language must have every string that
English has; the build stops if one is missing.

The pictures, videos, install.sh and version come from the podbag repository: a clone next to
this folder (../podbag), or the folder in PODBAG_REPO.

The blog (dev/docs/blog.py, posts in site/blog/posts) is at /blog/ and /<lang>/blog/.
Training (dev/docs/training.py, modules in site/training) is at /training/ and /<lang>/training/.

usage: python3 dev/docs/site.py OUT
       python3 dev/docs/check_links.py OUT     # no broken internal links
       python3 -m unittest dev/docs/test_blog.py dev/docs/test_training.py
       python3 -m http.server -d OUT 8000      # look at it
       python3 dev/docs/site.py --moved OUT    # pages that send the old address to podbag.dev
"""
import html
import importlib.util
import json
import os
import re
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import blog  # noqa: E402
import training  # noqa: E402
from comparisons import Metric, Reading, picker, series  # noqa: E402

PAGE = Path(__file__).resolve().parents[2]
SITE = PAGE / "site"
# The podbag repository: its pictures, videos, install.sh, version and picture texts.
REPO = Path(os.environ.get("PODBAG_REPO", PAGE.parent / "podbag")).resolve()
URL = "https://podbag.dev/"
LANGS = [("en", "English"), ("ko", "한국어"), ("ja", "日本語"), ("zh-CN", "简体中文"),
         ("fil", "Filipino"), ("es", "Español"), ("vi", "Tiếng Việt")]
# Thousands and decimal separators; the rest use "," and ".".
SEPARATORS = {"es": (".", ","), "vi": (".", ",")}
ASSETS = ["style.css", "blog.css", "main.js", "theme.js", "favicon.png", "apple-touch-icon.png", "_headers"]


def version():
    text = (REPO / "Cargo.toml").read_text()
    return re.search(r'^version = "([^"]+)"', text, re.M).group(1)


def storage_text():
    """The animated picture's description in each language (dev/docs/storage.py)."""
    spec = importlib.util.spec_from_file_location("storage", REPO / "dev/docs/storage.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return {lang: words["aria"] for lang, words in module.TEXT.items()}


def number(literal, lang):
    group, decimal = SEPARATORS.get(lang, (",", "."))
    whole, _, part = literal.partition(".")
    whole = f"{int(whole):,}".replace(",", group)
    return whole + (decimal + part if part else "")


def path_of(code):
    return "" if code == "en" else f"{code}/"


# Values in the Linux benchmarks. Keep root and rootless results separate.
LINUX = {
    "start": ("ms", {"podbag-rootless": 4.1, "podbag-root": 4.4, "kiri": 9.1, "podman": 46.4, "docker": 73.8}),
    "mem": ("MiB", {"podbag-root": 105, "kiri": 109, "podbag-rootless": 117, "podman": 203, "docker": 562}),
    "disk": ("MiB", {"podbag-root": 902, "podbag-rootless": 944, "podman": 1783, "kiri": 2960, "docker": 2970}),
    "cache": ("MiB", {"podbag-rootless": 324, "podbag-root": 333, "kiri": 960, "podman": 975, "docker": 982}),
    "idle": ("", {"podbag-rootless": 0, "podbag-root": 0, "kiri": 1, "podman": 1, "docker": 4}),
}


def reading(engine, value, unit, lang):
    product, _, mode = engine.partition("-")
    name = {"podbag": "podbag", "orbstack": "OrbStack"}.get(product, product.title())
    if engine == "docker-desktop":
        name = "Docker Desktop"
    elif mode:
        name += f"<small>{mode}</small>"
    magnitude = value * 1024 if unit == "GiB" else value
    return Reading(product, name, magnitude, (number(str(value), lang) + " " + unit).rstrip())


def homepage_comparisons(template, words, lang, root):
    linux = {}
    for key, (unit, values) in LINUX.items():
        title = words["fact_idle" if key == "idle" else f"chart_{key}_t"]
        caption = "" if key == "idle" else words[f"chart_{key}_s"]
        linux[key] = Metric(title, [reading(k, v, unit, lang) for k, v in values.items()], caption)

    panels = []
    for key, metric, engine in (("start", "start", "podbag-rootless"), ("idle", "idle", "podbag-rootless"),
                                ("memory", "cache", "podbag-rootless"), ("disk", "disk", "podbag-root")):
        unit, values = LINUX[metric]
        value, baseline = values[engine], values["docker"]
        reduction = key in ("memory", "disk")
        target = str(round(100 * (1 - value / baseline)) if reduction else value)
        rows = [reading("podbag" if key == "idle" else engine, value, unit, lang),
                reading("docker", baseline, unit, lang)]
        panels.append(render(template, {
            "key": key, "label": words[f"fact_{key}"], "headline": number(target, lang),
            "target": target, "decimals": str(len(target.partition(".")[2])),
            "prefix": "−" if reduction else "", "suffix": "%" if reduction else (" " + unit).rstrip(),
            "checked": "checked" if key == "start" else "",
            "context": linux[metric].caption if key == "start" else linux[metric].name,
            "nav_benchmarks": words["nav_benchmarks"], "series": series(rows, root),
        }, lang))

    storage = []
    for key, label, engine in (("cache", "fact_memory", "podbag-rootless"), ("disk", "fact_disk", "podbag-root")):
        unit, values = LINUX[key]
        rows = [reading(k, values[k], unit, lang) for k in (engine, "docker")]
        storage.append(Metric(words[label], rows, f'{linux[key].name} · {linux[key].caption}'))

    mac = []
    engines = ("podbag", "docker-desktop", "orbstack", "colima", "kiri")
    for label, samples in [
        ("row_start", [(14.4, "ms"), (97.4, "ms"), (90.4, "ms"), (73.6, "ms"), (11.8, "ms")]),
        ("row_memory", [(1.7, "MiB"), (950, "MiB"), (795, "MiB"), (1.54, "GiB"), (12, "MiB")]),
    ]:
        rows = [reading(engine, value, unit, lang) for engine, (value, unit) in zip(engines, samples, strict=True)]
        mac.append(Metric(words[label], rows))
    return {
        "hero_facts": "\n".join(panels),
        "linux_charts": picker("linux", words["bench_title"], list(linux.values()), root),
        "mac_charts": picker("mac", words["compare_title"], mac, root),
        "storage_charts": picker("storage", words["layers_title"], storage, root),
    }


def session(words, ver):
    return [
        ["c", "curl -fsSL https://podbag.dev/install.sh | sh"],
        ["o", "Downloading podbag-x86_64-linux (latest)"],
        ["o", f"Installed /usr/local/bin/podbag (podbag {ver})"],
        ["c", "podbag run --rm alpine echo hello"],
        ["o", "hello"],
        ["c", "sleep 15; pgrep -l podbag"],
        ["m", words["term_note"]],
    ]


def session_html(lines):
    out = []
    for kind, text in lines:
        if kind == "c":
            out.append(f'<span class="p">$ </span><span class="c">{html.escape(text)}</span>')
        else:
            out.append(f'<span class="{kind}">{html.escape(text)}</span>')
    # The last, empty line is where the cursor waits; keep room for it.
    return "\n".join(out) + "\n "


def render(template, values, lang):
    def fill(match):
        key, kind = match.group(1), match.group(2)
        if key.startswith("n:"):
            return number(key[2:], lang)
        if key not in values:
            raise SystemExit(f"{lang}: no string for {{{{{key}}}}}")
        value = values[key]
        if kind == "attr":
            return html.escape(html.unescape(re.sub(r"<[^>]+>", "", value)), quote=True)
        return value
    page = re.sub(r"\{\{([a-z0-9_:.]+)(?:\|(attr))?\}\}", fill, template)
    if "{{" in page:
        raise SystemExit(f"{lang}: a placeholder is left: {page[page.index('{{'):][:40]}")
    return page


def moved(out):
    """Pages for the old address (GitHub Pages): each one sends the reader to podbag.dev."""
    if out.exists():
        shutil.rmtree(out)
    for code, _ in LANGS:
        target = URL + path_of(code)
        page = out / path_of(code) / "index.html"
        page.parent.mkdir(parents=True, exist_ok=True)
        page.write_text(
            f'<!doctype html>\n<html lang="{code}">\n<meta charset="utf-8">\n<title>podbag</title>\n'
            f'<link rel="canonical" href="{target}">\n'
            f'<meta http-equiv="refresh" content="0; url={target}">\n'
            f'<p>The podbag website is now at <a href="{target}">{target}</a>.</p>\n</html>\n')
    (out / "404.html").write_text(
        '<!doctype html>\n<html lang="en">\n<meta charset="utf-8">\n<title>podbag</title>\n'
        '<script>location.replace("https://podbag.dev" + '
        'location.pathname.replace(/^\\/podbag(?=\\/|$)/, "") + location.hash)</script>\n'
        f'<p>The podbag website is now at <a href="{URL}">{URL}</a>.</p>\n</html>\n')
    print(f"wrote pages that point to {URL} into {out}")


def need_repo():
    if not (REPO / "Cargo.toml").is_file() or not (REPO / "install.sh").is_file():
        raise SystemExit(
            f"cannot find the podbag repository at {REPO}: clone "
            "https://github.com/SteelCrab/podbag next to this folder, or set PODBAG_REPO"
        )


def main():
    need_repo()
    if len(sys.argv) == 3 and sys.argv[1] == "--moved":
        return moved(Path(sys.argv[2]))
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    out = Path(sys.argv[1])
    if out.exists():
        shutil.rmtree(out)
    (out / "images").mkdir(parents=True)
    for name in ASSETS:
        shutil.copy(SITE / name, out / name)
    # The logos of the tools the benchmarks compare with.
    shutil.copytree(SITE / "logos", out / "logos")
    # `curl -fsSL https://podbag.dev/install.sh | sh` gets the same script as the repository.
    shutil.copy(REPO / "install.sh", out / "install.sh")
    for picture in sorted((REPO / "docs/images").iterdir()):
        if picture.suffix in (".svg", ".png"):
            shutil.copy(picture, out / "images" / picture.name)
    (out / "media").mkdir()
    for video in sorted((REPO / "docs/media").glob("*.mp4")):
        shutil.copy(video, out / "media" / video.name)

    template = (SITE / "page.html").read_text()
    fact_template = (SITE / "fact.html").read_text()
    english = json.loads((SITE / "i18n/en.json").read_text())
    alts = storage_text()
    ver = version()
    words_of = {}
    for code, name in LANGS:
        words = json.loads((SITE / f"i18n/{code}.json").read_text())
        missing = sorted(set(english) - set(words))
        extra = sorted(set(words) - set(english))
        if missing or extra:
            raise SystemExit(f"{code}.json: missing {missing}, unknown {extra}")
        words_of[code] = words
        root = "" if code == "en" else "../"
        lines = session(words, ver)
        group, decimal = SEPARATORS.get(code, (",", "."))
        values = dict(words)
        values.update({
            "lang": code, "lang_name": name, "root": root, "site": URL,
            "group": group, "decimal": decimal,
            "canonical": URL + path_of(code),
            "alternates": "\n".join(
                [f'<link rel="alternate" hreflang="{c}" href="{URL}{path_of(c)}">' for c, _ in LANGS]
                + [f'<link rel="alternate" hreflang="x-default" href="{URL}">']),
            "lang_menu": "".join(
                f'<a href="{root}{path_of(c)}" hreflang="{c}" lang="{c}"'
                f'{" aria-current=\"page\"" if c == code else ""}>{n}</a>' for c, n in LANGS),
            "lang_links": " · ".join(
                f'<a href="{root}{path_of(c)}" hreflang="{c}" lang="{c}">{n}</a>' for c, n in LANGS),
            "storage": "storage" if code == "en" else f"storage-{code}",
            "storage_alt": alts[code],
            **homepage_comparisons(fact_template, words, code, root),
            "session_html": session_html(lines),
            "session_json": json.dumps(lines, ensure_ascii=False).replace("</", "<\\/"),
        })
        page = render(template, values, code)
        target = out / path_of(code) / "index.html"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(page)

    (out / "404.html").write_text(render(
        (SITE / "404.html").read_text(),
        {"lang_links": " · ".join(f'<a href="/{path_of(c)}" hreflang="{c}" lang="{c}">{n}</a>'
                                  for c, n in LANGS)}, "en"))
    posts = blog.build(out, sys.modules[__name__], words_of)
    modules = training.build(out, sys.modules[__name__], words_of)
    print(f"built {len(LANGS)} languages, {posts} blog posts and {modules} training modules into {out}")


if __name__ == "__main__":
    main()
