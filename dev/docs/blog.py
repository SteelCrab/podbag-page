#!/usr/bin/env python3
"""The blog: Markdown posts in site/blog/posts/<slug>/<lang>.md, built into /blog/ and /<lang>/blog/.

dev/docs/site.py calls build(). The Markdown is converted here, with the standard library only:
headings, paragraphs, lists, links, emphasis, inline code, fenced code, tables, pictures with
captions, block quotes and rules. `{{n:2970}}` writes a number in the page's language.

A post starts with front matter:

    ---
    title: podbag 0.1.0
    date: 2026-11-20
    author: team
    categories: [announcements]
    tags: [release]
    summary: One or two sentences for the lists, the feed and search engines.
    image: card-en.png
    image_alt: What the picture shows.
    draft: false
    ---

- author: a key of site/blog/authors.json.
- categories: announcements, engineering, benchmarks, how-to.
- image: a file next to the post, or /images/…; card-<lang>.png comes from `cards` below.
- draft: true leaves the post out of the build.

usage: python3 dev/docs/blog.py cards     # draw each post's sharing card (Chrome, Node.js 22)
"""
import html
import json
import re
import shutil
import struct
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from datetime import date as Date, datetime, timezone
from email.utils import format_datetime
from pathlib import Path
from xml.sax.saxutils import escape as xml_escape

from comparisons import Metric, Reading, picker

HERE = Path(__file__).resolve().parent
CATEGORIES = ["announcements", "engineering", "benchmarks", "how-to"]
LOCALES = {"en": "en_US", "ko": "ko_KR", "ja": "ja_JP", "zh-CN": "zh_CN", "fil": "fil_PH",
           "es": "es_ES", "vi": "vi_VN"}
MONTHS = {
    "en": "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split(),
    "fil": ("Enero Pebrero Marso Abril Mayo Hunyo Hulyo Agosto Setyembre Oktubre Nobyembre "
            "Disyembre").split(),
    "es": ("enero febrero marzo abril mayo junio julio agosto septiembre octubre noviembre "
           "diciembre").split(),
}


def format_date(day, lang):
    """A date as people write it in the language."""
    y, m, d = day.year, day.month, day.day
    if lang == "ko":
        return f"{y}년 {m}월 {d}일"
    if lang in ("ja", "zh-CN"):
        return f"{y}年{m}月{d}日"
    if lang == "fil":
        return f"{MONTHS['fil'][m - 1]} {d}, {y}"
    if lang == "es":
        return f"{d} de {MONTHS['es'][m - 1]} de {y}"
    if lang == "vi":
        return f"{d} tháng {m}, {y}"
    return f"{d} {MONTHS['en'][m - 1]} {y}"


# ---------------------------------------------------------------- Markdown

FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})\s*([\w+.-]*)\s*$")
HEADING = re.compile(r"^ {0,3}(#{1,6})\s+(.*?)\s*#*\s*$")
RULE = re.compile(r"^ {0,3}([-*_])(\s*\1){2,}\s*$")
QUOTE = re.compile(r"^ {0,3}>")
LIST = re.compile(r"^( *)([-*+]|\d{1,9}[.)])( +)(.*)$")
DELIM = re.compile(r"^\s*\|?\s*:?-+:?\s*(\|\s*:?-+:?\s*)*\|?\s*$")
VIDEO_POSTER = re.compile(r'^\[!\[([^\]]+)\]\(([^)\s]+)\)\]\(([^)\s]+\.mp4)\)$', re.I)
IMAGE_ONLY = re.compile(r'^!\[([^\]]*)\]\(([^)\s]+)(?:\s+"([^"]*)")?\)$')
IMAGE = re.compile(r'!\[([^\]]*)\]\(([^)\s]+)(?:\s+"([^"]*)")?\)')
LINK = re.compile(r'\[([^\]]+)\]\(([^)\s]+)(?:\s+"([^"]*)")?\)')
COMPARE = re.compile(r"^<!-- compare-(columns|rows): ([a-z ]+) -->$")
NUMBER = re.compile(r"\{\{n:(\d+(?:\.\d+)?)\}\}")
SEPARATORS = {"es": (".", ","), "vi": (".", ",")}
# Lines of one paragraph join without a space in these languages.
NO_SPACES = {"ja", "zh-CN"}


def number(literal, lang):
    group, decimal = SEPARATORS.get(lang, (",", "."))
    whole, _, part = literal.partition(".")
    return f"{int(whole):,}".replace(",", group) + (decimal + part if part else "")


def code_text(text):
    """Code as HTML. "{" is written as a reference so that no page keeps a stray "{{"."""
    return html.escape(text, quote=False).replace("{", "&#123;")


def slug(text):
    text = html.unescape(re.sub(r"<[^>]+>", "", text)).lower()
    text = re.sub(r"[^\w\- ]", "", text).strip()
    return re.sub(r"[\s-]+", "-", text) or "section"


def indent_of(line):
    return len(line) - len(line.lstrip(" "))


def split_row(line):
    """The cells of a table row: split on "|" outside code spans and escapes."""
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|") and not line.endswith("\\|"):
        line = line[:-1]
    cells, cell, ticks, i = [], "", False, 0
    while i < len(line):
        ch = line[i]
        if ch == "\\" and i + 1 < len(line) and line[i + 1] == "|":
            cell += "|"
            i += 2
            continue
        if ch == "`":
            ticks = not ticks
        if ch == "|" and not ticks:
            cells.append(cell.strip())
            cell = ""
        else:
            cell += ch
        i += 1
    cells.append(cell.strip())
    return cells


class Markdown:
    """Markdown to HTML for one post.

    root: the page's way to the site root ("../../" or "https://podbag.dev/"); links that
          start with "/" are written from there.
    base: where relative links point, from the site root ("/blog/<slug>/").
    code_button: HTML put after each code block (the copy button).
    picture: picture(src) -> (sources, (width, height) or None); sources are
             (media, src) pairs for a <picture>.
    """

    def __init__(self, lang="en", root="", base="", code_button="", picture=None, table_label=""):
        self.lang, self.root, self.base = lang, root, base
        self.code_button, self.picture = code_button, picture
        self.ids = set()
        self.table_label = table_label
        self.comparison_count = 0

    def convert(self, text):
        return self.blocks(text.replace("\r\n", "\n").replace("\t", "    ").split("\n"))

    # Blocks

    def starts_block(self, lines, i):
        line = lines[i]
        return bool(FENCE.match(line) or HEADING.match(line) or RULE.match(line)
                    or QUOTE.match(line) or LIST.match(line) or COMPARE.fullmatch(line) or self.is_table(lines, i))

    @staticmethod
    def is_table(lines, i):
        return ("|" in lines[i] and i + 1 < len(lines) and "|" in lines[i + 1]
                and bool(DELIM.match(lines[i + 1])))

    def blocks(self, lines, tight=False):
        out, i = [], 0
        while i < len(lines):
            line = lines[i]
            if not line.strip():
                i += 1
                continue
            if m := FENCE.match(line):
                fence, info, body = m.group(1), m.group(2), []
                i += 1
                while i < len(lines) and not re.match(
                        rf"^ {{0,3}}{re.escape(fence[0])}{{{len(fence)},}}\s*$", lines[i]):
                    body.append(lines[i])
                    i += 1
                i += 1
                out.append(self.code(body, info))
            elif m := HEADING.match(line):
                out.append(self.heading(len(m.group(1)), m.group(2)))
                i += 1
            elif RULE.match(line):
                out.append("<hr>")
                i += 1
            elif QUOTE.match(line):
                quote = []
                while i < len(lines) and lines[i].strip() and (
                        QUOTE.match(lines[i]) or not self.starts_block(lines, i)):
                    quote.append(re.sub(r"^ {0,3}> ?", "", lines[i]))
                    i += 1
                out.append(f"<blockquote>\n{self.blocks(quote)}\n</blockquote>")
            elif LIST.match(line):
                i = self.list(lines, i, out)
            elif m := COMPARE.fullmatch(line):
                if i + 2 >= len(lines) or not self.is_table(lines, i + 1):
                    raise ValueError(f"Expected a comparison table after {line}")
                i = self.table(lines, i + 1, out, m)
            elif self.is_table(lines, i):
                i = self.table(lines, i, out)
            else:
                para = [line.strip()]
                i += 1
                while i < len(lines) and lines[i].strip() and not self.starts_block(lines, i):
                    para.append(lines[i].strip())
                    i += 1
                out.append(self.paragraph(para, tight))
        return "\n".join(out)

    def code(self, body, info):
        cls = f' class="language-{html.escape(info)}"' if info else ""
        text = code_text("\n".join(body))
        return f'<div class="code"><pre><code{cls}>{text}</code></pre>{self.code_button}</div>'

    def heading(self, level, text):
        level = max(level, 2)  # the page's title is the only <h1>
        if m := re.match(r"^(.*?)\s*\{#([\w-]+)\}$", text):
            text, ident = m.group(1), m.group(2)
        else:
            ident = slug(self.inline(text))
        base, n = ident, 2
        while ident in self.ids:
            ident, n = f"{base}-{n}", n + 1
        self.ids.add(ident)
        return f'<h{level} id="{ident}">{self.inline(text)}</h{level}>'

    def list(self, lines, i, out):
        first = LIST.match(lines[i])
        indent, ordered = len(first.group(1)), first.group(2)[0].isdigit()

        def same(m):
            return m and len(m.group(1)) == indent and m.group(2)[0].isdigit() == ordered

        items, loose = [], False
        while i < len(lines) and same(m := LIST.match(lines[i])):
            width = indent + len(m.group(2)) + len(m.group(3))
            body = [m.group(4)]
            i += 1
            while i < len(lines):
                line = lines[i]
                if not line.strip():
                    j = i
                    while j < len(lines) and not lines[j].strip():
                        j += 1
                    if j < len(lines) and indent_of(lines[j]) >= width:
                        body.extend([""] * (j - i))
                        i, loose = j, True
                        continue
                    if j < len(lines) and same(LIST.match(lines[j])):
                        i, loose = j, True
                    break
                if indent_of(line) >= width:
                    body.append(line[width:])
                elif self.starts_block(lines, i):
                    break
                else:
                    body.append(line.strip())  # a lazy continuation of the paragraph
                i += 1
            items.append(body)
        tag = "ol" if ordered else "ul"
        start = int(first.group(2)[:-1]) if ordered else 1
        attrs = f' start="{start}"' if start != 1 else ""
        rendered = "\n".join(f"<li>{self.blocks(body, tight=not loose)}</li>" for body in items)
        out.append(f"<{tag}{attrs}>\n{rendered}\n</{tag}>")
        return i

    def table(self, lines, i, out, comparison=None):
        head = split_row(lines[i])
        aligns = []
        for cell in split_row(lines[i + 1]):
            left, right = cell.startswith(":"), cell.endswith(":")
            aligns.append("center" if left and right else "right" if right else
                          "left" if left else "")
        i += 2
        rows = []
        while i < len(lines) and lines[i].strip() and "|" in lines[i]:
            rows.append(split_row(lines[i]))
            i += 1

        def cell(tag, text, n, scope=""):
            align = aligns[n] if n < len(aligns) else ""
            style = f' style="text-align: {align}"' if align else ""
            return f"<{tag}{scope}{style}>{self.inline(text)}</{tag}>"

        thead = "".join(cell("th", t, n, ' scope="col"') for n, t in enumerate(head))
        body = []
        for row in rows:
            row = (row + [""] * len(head))[:len(head)]
            # A first cell with words and no number names the row.
            first = cell("th", row[0], 0, ' scope="row"') if row[0] and head[0] == "" else \
                cell("td", row[0], 0)
            body.append("<tr>" + first + "".join(
                cell("td", t, n) for n, t in enumerate(row) if n) + "</tr>")
        table = ('<div class="table-wrap"><table>\n'
                 f"<thead><tr>{thead}</tr></thead>\n<tbody>\n" + "\n".join(body)
                 + "\n</tbody>\n</table></div>")
        if comparison and self.table_label:
            axis, products = comparison.groups()
            out.append(self.comparison(head, rows, axis, products.split()))
            table = (f'<details class="comparison-table"><summary>{self.table_label}</summary>'
                     f'{table}</details>')
        out.append(table)
        return i

    def comparison(self, head, rows, axis, products):
        # Each authored measurement starts with its unformatted numeric value.
        if axis == "rows":
            head, *rows = zip(head, *rows, strict=True)
        metrics = []
        for row in rows:
            readings = []
            for product, label, cell in zip(products, head[1:len(products) + 1],
                                            row[1:len(products) + 1], strict=True):
                value = NUMBER.match(cell)
                if not value:
                    raise ValueError(f"Expected a numeric comparison value in {cell!r}")
                readings.append(Reading(product, self.inline(label), float(value[1]), self.inline(cell)))
            metrics.append(Metric(self.inline(row[0]), readings))
        self.comparison_count += 1
        return picker(f"article-metric-{self.comparison_count}", self.table_label, metrics, self.root)

    def paragraph(self, lines, tight):
        text = ("" if self.lang in NO_SPACES else " ").join(lines)
        if m := VIDEO_POSTER.fullmatch(text):
            label = html.escape(html.unescape(m[1]), quote=True)
            video = self.url(m[3])
            return (f'<figure><video controls playsinline preload="none" aria-label="{label}" '
                    f'poster="{self.url(m[2])}" src="{video}"><a href="{video}">{label}</a></video></figure>')
        if m := IMAGE_ONLY.match(text):
            img = self.image(m.group(1), m.group(2))
            caption = f"<figcaption>{self.inline(m.group(3))}</figcaption>" if m.group(3) else ""
            return f"<figure>{img}{caption}</figure>"
        body = self.inline(text)
        return body if tight else f"<p>{body}</p>"

    # Inline

    def url(self, href):
        href = html.unescape(href)
        if re.match(r"^([a-z][a-z0-9+.-]*:|#|//)", href):
            pass
        elif href.startswith("/"):
            href = self.root + href[1:]
        elif self.base:
            href = self.root + self.base.lstrip("/") + href
        return html.escape(href, quote=True)

    def image(self, alt, src):
        alt = html.escape(html.unescape(alt), quote=True)
        sources, size = self.picture(src) if self.picture else ([], None)
        dims = f' width="{size[0]}" height="{size[1]}"' if size else ""
        img = f'<img src="{self.url(src)}" alt="{alt}"{dims} loading="lazy">'
        if not sources:
            return img
        tags = "".join(f'<source media="{html.escape(media)}" srcset="{self.url(s)}">'
                       for media, s in sources)
        return f"<picture>{tags}{img}</picture>"

    def inline(self, text):
        keep = []

        def stash(piece):
            keep.append(piece)
            return f"\x00{len(keep) - 1}\x00"

        text = re.sub(r"\\([\\`*_{}\[\]()#+\-.!|<>~\"])",
                      lambda m: stash(html.escape(m.group(1))), text)
        text = re.sub(r"(`+)(.+?)\1", lambda m: stash(f"<code>{code_text(m.group(2).strip())}</code>"),
                      text)
        text = re.sub(r"<(https?://[^\s>]+)>", lambda m: stash(
            f'<a href="{self.url(m.group(1))}">{html.escape(m.group(1))}</a>'), text)
        text = NUMBER.sub(lambda m: number(m.group(1), self.lang), text)
        text = html.escape(text, quote=False)
        text = IMAGE.sub(lambda m: stash(self.image(m.group(1), m.group(2))), text)

        def link(m):
            title = f' title="{html.escape(m.group(3), quote=True)}"' if m.group(3) else ""
            return stash(f'<a href="{self.url(m.group(2))}"{title}>{self.emphasis(m.group(1))}</a>')

        text = self.emphasis(LINK.sub(link, text))
        while "\x00" in text:
            text = re.sub(r"\x00(\d+)\x00", lambda m: keep[int(m.group(1))], text)
        return text

    @staticmethod
    def emphasis(text):
        text = re.sub(r"\*\*(?=\S)(.+?)(?<=\S)\*\*", r"<strong>\1</strong>", text)
        text = re.sub(r"(?<!\*)\*(?=[^\s*])(.+?)(?<=[^\s*])\*(?!\*)", r"<em>\1</em>", text)
        return re.sub(r"(?<!\w)_(?=\S)(.+?)(?<=\S)_(?!\w)", r"<em>\1</em>", text)


def markdown(text, **options):
    return Markdown(**options).convert(text)


# ---------------------------------------------------------------- Posts

@dataclass
class Post:
    slug: str
    lang: str
    title: str
    day: Date
    author: str
    categories: list
    tags: list
    summary: str
    image: str
    image_alt: str
    body: str
    folder: Path = field(repr=False, default=None)


def parse_value(value):
    if value.startswith("[") and value.endswith("]"):
        items = re.findall(r'\s*"((?:[^"\\]|\\.)*)"\s*|([^,]+)', value[1:-1])
        return [parse_value(q and f'"{q}"' or p.strip()) for q, p in items if (q or p.strip())]
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1].replace('\\"', '"')
    if value in ("true", "false"):
        return value == "true"
    return value


def front_matter(text):
    """(meta, body) of a post. The front matter is "key: value" lines between two "---"."""
    text = text.replace("\r\n", "\n")
    if not text.startswith("---\n"):
        raise ValueError("a post starts with front matter between two --- lines")
    end = text.find("\n---\n", 3)
    if end < 0:
        raise ValueError("the front matter has no closing ---")
    meta = {}
    for n, line in enumerate(text[4:end].split("\n"), 2):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        key, sep, value = line.partition(":")
        if not sep or not key.strip():
            raise ValueError(f"line {n}: not 'key: value': {line!r}")
        meta[key.strip()] = parse_value(value.strip())
    return meta, text[end + 5:]


def load(path, langs, authors):
    """The post in PATH (site/blog/posts/<slug>/<lang>.md), or None for a draft."""
    meta, body = front_matter(path.read_text())
    where = f"{path.parent.name}/{path.name}"
    if meta.get("draft") is True:
        return None
    lang = path.stem
    if lang not in langs:
        raise SystemExit(f"{where}: no language {lang!r}")
    for key in ("title", "date", "author", "categories", "summary"):
        if not meta.get(key):
            raise SystemExit(f"{where}: no {key}")
    try:
        day = Date.fromisoformat(str(meta["date"]))
    except ValueError:
        raise SystemExit(f"{where}: date is not YYYY-MM-DD: {meta['date']}")
    categories = meta["categories"] if isinstance(meta["categories"], list) else [meta["categories"]]
    for c in categories:
        if c not in CATEGORIES:
            raise SystemExit(f"{where}: no category {c!r}; use one of {CATEGORIES}")
    if meta["author"] not in authors:
        raise SystemExit(f"{where}: no author {meta['author']!r} in authors.json")
    tags = meta.get("tags", [])
    known = {"title", "date", "author", "categories", "tags", "summary", "image", "image_alt",
             "draft"}
    if unknown := set(meta) - known:
        raise SystemExit(f"{where}: unknown keys {sorted(unknown)}")
    if meta.get("image") and not meta.get("image_alt"):
        raise SystemExit(f"{where}: an image needs image_alt")
    return Post(path.parent.name, lang, meta["title"], day, meta["author"], categories,
                tags if isinstance(tags, list) else [tags], meta["summary"],
                meta.get("image", ""), meta.get("image_alt", ""), body, path.parent)


def load_all(folder, langs, authors):
    """{lang: [posts, newest first]} for every language, drafts left out."""
    posts = {lang: [] for lang in langs}
    for path in sorted(folder.glob("*/*.md")):
        if post := load(path, langs, authors):
            posts[post.lang].append(post)
    for lang in posts:
        posts[lang].sort(key=lambda p: (p.day, p.slug), reverse=True)
    return posts


def image_size(path):
    """(width, height) of an SVG or PNG file, or None."""
    data = path.read_bytes()[:4096]
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        return struct.unpack(">II", data[16:24])
    if m := re.search(rb'<svg[^>]*?\swidth="(\d+)"[^>]*?\sheight="(\d+)"', data):
        return int(m.group(1)), int(m.group(2))
    return None


def related(post, posts, count=3):
    """Other posts in the same language that share a category or a tag, the closest first."""
    scored = []
    for other in posts:
        if other.slug == post.slug:
            continue
        score = 2 * len(set(post.categories) & set(other.categories)) \
            + len(set(post.tags) & set(other.tags))
        if score:
            scored.append((score, other.day, other))
    scored.sort(key=lambda s: (s[0], s[1]), reverse=True)
    return [s[2] for s in scored[:count]]


# ---------------------------------------------------------------- Pages

class Builder:
    """Writes the blog pages of every language. `site` is dev/docs/site.py."""

    def __init__(self, out, site, words):
        self.out, self.site, self.words = out, site, words
        self.langs = [code for code, _ in site.LANGS]
        self.names = dict(site.LANGS)
        self.url = site.URL
        self.folder = site.SITE / "blog"
        self.pictures = site.REPO / "docs/images"
        self.authors = json.loads((self.folder / "authors.json").read_text())
        self.posts = load_all(self.folder / "posts", self.langs, self.authors)
        self.layout = (self.folder / "layout.html").read_text()

    # Paths are from the site root, with no leading "/": "ko/blog/podbag-0-1-0/".
    def blog_path(self, lang):
        return self.site.path_of(lang) + "blog/"

    def post_path(self, post, lang=None):
        return self.blog_path(lang or post.lang) + post.slug + "/"

    def category_path(self, lang, category):
        return self.blog_path(lang) + f"category/{category}/"

    def picture(self, src):
        """Dark and narrow versions of a picture in /images/, when they exist."""
        if not src.startswith("/images/"):
            path = None
        else:
            path = self.pictures / src[len("/images/"):]
        if path is None or not path.exists():
            return [], None
        sources = []
        if src.endswith("-light.svg"):
            stem = src[:-len("-light.svg")]
            for media, name in [("(max-width: 600px) and (prefers-color-scheme: dark)", "-tall-dark"),
                                ("(max-width: 600px)", "-tall-light"),
                                ("(prefers-color-scheme: dark)", "-dark")]:
                if (self.pictures / (stem[len("/images/"):] + name + ".svg")).exists():
                    sources.append((media, stem + name + ".svg"))
        return sources, image_size(path)

    def image_url(self, post, root):
        """The address of a post's picture from ROOT, and its size; None with no picture."""
        if not post.image:
            card = post.folder / f"card-{post.lang}.png" if post.folder else None
            if card and card.exists():
                return root + f"blog/{post.slug}/{card.name}", image_size(card)
            return None, None
        if post.image.startswith("/"):
            path = self.pictures / post.image[len("/images/"):]
            return root + post.image[1:], image_size(path)
        return root + f"blog/{post.slug}/{post.image}", image_size(post.folder / post.image)

    def body(self, post, root, button="", table_label=""):
        return markdown(post.body, lang=post.lang, root=root, base=f"/blog/{post.slug}/",
                        code_button=button, picture=self.picture, table_label=table_label)

    # Pieces

    def author_info(self, post):
        record = self.authors[post.author]
        if handle := record.get("github"):
            return f"@{handle}", f"https://github.com/{handle}", ""
        local = record[post.lang]
        return local["name"], None, local["bio"]

    def byline(self, post, root):
        author = self.authors[post.author]
        maintainer = author.get("maintainer")
        account = self.authors[maintainer] if maintainer else author
        if not (handle := account.get("github")):
            return html.escape(author[post.lang]["name"])
        prefix = html.escape(author[post.lang]["name"]) + " · " if maintainer else ""
        photo = ""
        if avatar := account.get("avatar"):
            photo = (f'<img class="author-avatar" src="{root}{html.escape(avatar, quote=True)}" '
                     'width="28" height="28" alt="">')
        mark = f'<img src="{root}logos/github.svg" width="20" height="20" alt="">'
        label = html.escape(handle)
        rel = "" if maintainer else ' rel="author"'
        return (f'{prefix}<a class="github-byline"{rel} href="https://github.com/{label}">'
                f'{photo}{mark}<span>@{label}</span></a>')

    def meta_line(self, post, w, root, with_share=True):
        cats = ", ".join(f'<a href="{root}{self.category_path(post.lang, c)}">{w[cat_key(c)]}</a>'
                         for c in post.categories)
        author = self.byline(post, root)
        when = (f'<time datetime="{post.day.isoformat()}">'
                f"{format_date(post.day, post.lang)}</time>")
        parts = [w["blog_by"].replace("{author}", author),
                 w["blog_on"].replace("{date}", when),
                 w["blog_in"].replace("{categories}", cats)]
        parts.append(f'<a href="{root}{self.post_path(post)}">{w["blog_permalink"]}</a>')
        sep = '<span class="sep" aria-hidden="true">|</span>'
        line = sep.join(f"<span>{p}</span>" for p in parts)
        share = (f'<span class="share-wrap">{sep}<button type="button" class="link-button" '
                 f'data-share data-url="{self.url}{self.post_path(post)}" '
                 f'data-title="{html.escape(post.title, quote=True)}" '
                 f'data-done="{html.escape(w["blog_link_copied"], quote=True)}" '
                 f'data-fail="{html.escape(w["copy_fail"], quote=True)}">'
                 f'{w["blog_share"]}</button></span>')
        return f'<p class="meta">{line}{share if with_share else ""}</p>'

    def card(self, post, w, root, level=3, featured=False):
        src, size = self.image_url(post, root)
        href = root + self.post_path(post)
        cats = "".join(f'<a href="{root}{self.category_path(post.lang, c)}">{w[cat_key(c)]}</a>'
                       for c in post.categories)
        if src:
            dims = f' width="{size[0]}" height="{size[1]}"' if size else ""
            loading = "" if featured else ' loading="lazy"'
            picture = f'<img src="{src}" alt=""{dims}{loading}>'
        else:  # no picture: the logo on the band's colour
            picture = (f'<span class="blank"><img src="{root}images/logo-small.png" alt="" '
                       f'width="64" height="64"></span>')
        return (f'<article class="post-card{" featured" if featured else ""} reveal">'
                f'<a class="thumb" href="{href}" tabindex="-1" aria-hidden="true">{picture}</a>'
                f'<div class="post-text"><p class="cats">{cats}</p>'
                f'<h{level} class="post-title"><a href="{href}">{html.escape(post.title)}</a></h{level}>'
                f"{self.meta_line(post, w, root)}"
                f'<p class="summary">{inline(post.summary, post.lang)}</p></div></article>')

    def band(self, lang, w, root, current=None, heading=True):
        title = (f'<h1 class="band-title">{w["blog_title"]}</h1>' if heading else
                 f'<p class="band-title"><a href="{root}{self.blog_path(lang)}">{w["blog_title"]}</a></p>')
        links = [(root + self.blog_path(lang), w["blog_all"], current == "all")]
        links += [(root + self.category_path(lang, c), w[cat_key(c)], current == c)
                  for c in CATEGORIES]
        nav = "".join(f'<a href="{h}"{" aria-current=\"page\"" if on else ""}>{t}</a>'
                      for h, t, on in links)
        return (f'<div class="band"><div class="wrap">{title}'
                f'<p class="band-sub">{w["blog_tagline"]}</p>'
                f'<nav class="band-nav" aria-label="{attr(w["blog_categories"])}">{nav}</nav>'
                f"</div></div>")

    def side(self, lang, w, root):
        feed = root + self.blog_path(lang) + "feed.xml"
        gh = "https://github.com/SteelCrab/podbag"
        resources = [
            (f"{gh}/blob/main/docs/usage.md", w["blog_res_docs"]),
            (gh, "GitHub"),
            (f"{gh}/releases", w["footer_releases"]),
            (feed, w["blog_res_rss"]),
        ]
        items = "".join(f'<li><a href="{h}">{t}</a></li>' for h, t in resources)
        counts = "".join(
            f'<li><a href="{root}{self.category_path(lang, c)}">{w[cat_key(c)]}</a>'
            f'<span class="count">{sum(c in p.categories for p in self.posts[lang])}</span></li>'
            for c in CATEGORIES)
        button = copy_button(w)
        return (f'<aside class="side" aria-label="{attr(w["blog_side"])}">'
                f'<section class="side-box"><h2>{w["blog_resources"]}</h2><ul>{items}</ul></section>'
                f'<section class="side-box"><h2>{w["blog_categories"]}</h2>'
                f'<ul class="cat-list">{counts}</ul></section>'
                f'<section class="side-box"><h2>{w["blog_get"]}</h2>'
                f'<div class="code"><pre><code>curl -fsSL https://podbag.dev/install.sh | sh</code>'
                f"</pre>{button}</div>"
                f'<p class="note">{w["blog_get_note"]}</p></section></aside>')

    def lang_links(self, targets, lang, root):
        menu = "".join(
            f'<a href="{root}{targets[c]}" hreflang="{c}" lang="{c}"'
            f'{" aria-current=\"page\"" if c == lang else ""}>{self.names[c]}</a>' for c in self.langs)
        line = " · ".join(f'<a href="{root}{targets[c]}" hreflang="{c}" lang="{c}">{self.names[c]}</a>'
                          for c in self.langs)
        return menu, line

    def alternates(self, paths):
        """hreflang links for the languages in PATHS ({lang: path})."""
        links = [f'<link rel="alternate" hreflang="{c}" href="{self.url}{p}">' for c, p in paths.items()]
        default = paths.get("en") or next(iter(paths.values()))
        links.append(f'<link rel="alternate" hreflang="x-default" href="{self.url}{default}">')
        return "\n".join(links)

    def social(self, kind, url, title, description, image, size, alt, lang, extra=""):
        tags = [("og:type", kind), ("og:site_name", "podbag"), ("og:url", url),
                ("og:title", title), ("og:description", description), ("og:image", image),
                ("og:locale", LOCALES[lang])]
        if size:
            tags += [("og:image:width", str(size[0])), ("og:image:height", str(size[1]))]
        if alt:
            tags.append(("og:image:alt", alt))
        out = [f'<meta property="{k}" content="{attr(v)}">' for k, v in tags]
        out += [f'<meta name="{k}" content="{attr(v)}">' for k, v in [
            ("twitter:card", "summary_large_image"), ("twitter:title", title),
            ("twitter:description", description), ("twitter:image", image)]]
        return "\n".join(out) + extra

    def page(self, lang, path, values):
        """Write one page at PATH (a folder) from the layout."""
        w = self.words[lang]
        root = "../" * path.count("/")
        group, decimal = SEPARATORS.get(lang, (",", "."))
        menu, line = self.lang_links(values.pop("targets"), lang, root)
        full = dict(w)
        full.update({
            "lang": lang, "lang_name": self.names[lang], "root": root, "group": group,
            "decimal": decimal, "home": root + self.site.path_of(lang),
            "blog": root + self.blog_path(lang), "feed": root + self.blog_path(lang) + "feed.xml",
            "canonical": self.url + path, "lang_menu": menu, "lang_links": line,
            "jsonld": "", "social": "",
        })
        full.update(values)
        target = self.out / path / "index.html"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(self.site.render(self.layout, full, lang))

    def all_targets(self, make):
        return {c: make(c) for c in self.langs}

    def list_page(self, lang, path, posts, current, heading, title, description):
        w = self.words[lang]
        root = "../" * path.count("/")
        parts = []
        if heading:
            parts.append(f'<h1 class="list-heading">{heading}</h1>')
        if not posts:
            parts.append(f'<p class="empty">{w["blog_empty"]}</p>')
        rest = posts
        if current == "all" and posts:
            parts.append(self.card(posts[0], w, root, level=2, featured=True))
            rest = posts[1:]
            if rest:
                parts.append(f'<h2 class="list-title">{w["blog_more"]}</h2>')
        level = 3 if current == "all" else 2
        parts += [self.card(p, w, root, level=level) for p in rest]
        content = f'<div class="blog-list">{"".join(parts)}</div>'
        if current == "all":
            make = self.blog_path
        else:
            make = lambda c: self.category_path(c, current)  # noqa: E731
        paths = self.all_targets(make)
        image = self.url + "images/logo.png"
        jsonld = json_ld({
            "@context": "https://schema.org", "@type": "Blog", "name": w["blog_title"],
            "description": description, "url": self.url + path, "inLanguage": lang,
            "publisher": publisher(self.url),
            "blogPost": [{"@type": "BlogPosting", "headline": p.title,
                          "url": self.url + self.post_path(p),
                          "datePublished": p.day.isoformat()} for p in posts[:20]],
        })
        self.page(lang, path, {
            "targets": paths, "page_title": title, "page_description": description,
            "alternates": self.alternates(paths),
            "social": self.social("website", self.url + path, title, description, image,
                                  image_size(self.pictures / "logo.png"), "", lang),
            "jsonld": jsonld, "band": self.band(lang, w, root, current, heading=current == "all"),
            "content": content, "side": self.side(lang, w, root),
        })

    def post_page(self, post, newer, older):
        lang, w = post.lang, self.words[post.lang]
        path = self.post_path(post)
        root = "../" * path.count("/")
        translations = {c: self.post_path(post, c) for c in self.langs
                        if any(p.slug == post.slug for p in self.posts[c])}
        targets = {c: translations.get(c, self.blog_path(c)) for c in self.langs}
        name, profile, bio = self.author_info(post)
        first = post.categories[0]
        crumbs = (f'<nav class="crumbs" aria-label="{attr(w["blog_breadcrumb"])}"><ol>'
                  f'<li><a href="{root}{self.site.path_of(lang)}">podbag</a></li>'
                  f'<li><a href="{root}{self.blog_path(lang)}">{w["nav_blog"]}</a></li>'
                  f'<li><a href="{root}{self.category_path(lang, first)}">{w[cat_key(first)]}</a></li>'
                  f"</ol></nav>")
        url = self.url + path
        share = (f'<div class="share-bar" role="group" aria-label="{attr(w["blog_share"])}">'
                 f'<button type="button" class="button small" data-share data-native '
                 f'data-url="{url}" data-title="{attr(post.title)}" '
                 f'data-done="{attr(w["blog_link_copied"])}" data-fail="{attr(w["copy_fail"])}">'
                 f'{ICON_SHARE}{w["blog_share"]}</button>'
                 f'<button type="button" class="button small" data-share data-copy '
                 f'data-url="{url}" data-title="{attr(post.title)}" '
                 f'data-done="{attr(w["blog_link_copied"])}" data-fail="{attr(w["copy_fail"])}">'
                 f'{ICON_LINK}{w["blog_copy_link"]}</button></div>')
        tags = "".join(f"<li>{html.escape(t)}</li>" for t in post.tags)
        tags_html = (f'<section class="tags" aria-labelledby="tags-h"><h2 id="tags-h">'
                     f'{w["blog_tags"]}</h2><ul>{tags}</ul></section>') if tags else ""
        portrait = "" if profile else (
            f'<img src="{root}images/logo-small.png" alt="" width="56" height="56">')
        about = (f'<section class="author-box" aria-labelledby="author-h">'
                 f'{portrait}<div><h2 id="author-h">{w["blog_about_author"]}</h2>'
                 f'<p><b>{self.byline(post, root)}</b></p>'
                 + (f"<p>{bio}</p>" if bio else "") + "</div></section>")
        steps = []
        if older:
            steps.append(f'<a class="prev" rel="prev" href="{root}{self.post_path(older)}">'
                         f'<span>← {w["blog_older"]}</span><b>{html.escape(older.title)}</b></a>')
        if newer:
            steps.append(f'<a class="next" rel="next" href="{root}{self.post_path(newer)}">'
                         f'<span>{w["blog_newer"]} →</span><b>{html.escape(newer.title)}</b></a>')
        steps_html = (f'<nav class="post-nav" aria-label="{attr(w["blog_more"])}">'
                      f'{"".join(steps)}</nav>') if steps else ""
        near = related(post, self.posts[lang])
        near_html = ""
        if near:
            items = "".join(
                f'<li><a href="{root}{self.post_path(p)}">{html.escape(p.title)}</a>'
                f'<time datetime="{p.day.isoformat()}">{format_date(p.day, lang)}</time></li>'
                for p in near)
            near_html = (f'<section class="related" aria-labelledby="related-h">'
                         f'<h2 id="related-h">{w["blog_related"]}</h2><ul>{items}</ul></section>')
        content = (f'<article class="post">{crumbs}<header class="post-head">'
                   f'<h1>{html.escape(post.title)}</h1>{self.meta_line(post, w, root, with_share=False)}'
                   f"{share}</header>"
                   f'<div class="prose">{self.body(post, root, copy_button(w), w["data_table"])}</div>'
                   f'<footer class="post-foot">{about}{tags_html}{steps_html}</footer>'
                   f"{near_html}</article>")
        image, size = self.image_url(post, self.url)
        if not image:
            image, size = self.url + "images/logo.png", image_size(self.pictures / "logo.png")
        names = [w[cat_key(c)] for c in post.categories]
        extra = "\n" + "\n".join(
            [f'<meta property="article:published_time" content="{post.day.isoformat()}">']
            + [f'<meta property="article:section" content="{attr(n)}">' for n in names[:1]]
            + [f'<meta property="article:tag" content="{attr(t)}">' for t in post.tags])
        summary = strip(inline(post.summary, lang))
        jsonld = json_ld({
            "@context": "https://schema.org", "@type": "BlogPosting",
            "headline": post.title, "description": summary, "inLanguage": lang,
            "datePublished": post.day.isoformat(), "dateModified": post.day.isoformat(),
            "url": url, "mainEntityOfPage": {"@type": "WebPage", "@id": url},
            "image": image, "articleSection": names, "keywords": post.tags,
            "author": {"@type": "Person" if profile else "Organization", "name": name,
                       "url": profile or self.url},
            "publisher": publisher(self.url),
        })
        self.page(lang, path, {
            "targets": targets, "page_title": f"{post.title} — {strip(w['blog_title'])}",
            "page_description": summary, "alternates": self.alternates(translations),
            "social": self.social("article", url, post.title, summary, image, size,
                                  post.image_alt, lang, extra),
            "jsonld": jsonld, "band": self.band(lang, w, root, None, heading=False),
            "content": content, "side": self.side(lang, w, root),
        })

    def feed(self, lang):
        w = self.words[lang]
        posts = self.posts[lang]
        link = self.url + self.blog_path(lang)
        newest = posts[0].day if posts else Date(2026, 11, 20)
        items = []
        for post in posts[:30]:
            url = self.url + self.post_path(post)
            content = self.body(post, self.url).replace("]]>", "]]]]><![CDATA[>")
            cats = "".join(f"<category>{xml_escape(strip(w[cat_key(c)]))}</category>"
                           for c in post.categories)
            items.append(
                f"<item>\n<title>{xml_escape(post.title)}</title>\n<link>{url}</link>\n"
                f'<guid isPermaLink="true">{url}</guid>\n<pubDate>{rfc822(post.day)}</pubDate>\n'
                f"<dc:creator>{xml_escape(self.author_info(post)[0])}</dc:creator>\n"
                f"{cats}\n<description>{xml_escape(strip(inline(post.summary, lang)))}</description>\n"
                f"<content:encoded><![CDATA[{content}]]></content:encoded>\n</item>")
        feed = (
            '<?xml version="1.0" encoding="utf-8"?>\n'
            '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom" '
            'xmlns:content="http://purl.org/rss/1.0/modules/content/" '
            'xmlns:dc="http://purl.org/dc/elements/1.1/">\n<channel>\n'
            f"<title>{xml_escape(strip(w['blog_title']))}</title>\n<link>{link}</link>\n"
            f"<description>{xml_escape(strip(w['blog_tagline']))}</description>\n"
            f"<language>{lang.lower()}</language>\n<lastBuildDate>{rfc822(newest)}</lastBuildDate>\n"
            f'<atom:link href="{link}feed.xml" rel="self" type="application/rss+xml"/>\n'
            f"<image><url>{self.url}images/logo-small.png</url><title>{xml_escape(strip(w['blog_title']))}"
            f"</title><link>{link}</link></image>\n"
            + "\n".join(items) + "\n</channel>\n</rss>\n")
        target = self.out / self.blog_path(lang) / "feed.xml"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(feed)

    def build(self):
        for folder in sorted((self.folder / "posts").glob("*")):
            if not folder.is_dir():
                continue
            files = [f for f in folder.iterdir() if f.suffix != ".md" and not f.name.startswith(".")]
            if files and any(folder.name == p.slug for ps in self.posts.values() for p in ps):
                (self.out / "blog" / folder.name).mkdir(parents=True, exist_ok=True)
                for f in files:
                    shutil.copy(f, self.out / "blog" / folder.name / f.name)
        count = 0
        for lang in self.langs:
            w = self.words[lang]
            posts = self.posts[lang]
            self.list_page(lang, self.blog_path(lang), posts, "all", "",
                           strip(w["blog_title"]), strip(w["blog_description"]))
            for c in CATEGORIES:
                name = strip(w[cat_key(c)])
                self.list_page(lang, self.category_path(lang, c),
                               [p for p in posts if c in p.categories], c, w[cat_key(c)],
                               f"{name} — {strip(w['blog_title'])}",
                               w["blog_category_description"].replace("{category}", name))
            for n, post in enumerate(posts):
                newer = posts[n - 1] if n > 0 else None
                older = posts[n + 1] if n + 1 < len(posts) else None
                self.post_page(post, newer, older)
                count += 1
            self.feed(lang)
        return count


def build(out, site, words):
    """Build the blog of every language into OUT; return how many post pages were written."""
    return Builder(out, site, words).build()


# ---------------------------------------------------------------- Small helpers

ICON_SHARE = ('<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" '
              'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
              '<path d="M12 3v12M7 8l5-5 5 5M5 13v6a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2v-6"/></svg>')
ICON_LINK = ('<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" '
             'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
             '<path d="M10 14a4 4 0 0 0 5.7 0l3-3a4 4 0 0 0-5.7-5.7l-1 1"/>'
             '<path d="M14 10a4 4 0 0 0-5.7 0l-3 3a4 4 0 0 0 5.7 5.7l1-1"/></svg>')


def cat_key(category):
    return "cat_" + category.replace("-", "_")


def strip(text):
    return html.unescape(re.sub(r"<[^>]+>", "", text))


def attr(text):
    return html.escape(strip(text), quote=True)


def inline(text, lang):
    """One line of Markdown (a summary) as HTML."""
    return Markdown(lang=lang).inline(text)


def copy_button(w):
    return (f'<button type="button" data-copied="{attr(w["copied"])}" '
            f'data-fail="{attr(w["copy_fail"])}">{w["copy"]}</button>')


def json_ld(data):
    text = json.dumps(data, ensure_ascii=False, indent=1).replace("</", "<\\/")
    return f'<script type="application/ld+json">\n{text}\n</script>'


def publisher(url):
    return {"@type": "Organization", "name": "podbag", "url": url,
            "logo": {"@type": "ImageObject", "url": url + "images/logo.png"}}


def rfc822(day):
    return format_datetime(datetime(day.year, day.month, day.day, tzinfo=timezone.utc))


# ---------------------------------------------------------------- Sharing cards

CARD = """<!doctype html>
<html lang="{lang}"><head><meta charset="utf-8"><style>
html, body {{ margin: 0; }}
body {{
  width: 1200px; height: 630px; box-sizing: border-box; padding: 72px 80px;
  display: flex; flex-direction: column; color: #f0efec; overflow: hidden;
  background: radial-gradient(circle at 88% 8%, rgb(57 135 229 / 0.35), transparent 46%),
    radial-gradient(rgb(240 239 236 / 0.08) 1.2px, transparent 1.4px) 0 0 / 26px 26px, #0d0d0d;
  font-family: ui-sans-serif, -apple-system, "Segoe UI", "Apple SD Gothic Neo", "Hiragino Sans",
    "PingFang SC", Helvetica, Arial, sans-serif;
}}
:lang(ko) {{ word-break: keep-all; }}
.top {{ display: flex; align-items: center; gap: 18px; font-size: 30px; font-weight: 800; }}
.top img {{ width: 64px; height: 64px; }}
.top span {{ color: #9db7d9; font-weight: 600; }}
.cat {{ margin-top: auto; color: #6fb3ff; font-size: 24px; font-weight: 700;
  letter-spacing: 0.08em; text-transform: uppercase; }}
h1 {{ margin: 14px 0 0; font-size: {size}px; line-height: 1.12; letter-spacing: -0.02em;
  max-width: 1000px; }}
.foot {{ margin-top: 34px; display: flex; justify-content: space-between; color: #c3c2b7;
  font-size: 24px; border-top: 2px solid #2c2c2a; padding-top: 22px; }}
</style></head><body>
<div class="top"><img src="{logo}" alt="">podbag <span>{blog}</span></div>
<div class="cat">{category}</div>
<h1>{title}</h1>
<div class="foot"><span>{date}</span><span>podbag.dev</span></div>
</body></html>
"""


def cards():
    """Draw site/blog/posts/<slug>/card-<lang>.png for every post (needs Chrome and Node.js 22)."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("podbag_site", HERE / "site.py")
    site = importlib.util.module_from_spec(spec)
    sys.modules["podbag_site"] = site
    spec.loader.exec_module(site)
    words = {code: json.loads((site.SITE / f"i18n/{code}.json").read_text())
             for code, _ in site.LANGS}
    authors = json.loads((site.SITE / "blog/authors.json").read_text())
    posts = load_all(site.SITE / "blog/posts", [c for c, _ in site.LANGS], authors)
    logo = (site.REPO / "docs/images/logo.png").as_uri()
    with tempfile.TemporaryDirectory() as tmp:
        for lang, items in posts.items():
            for post in items:
                w = words[lang]
                title = html.escape(post.title)
                size = 64 if len(post.title) < 60 else 54
                page = Path(tmp) / f"{post.slug}-{lang}.html"
                page.write_text(CARD.format(
                    lang=lang, logo=logo, blog=strip(w["nav_blog"]), size=size, title=title,
                    category=strip(w[cat_key(post.categories[0])]),
                    date=format_date(post.day, lang)))
                shots = Path(tmp) / f"{post.slug}-{lang}"
                shots.mkdir()
                subprocess.run(["node", str(site.REPO / "dev/docs/frames.mjs"), page.as_uri(), str(shots),
                                "1200", "630", "1", "1", "1"], check=True)
                target = post.folder / f"card-{lang}.png"
                shutil.copy(shots / "f00000.png", target)
                print(f"wrote {target}")


if __name__ == "__main__":
    if sys.argv[1:] == ["cards"]:
        cards()
    else:
        raise SystemExit(__doc__)
