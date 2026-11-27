#!/usr/bin/env python3
"""Podbag Training: the module catalog and the /training/ pages.

dev/docs/site.py calls build() after the blog. The source is in site/training:

- catalog.json: {"modules": ["container-basics", "web-basics", …]}, the ids in order.
- modules/<id>.podbag: one module file for each id.

The build checks every module file with the rules that Podbag Desktop and the CLI use, and
stops on a bad file. Then it writes:

- /training/modules/<id>.podbag: the files, byte for byte.
- /training/catalog.json: {"format": "podbag-training-catalog-v1", "modules": [{"id", "file",
  "sha256"}, …]}. The apps read it to find new and changed modules.
- /training/gui/ and /<lang>/training/gui/: how to use Podbag Desktop (the first tab): where
  to get it, the pages of its sidebar and the GUI guides (blog posts) from gui.json, as cards.
- /training/ and /<lang>/training/: a page that lists the modules (the "GUI practice" tab).
- /training/tui/ and /<lang>/training/tui/: how to use `podbag tui` (the last tab): the
  main keys and the TUI guides (blog posts) from tui.json, as cards. The TUI has no
  practice module.

gui.json: {"guides": ["<post slug>", …], "minutes": {"<slug>": 5},
"pages": [{"names": {"<lang>": "Images"}, "words": {"<lang>": "…"}}, …]}, with the names that
Podbag Desktop shows and the words in every language.
tui.json: the same, with "keys": [{"keys": ["a", "F2"], "words": {"<lang>": "…"}}, …] in place
of "pages".

The rules for a module file:

- JSON, at most 65,536 bytes, with a known "format" and translations.en.title.
- podbag-course-v1: "id" is the file name ([a-z0-9-]{1,40}). "port" is absent or 1024–65535.
  Every translations.<lang>.url starts with https://podbag.dev/; translations.en has one.
  1 to 40 steps. Each step has a unique "key" ([A-Za-z0-9]{1,40}), names.en and a check
  with a known "kind". A step with a desktop-* check has no command. Any other step has a
  one-line command: "exit" or "podbag …". "{port}" needs "port". The last step is "finish",
  with the command "exit" and the check kind "finish".
- Commands are one podbag command: no shell operators, substitutions, redirections or
  patterns outside single quotes, at most 1,000 characters. "exit" is the finish step's.
- Each check has the fields of its kind (see FIELDS). Ids in RESERVED are the app's.
- The older formats (see LEGACY) keep their fixed ids as file names and have no steps.
- These are the app's rules (parse_package in podbag's src/volume_lesson.rs); keep both
  the same.
"""
import html
import json
import re
from hashlib import sha256

import blog

CATALOG_FORMAT = "podbag-training-catalog-v1"
COURSE = "podbag-course-v1"
# v1 with more check kinds, files for the practice directory, and `docker …` steps.
COURSE_V2 = "podbag-course-v2"
COURSES = {COURSE, COURSE_V2}
MAX_FILES = 8
FILES_LIMIT = 16 * 1024
PATH = re.compile(r"[A-Za-z0-9._-]+(/[A-Za-z0-9._-]+)*")
# What the practice session keeps in its directory: a module file cannot use these names.
SESSION_NAMES = {"bin", "run", "data", "config", "ui", "docker", "api.sock", "disk.img",
                 "console.log", "verified"}
COUNT_MAX = 2 ** 32 - 1
# Older module kinds. The app knows each one by a fixed id.
LEGACY = {
    "podbag-container-basics-v1": "container-basics",
    "podbag-cli-gui-volumes-v1": "volume-basics",
    "podbag-cli-tui-volumes-v1": "tui-volumes",
}
# The blog post that explains each older module.
LEGACY_GUIDES = {
    "container-basics": "container-basics",
    "volume-basics": "cli-tui-volumes",
}
# The apps refuse a larger module file.
LIMIT = 65536
ID = re.compile(r"[a-z0-9-]{1,40}")
KEY = re.compile(r"[A-Za-z0-9]{1,40}")
CONTROL = re.compile(r"[\x00-\x1f\x7f-\x9f]")
GUIDE_SITE = "https://podbag.dev/"
MAX_STEPS = 40
# The fields of each check kind; "page?" is optional. Text fields are one plain line.
NAME = {"name": str}
FIELDS = {
    "network-exists": NAME, "network-absent": NAME, "volume-exists": NAME,
    "volumes-empty": {}, "containers-empty": {}, "container-running": NAME,
    "container-published": {"name": str, "page?": str},
    "container-exited": {"name": str, "code": int}, "container-absent": NAME,
    "stdout-equals": {"text": str}, "output-has-line": {"text": str}, "finish": {},
    "desktop-inspect-exited": NAME, "desktop-ports": NAME,
    "desktop-browser": {"name": str, "page": str}, "desktop-stop": NAME,
    "desktop-inspect-volume": NAME, "desktop-delete-volume": NAME,
    # podbag-course-v2
    "image-exists": NAME, "image-absent": NAME, "container-created": NAME,
    "container-stopped": NAME, "container-paused": NAME, "container-healthy": NAME,
    "container-restarted": {"name": str, "count": int},
    "container-in-network": {"name": str, "network": str},
    "container-not-in-network": {"name": str, "network": str},
    "volume-absent": NAME, "output-contains": {"text": str}, "file-exists": {"path": str},
}
KINDS = set(FIELDS)
V2_KINDS = {"image-exists", "image-absent", "container-created", "container-stopped",
            "container-paused", "container-healthy", "container-restarted",
            "container-in-network", "container-not-in-network", "volume-absent",
            "output-contains", "file-exists"}
MAX_COMMAND = 1000
# Ids a course cannot have: the app's built-in labs, the library's other files, and names
# Windows keeps for devices.
RESERVED = ({"container-basics", "volume-basics", "tui-volumes", "catalog", "cli-tui-volumes",
             "modules", "con", "nul", "aux", "prn"}
            | {f"{p}{n}" for p in ("com", "lpt") for n in range(10)})
BASE64 = re.compile(r"[A-Za-z0-9+/=]+")


class Invalid(ValueError):
    """A module file or the catalog breaks a rule."""


def text(value):
    return isinstance(value, str) and value.strip() != ""


def plain(value):
    """One line of text."""
    return text(value) and not CONTROL.search(value)


def words(value):
    """Text that may have line breaks (titles, guides)."""
    return text(value) and not CONTROL.search(value.replace("\n", ""))


def shell_safe(command):
    """Whether COMMAND is one plain podbag command when a learner pastes it into a shell:
    outside quotes no operators, substitutions, redirections or patterns; inside double
    quotes no expansions. Single quotes keep everything as text."""
    quote = None
    for c in command.replace("{port}", "8080"):
        if quote == "'":
            quote = None if c == "'" else quote
        elif quote == '"':
            if c == '"':
                quote = None
            elif c in "$`\\!":
                return False
        elif c in "'\"":
            quote = c
        elif c in "|&;<>()$`\\*?[]{}~#!":
            return False
    return quote is None


def check_fields(check, where):
    kind = check.get("kind")
    for field, kind_of in FIELDS[kind].items():
        optional = field.endswith("?")
        field = field.rstrip("?")
        if field not in check:
            if optional:
                continue
            raise Invalid(f"{where}: a {kind} check needs {field!r}")
        value = check[field]
        if kind_of is int:
            if type(value) is not int or not (field != "count" or 0 <= value <= COUNT_MAX):
                raise Invalid(f"{where}: {field} must be a whole number")
        elif not plain(value):
            raise Invalid(f"{where}: {field} must be one line of text")


def practice_path(path):
    """A relative path in the practice directory: plain names, no `..`."""
    return (isinstance(path, str) and len(path) <= 200 and PATH.fullmatch(path) is not None
            and all(part not in (".", "..") for part in path.split("/")))


def check_course(module, name):
    v2 = module["format"] == COURSE_V2
    files = module.get("files", {})
    if files and not v2:
        raise Invalid("files need podbag-course-v2")
    if (not isinstance(files, dict) or len(files) > MAX_FILES
            or not all(practice_path(p) and p.split("/")[0].lower() not in SESSION_NAMES for p in files)
            or not all(isinstance(t, str) and not CONTROL.search(t.replace("\n", "").replace("\t", ""))
                       for t in files.values())
            or sum(len(t.encode()) for t in files.values()) > FILES_LIMIT):
        raise Invalid("files are at most 8 plain text files, 16 KiB in all, under the practice directory")
    if module.get("id") != name:
        raise Invalid(f"id {module.get('id')!r} is not the file name {name!r}")
    if module.get("port") is None and any("{port}" in t for t in files.values()):
        raise Invalid("files use {port}, but the module has no port")
    if not ID.fullmatch(name):
        raise Invalid(f"id {name!r} must match [a-z0-9-]{{1,40}}")
    if name in RESERVED:
        raise Invalid(f"id {name!r} is taken by the app")
    port = module.get("port")
    if port is not None and (type(port) is not int or not 1024 <= port <= 65535):
        raise Invalid(f"port {port!r} must be a number from 1024 to 65535")
    for lang, words in module["translations"].items():
        if not isinstance(words, dict):
            raise Invalid(f"translations.{lang} is not an object")
        url = words.get("url")
        if url is not None and not (isinstance(url, str) and url.startswith(GUIDE_SITE)
                                    and not re.search(r"\s", url)):
            raise Invalid(f"translations.{lang}.url {url!r} must start with {GUIDE_SITE}")
    if not text(module["translations"]["en"].get("url")):
        raise Invalid("translations.en has no url (the guide)")
    steps = module.get("steps")
    if not isinstance(steps, list) or not 1 <= len(steps) <= MAX_STEPS:
        raise Invalid(f"steps must be a list of 1 to {MAX_STEPS} steps")
    keys = set()
    for n, step in enumerate(steps, 1):
        where = f"step {n}"
        if not isinstance(step, dict):
            raise Invalid(f"{where} is not an object")
        key = step.get("key")
        if not isinstance(key, str) or not KEY.fullmatch(key):
            raise Invalid(f"{where}: key {key!r} must match [A-Za-z0-9]{{1,40}}")
        where = f"step {n} ({key})"
        if key in keys:
            raise Invalid(f"{where}: the key is used twice")
        keys.add(key)
        names = step.get("names")
        if not isinstance(names, dict) or not text(names.get("en")):
            raise Invalid(f"{where}: no names.en")
        if not all(plain(n) for n in names.values()):
            raise Invalid(f"{where}: every name is one line of text")
        check = step.get("check")
        kind = check.get("kind") if isinstance(check, dict) else None
        if kind not in KINDS:
            raise Invalid(f"{where}: unknown check kind {kind!r}")
        if kind in V2_KINDS and not v2:
            raise Invalid(f"{where}: a {kind} check needs podbag-course-v2")
        check_fields(check, where)
        if port is None and any(isinstance(v, str) and "{port}" in v for v in check.values()):
            raise Invalid(f"{where}: the check uses {{port}}, but the module has no port")
        if kind == "file-exists" and not practice_path(check["path"]):
            raise Invalid(f"{where}: file-exists checks a path outside the practice directory")
        if kind.startswith("desktop-"):
            if "command" in step:
                raise Invalid(f"{where}: a Desktop step has no command")
            continue
        command = step.get("command")
        if not isinstance(command, str):
            raise Invalid(f"{where}: no command")
        if (command == "exit") != (kind == "finish"):
            raise Invalid(f"{where}: exit is the command of the finish step only")
        programs = ("podbag ", "docker ") if v2 else ("podbag ",)
        if command.startswith("docker ") and (command.split()[1].startswith("-")
                                              or command.split()[1] == "context"):
            raise Invalid(f"{where}: a docker command talks to the practice engine: no global "
                          f"options before the command and no docker context: {command!r}")
        if command != "exit" and not command.startswith(programs):
            raise Invalid(f"{where}: the command must be exit or start with "
                          f"{' or '.join(repr(p) for p in programs)}: {command!r}")
        if CONTROL.search(command):
            raise Invalid(f"{where}: the command has a control character")
        if len(command) > MAX_COMMAND:
            raise Invalid(f"{where}: the command is longer than {MAX_COMMAND} characters")
        if not shell_safe(command):
            raise Invalid(f"{where}: the command must be one podbag command, without shell "
                          f"operators outside single quotes: {command!r}")
        if "{port}" in command and port is None:
            raise Invalid(f"{where}: the command uses {{port}}, but the module has no port")
    last = steps[-1]
    if last.get("key") != "finish" or last.get("command") != "exit" or last["check"]["kind"] != "finish":
        raise Invalid("the last step must be key finish, command exit, check kind finish")


def check(raw, name):
    """The module in RAW (the bytes of modules/NAME.podbag) as a dict; Invalid if it is bad."""
    if len(raw) > LIMIT:
        raise Invalid(f"{len(raw)} bytes; the limit is {LIMIT}")
    try:
        module = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise Invalid(f"not valid JSON: {error}")
    if not isinstance(module, dict):
        raise Invalid("not a JSON object")
    form = module.get("format")
    if form not in COURSES and form not in LEGACY:
        raise Invalid(f"unknown format {form!r}; use one of {[*sorted(COURSES), *LEGACY]}")
    translations = module.get("translations")
    if not isinstance(translations, dict) or not isinstance(translations.get("en"), dict) \
            or not text(translations["en"].get("title")):
        raise Invalid("no translations.en.title")
    for lang, w in translations.items():
        if not isinstance(w, dict) or not words(w.get("title")) or not words(w.get("guide")):
            raise Invalid(f"translations.{lang} needs a title and a guide")
        intro = w.get("intro")
        if intro is not None and not (isinstance(intro, dict) and words(intro.get("title"))
                                      and words(intro.get("text"))):
            raise Invalid(f"translations.{lang}.intro needs a title and a text")
    animation = module.get("animation")
    if animation is not None:
        clips = [animation.get(k) for k in ("mp4", "webp")] if isinstance(animation, dict) else []
        if (not clips or translations["en"].get("intro") is None
                or not all(isinstance(c, str) and c and len(c) % 4 == 0 and BASE64.fullmatch(c)
                           for c in clips)):
            raise Invalid("animation needs translations.en.intro and base64 mp4 and webp")
    if form in COURSES:
        check_course(module, name)
    else:
        if LEGACY[form] != name:
            raise Invalid(f"a {form} file must be named {LEGACY[form]}.podbag")
        if any(k in module for k in ("id", "port", "steps", "files")):
            raise Invalid(f"a {form} file has no id, port, steps or files")
    return module


def load(folder):
    """[(id, bytes, module)] in catalog order, from FOLDER (site/training)."""
    try:
        source = json.loads((folder / "catalog.json").read_text())
    except (OSError, json.JSONDecodeError) as error:
        raise SystemExit(f"site/training/catalog.json: {error}")
    ids = source.get("modules") if isinstance(source, dict) else None
    if not isinstance(ids, list) or not ids:
        raise SystemExit('site/training/catalog.json: write {"modules": ["<id>", …]}')
    times = source.get("minutes")
    if not isinstance(times, dict):
        raise SystemExit('site/training/catalog.json: write {"minutes": {"<id>": [10, 15]}}')
    modules = []
    for name in ids:
        if not isinstance(name, str) or not ID.fullmatch(name):
            raise SystemExit(f"site/training/catalog.json: bad id {name!r}")
        if any(name == m[0] for m in modules):
            raise SystemExit(f"site/training/catalog.json: {name} is listed twice")
        path = folder / "modules" / f"{name}.podbag"
        if not path.is_file():
            raise SystemExit(f"site/training/catalog.json: no file modules/{name}.podbag")
        minutes = times.get(name)
        if not (isinstance(minutes, list) and 1 <= len(minutes) <= 2
                and all(type(m) is int and 1 <= m <= 240 for m in minutes)
                and minutes == sorted(minutes)):
            raise SystemExit(f"site/training/catalog.json: minutes of {name} must be "
                             "[minutes] or [shortest, longest]")
        raw = path.read_bytes()
        try:
            modules.append((name, raw, check(raw, name), minutes))
        except Invalid as error:
            raise SystemExit(f"site/training/modules/{name}.podbag: {error}")
    return modules


def load_usage(source, langs, kind):
    """SOURCE (site/training/KIND.json, KIND "gui" or "tui") when it is a good list of guides
    and table rows: "pages" for the GUI, "keys" for the TUI."""
    where = f"site/training/{kind}.json"
    guides = source.get("guides") if isinstance(source, dict) else None
    if not isinstance(guides, list) or not guides:
        raise SystemExit(f'{where}: write {{"guides": ["<post slug>", …]}}')
    times = source.get("minutes")
    times = times if isinstance(times, dict) else {}
    for n, slug in enumerate(guides):
        if not isinstance(slug, str) or not ID.fullmatch(slug):
            raise SystemExit(f"{where}: bad guide {slug!r}")
        if slug in guides[:n]:
            raise SystemExit(f"{where}: {slug} is listed twice")
        minutes = times.get(slug)
        if not (type(minutes) is int and 1 <= minutes <= 240):
            raise SystemExit(f"{where}: minutes of {slug} must be a number from 1 to 240")
    table, row_name = ("pages", "page") if kind == "gui" else ("keys", "key")
    rows = source.get(table)
    if not isinstance(rows, list) or not rows:
        raise SystemExit(f'{where}: write {{"{table}": [{{…, "words": {{…}}}}]}}')
    for n, row in enumerate(rows, 1):
        row = row if isinstance(row, dict) else {}
        if kind == "tui":
            names = row.get("keys")
            if not isinstance(names, list) or not names or not all(plain(k) for k in names):
                raise SystemExit(f"{where}: key row {n} needs keys")
        for lang in langs:
            names, words = row.get("names"), row.get("words")
            if kind == "gui" and (not isinstance(names, dict) or not plain(names.get(lang))):
                raise SystemExit(f"{where}: page row {n} has no {lang} name")
            if not isinstance(words, dict) or not plain(words.get(lang)):
                raise SystemExit(f"{where}: {row_name} row {n} has no {lang} words")
    return source


def catalog(modules):
    """The served catalog.json text."""
    entries = [{"id": name, "file": f"modules/{name}.podbag", "sha256": sha256(raw).hexdigest()}
               for name, raw, *_ in modules]
    return json.dumps({"format": CATALOG_FORMAT, "modules": entries}, indent=2) + "\n"


def short_title(title):
    """The title without its "Podbag Training · " or "Lab · " start."""
    _, sep, rest = title.partition(" · ")
    return rest if sep else title


class Hub:
    """Writes /training/gui/ (the GUI guide), /training/ (GUI practice) and /training/tui/
    (the TUI guide) in each language, with the blog's layout."""

    def __init__(self, out, site, words, modules, usage):
        self.out, self.site, self.words, self.modules = out, site, words, modules
        self.usage = usage  # {"gui": gui.json, "tui": tui.json}
        self.pages = blog.Builder(out, site, words)

    def path(self, lang):
        return self.site.path_of(lang) + "training/"

    def usage_path(self, kind):
        """The address of the KIND ("gui" or "tui") guide in a language."""
        return lambda lang: self.path(lang) + f"{kind}/"

    def time(self, minutes, w):
        if len(minutes) == 1:
            return w["training_time"].replace("{n}", str(minutes[0]))
        return (w["training_time_range"].replace("{min}", str(minutes[0]))
                .replace("{max}", str(minutes[1])))

    def card(self, kind, name, title, post, href, facts, root, extra=""):
        """A card like the blog's lists: POST's picture, then TITLE and the post's summary."""
        src, size = self.pages.image_url(post, root)
        dims = f' width="{size[0]}" height="{size[1]}"' if size else ""
        sep = '<span class="sep" aria-hidden="true">|</span>'
        return (f'<li class="post-card {kind} reveal" id="{name}">'
                f'<a class="thumb" href="{href}" tabindex="-1" aria-hidden="true">'
                f'<img src="{src}" alt=""{dims} loading="lazy"></a>'
                f'<div class="post-text"><h3 class="post-title"><a href="{href}">'
                f'{html.escape(title)}</a></h3>'
                f'<p class="meta">{sep.join(f"<span>{f}</span>" for f in facts)}</p>'
                f'<p class="summary">{blog.inline(post.summary, post.lang)}</p>'
                f"{extra}</div></li>")

    def guide(self, name, module, lang, root):
        """The guide's address from the page."""
        if module["format"] in COURSES:
            words = module["translations"].get(lang) or {}
            url = words.get("url") or module["translations"]["en"]["url"]
            return root + url[len(GUIDE_SITE):]
        slug = LEGACY_GUIDES[name]
        local = self.site.path_of(lang) + f"blog/{slug}/"
        if (self.out / local / "index.html").is_file():
            return root + local
        return root + f"blog/{slug}/"

    def item(self, name, module, minutes, lang, root, w):
        words = module["translations"].get(lang) or {}
        title = short_title(words.get("title") or module["translations"]["en"]["title"])
        facts = [self.time(minutes, w),
                 f'<a href="{root}training/modules/{name}.podbag" download>{w["training_download"]}</a>']
        start = blog.code_block(f"podbag lab start {name}", "sh", lang, blog.copy_button(w))
        return self.card("module", name, title, self.post(name, module, lang),
                         self.guide(name, module, lang, root), facts, root, start)

    def post(self, name, module, lang):
        """The module's guide post in LANG, or in English when it has none."""
        if module["format"] in COURSES:
            slug = module["translations"]["en"]["url"].rstrip("/").rsplit("/", 1)[1]
        else:
            slug = LEGACY_GUIDES[name]
        return self.find(slug, lang, f"{name}: no guide post {slug}")

    def find(self, slug, lang, missing):
        """The blog post SLUG in LANG, or in English when it has none."""
        for code in (lang, "en"):
            for post in self.pages.posts[code]:
                if post.slug == slug:
                    return post
        raise SystemExit(missing)

    def side(self, lang, w, root):
        install = blog.code_block("curl -fsSL https://podbag.dev/install.sh | sh",
                                  "sh", lang, blog.copy_button(w))
        guides = root + self.site.path_of(lang) + "blog/category/how-to/"
        return (f'<aside class="side" aria-label="{blog.attr(w["training_side"])}">'
                f'<section class="side-box"><h2>{w["blog_get"]}</h2>{install}'
                f'<p class="note">{w["blog_get_note"]}</p></section>'
                f'<section class="side-box"><h2>{w["blog_resources"]}</h2><ul>'
                f'<li><a href="{guides}">{w["training_guides"]}</a></li>'
                f'<li><a href="https://github.com/SteelCrab/podbag/releases">{w["footer_releases"]}</a></li>'
                f"</ul></section></aside>")

    def band(self, lang, w, root, current, lead):
        """The title, LEAD and the three tabs: the GUI guide, GUI practice and the TUI guide
        (CURRENT: 0, 1 or 2)."""
        tabs = [(root + self.usage_path("gui")(lang), w["training_tab_gui_usage"]),
                (root + self.path(lang), w["training_tab_gui"]),
                (root + self.usage_path("tui")(lang), w["training_tab_tui"])]
        nav = "".join(f'<a href="{h}"{" aria-current=\"page\"" if n == current else ""}>{label}</a>'
                      for n, (h, label) in enumerate(tabs))
        return (f'<div class="band training-band"><div class="wrap">'
                f'<h1 class="band-title">{w["training_title"]}</h1>'
                f'<p class="band-sub">{lead}</p>'
                f'<nav class="band-nav" aria-label="{blog.attr(w["training_tabs"])}">{nav}</nav>'
                f"</div></div>")

    def write(self, lang, path_of, title, description, band, content):
        w = self.words[lang]
        path = path_of(lang)
        root = "../" * path.count("/")
        paths = {c: path_of(c) for c in self.pages.langs}
        title, description = blog.strip(title), blog.strip(description)
        url = self.site.URL + path
        image = self.site.URL + "images/logo.png"
        self.pages.page(lang, path, {
            "targets": paths, "page_title": title, "page_description": description,
            "alternates": self.pages.alternates(paths),
            "social": self.pages.social("website", url, title, description, image,
                                        blog.image_size(self.pages.pictures / "logo.png"), "", lang),
            "blog_current": "", "training_current": ' aria-current="true"',
            "band": band, "content": content, "side": self.side(lang, w, root),
        })

    def page(self, lang):
        w = self.words[lang]
        root = "../" * self.path(lang).count("/")
        items = "".join(self.item(name, module, minutes, lang, root, w)
                        for name, _, module, minutes in self.modules)
        listing = blog.code_block("podbag lab list", "sh", lang, blog.copy_button(w))
        content = (f'<div class="training">'
                   f'<p>{w["training_refresh"]}</p><p>{w["training_cli"]}</p>{listing}'
                   f'<h2 class="list-title">{w["training_modules"]}</h2>'
                   f'<ul class="modules" role="list">{items}</ul>'
                   f'<h2 class="list-title">{w["training_outside_title"]}</h2>'
                   f'<p>{w["training_outside"]}</p></div>')
        self.write(lang, self.path, w["training_title"], w["training_description"],
                   self.band(lang, w, root, 1, w["training_lead"]), content)

    def usage_page(self, lang, kind):
        """/training/KIND/: how to start the GUI or the TUI, a table of its pages or keys and
        its guides as cards."""
        w, usage, path_of = self.words[lang], self.usage[kind], self.usage_path(kind)
        root = "../" * path_of(lang).count("/")
        items = []
        for slug in usage["guides"]:
            post = self.find(slug, lang, f"site/training/{kind}.json: no blog post {slug}")
            items.append(self.card("guide", slug, short_title(post.title), post,
                                   root + self.pages.post_path(post),
                                   [self.time([usage["minutes"][slug]], w)], root))
        if kind == "tui":
            start = blog.code_block("podbag tui", "sh", lang, blog.copy_button(w))
            table, head = "keys", (w["tui_keys"], w["tui_key"], w["tui_action"])
            rows = ["<tr><td>" + " ".join(f"<kbd>{html.escape(k)}</kbd>" for k in row["keys"])
                    + f'</td><td>{html.escape(row["words"][lang])}</td></tr>' for row in usage["keys"]]
        else:
            start = ""
            table, head = "keys pages", (w["gui_pages"], w["gui_page"], w["gui_action"])
            rows = [f'<tr><td>{html.escape(row["names"][lang])}</td>'
                    f'<td>{html.escape(row["words"][lang])}</td></tr>' for row in usage["pages"]]
        content = (f'<div class="training">'
                   f'<p>{w[f"{kind}_intro"]}</p>{start}'
                   f'<h2 class="list-title">{head[0]}</h2>'
                   f'<table class="{table}"><thead><tr><th scope="col">{head[1]}</th>'
                   f'<th scope="col">{head[2]}</th></tr></thead><tbody>{"".join(rows)}</tbody></table>'
                   f'<h2 class="list-title">{w[f"{kind}_guides"]}</h2>'
                   f'<ul class="modules" role="list">{"".join(items)}</ul></div>')
        self.write(lang, path_of, w[f"{kind}_title"], w[f"{kind}_description"],
                   self.band(lang, w, root, {"gui": 0, "tui": 2}[kind], w[f"{kind}_lead"]), content)


def build(out, site, words):
    """Check the modules and write the catalog and the pages into OUT; return the module count."""
    modules = load(site.SITE / "training")
    target = out / "training" / "modules"
    target.mkdir(parents=True, exist_ok=True)
    for name, raw, *_ in modules:
        (target / f"{name}.podbag").write_bytes(raw)
    (out / "training" / "catalog.json").write_text(catalog(modules))
    usage = {}
    for kind in ("gui", "tui"):
        try:
            source = json.loads((site.SITE / "training" / f"{kind}.json").read_text())
        except (OSError, json.JSONDecodeError) as error:
            raise SystemExit(f"site/training/{kind}.json: {error}")
        usage[kind] = load_usage(source, [code for code, _ in site.LANGS], kind)
    hub = Hub(out, site, words, modules, usage)
    for code, _ in site.LANGS:
        hub.usage_page(code, "gui")
        hub.page(code)
        hub.usage_page(code, "tui")
    return len(modules)
