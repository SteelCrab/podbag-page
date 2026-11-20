#!/usr/bin/env python3
"""Check the built site for broken internal links: every href, src and srcset in every page,
and every link in the feeds, must point to a file in OUT, and every #fragment to an id.

Addresses on https://podbag.dev/ count as internal. Other sites are not checked.

usage: python3 dev/docs/check_links.py OUT
"""
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit
from xml.etree import ElementTree

SITE = "https://podbag.dev/"


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links, self.ids = [], set()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.add(attrs["id"])
        for name in ("href", "src"):
            if attrs.get(name):
                self.links.append(attrs[name])
        if attrs.get("srcset"):
            self.links += [part.strip().split()[0] for part in attrs["srcset"].split(",")]
        if tag == "meta" and attrs.get("content", "").startswith(SITE):
            self.links.append(attrs["content"])


def url_of(out, path):
    """The address a file in OUT is served at."""
    rel = path.relative_to(out).as_posix()
    if rel.endswith("index.html"):
        rel = rel[:-len("index.html")]
    return SITE + rel


def target(out, url):
    """(file, fragment) for an internal URL, or None for another site."""
    if not url.startswith(SITE):
        return None
    parts = urlsplit(url)
    path = unquote(parts.path).lstrip("/")
    file = out / path
    if path == "" or path.endswith("/"):
        file = file / "index.html"
    elif file.is_dir():
        file = file / "index.html"
    return file, parts.fragment


def check(out):
    out = Path(out)
    pages, problems = {}, []
    for path in sorted(out.rglob("*.html")):
        page = Page()
        page.feed(path.read_text())
        pages[path] = page
    links = [(path, link) for path, page in pages.items() for link in page.links]
    for feed in sorted(out.rglob("feed.xml")):
        try:
            tree = ElementTree.parse(feed)
        except ElementTree.ParseError as error:
            problems.append(f"{feed.relative_to(out)}: not valid XML: {error}")
            continue
        for el in tree.iter():
            if el.tag in ("link", "guid", "url") and el.text:
                links.append((feed, el.text.strip()))
            if el.get("href"):
                links.append((feed, el.get("href")))
    for path, link in links:
        if link.startswith(("mailto:", "data:", "javascript:")):
            continue
        base = url_of(out, path) if path.suffix == ".html" else SITE
        url = urljoin(base, link)
        found = target(out, url)
        if found is None:
            continue
        file, fragment = found
        where = f"{path.relative_to(out)}: {link}"
        if not file.exists():
            problems.append(f"{where}: no file {file.relative_to(out)}")
        elif fragment and file.suffix == ".html":
            if file not in pages:
                page = Page()
                page.feed(file.read_text())
                pages[file] = page
            if fragment not in pages[file].ids:
                problems.append(f"{where}: no id {fragment!r}")
    return problems, len(links)


def main():
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    problems, count = check(sys.argv[1])
    for p in problems:
        print(p)
    if problems:
        raise SystemExit(f"{len(problems)} broken links")
    print(f"checked {count} links: none broken")


if __name__ == "__main__":
    main()
