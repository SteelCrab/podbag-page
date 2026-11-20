"""Tests for the blog: the Markdown converter, front matter, and the built pages.

usage: python3 -m unittest dev/docs/test_blog.py
"""
import importlib.util
import json
import re
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path
from xml.etree import ElementTree

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import blog  # noqa: E402
import check_links  # noqa: E402


def md(text, **options):
    return blog.markdown(text, **options)


class Blocks(unittest.TestCase):
    def test_paragraphs(self):
        self.assertEqual(md("One line\nand the next.\n\nTwo."),
                         "<p>One line and the next.</p>\n<p>Two.</p>")

    def test_paragraph_lines_join_without_space_in_japanese_and_chinese(self):
        self.assertEqual(md("一行目\n二行目", lang="ja"), "<p>一行目二行目</p>")
        self.assertEqual(md("첫 줄\n둘째 줄", lang="ko"), "<p>첫 줄 둘째 줄</p>")

    def test_headings_get_ids_and_start_at_h2(self):
        out = md("# Top\n\n## Start time and memory\n\n### Why?\n\n## Start time and memory")
        self.assertIn('<h2 id="top">Top</h2>', out)
        self.assertIn('<h2 id="start-time-and-memory">Start time and memory</h2>', out)
        self.assertIn('<h3 id="why">Why?</h3>', out)
        self.assertIn('<h2 id="start-time-and-memory-2">', out)

    def test_heading_with_own_id_and_unicode(self):
        self.assertEqual(md("## 설치 {#install}"), '<h2 id="install">설치</h2>')
        self.assertEqual(md("## 데몬 없음"), '<h2 id="데몬-없음">데몬 없음</h2>')

    def test_lists(self):
        self.assertEqual(md("- a\n- b *c*"), "<ul>\n<li>a</li>\n<li>b <em>c</em></li>\n</ul>")
        self.assertEqual(md("1. one\n2. two"), "<ol>\n<li>one</li>\n<li>two</li>\n</ol>")
        self.assertEqual(md("3. three\n4. four"),
                         '<ol start="3">\n<li>three</li>\n<li>four</li>\n</ol>')

    def test_nested_and_loose_lists(self):
        out = md("- a\n  - b\n  - c\n- d")
        self.assertEqual(out, "<ul>\n<li>a\n<ul>\n<li>b</li>\n<li>c</li>\n</ul></li>\n<li>d</li>\n</ul>")
        self.assertEqual(md("- a\n\n- b"), "<ul>\n<li><p>a</p></li>\n<li><p>b</p></li>\n</ul>")

    def test_list_item_continues_on_next_lines(self):
        self.assertEqual(md("- one\n  more\n- two"), "<ul>\n<li>one more</li>\n<li>two</li>\n</ul>")

    def test_list_after_paragraph(self):
        self.assertEqual(md("Text:\n- a"), "<p>Text:</p>\n<ul>\n<li>a</li>\n</ul>")

    def test_fenced_code_is_escaped_and_gets_the_button(self):
        out = md("```sh\necho '<b>' && x={{a}}\n```", code_button="<button>Copy</button>")
        self.assertEqual(out, '<div class="code"><pre><code class="language-sh">echo \'&lt;b&gt;\' '
                              '&amp;&amp; x=&#123;&#123;a}}</code></pre><button>Copy</button></div>')

    def test_fenced_code_keeps_markdown_as_text(self):
        out = md("~~~\n# not a heading\n- not a list\n~~~")
        self.assertIn("# not a heading\n- not a list", out)
        self.assertNotIn("<h", out.replace("<div", ""))

    def test_blockquote_and_rule(self):
        self.assertEqual(md("> quoted **text**\n> more\n\n---"),
                         "<blockquote>\n<p>quoted <strong>text</strong> more</p>\n</blockquote>\n<hr>")

    def test_table_with_alignment_and_row_headers(self):
        out = md("| | podbag | Docker |\n|---|--:|:-:|\n| Disk | {{n:902}} MiB | `a|b` |")
        self.assertIn('<th scope="col" style="text-align: right">podbag</th>', out)
        self.assertIn('<th scope="row">Disk</th>', out)
        self.assertIn('<td style="text-align: right">902 MiB</td>', out)
        self.assertIn('<td style="text-align: center"><code>a|b</code></td>', out)
        self.assertTrue(out.startswith('<div class="table-wrap"><table>'))

    def test_table_without_empty_corner_has_no_row_headers(self):
        out = md("| System | File |\n|---|---|\n| Linux | `x` |")
        self.assertIn("<td>Linux</td>", out)
        self.assertNotIn('scope="row"', out)

    def test_comparisons_use_raw_values_and_keep_the_localized_table_for_feeds(self):
        columns = ("<!-- compare-columns: podbag docker -->\n"
                   "| | podbag | Docker | Savings |\n|---|---:|---:|---:|\n"
                   "| Disk | {{n:902}} MiB | {{n:2970}} MiB | 70% |\n"
                   "| Cache | {{n:324}} MiB | {{n:982}} MiB | 67% |")
        article = md(columns, lang="es", root="../../", table_label="Tabla")
        self.assertIn('name="article-metric-1"', article)
        self.assertIn('width:30.3704%', article)
        self.assertIn('<strong>2.970 MiB</strong>', article)
        self.assertIn('<summary>Tabla</summary>', article)
        self.assertIn("70%", article)
        feed = md(columns, lang="es")
        self.assertIn("<table>", feed)
        self.assertNotIn("compare-columns", feed)
        self.assertNotIn("fieldset", feed)

    def test_comparison_with_products_in_rows(self):
        article = md("<!-- compare-rows: podbag docker -->\n"
                     "| Engine | Seconds |\n|---|---:|\n"
                     "| podbag | {{n:0}} |\n| Docker | {{n:9.05}} |", table_label="Data")
        self.assertIn("comparison-card", article)
        self.assertIn("width:0.0000%", article)
        self.assertIn("<strong>9.05</strong>", article)

    def test_image_alone_is_a_figure_with_caption(self):
        out = md('![A chart](/images/perf.svg "The *numbers*")', root="../../")
        self.assertEqual(out, '<figure><img src="../../images/perf.svg" alt="A chart" loading="lazy">'
                              "<figcaption>The <em>numbers</em></figcaption></figure>")

    def test_figure_uses_picture_sources(self):
        def picture(src):
            return [("(prefers-color-scheme: dark)", src.replace("-light", "-dark"))], (800, 490)
        out = md("![x](/images/a-light.svg)", root="", picture=picture)
        self.assertEqual(out, '<figure><picture><source media="(prefers-color-scheme: dark)" '
                              'srcset="images/a-dark.svg"><img src="images/a-light.svg" alt="x" '
                              'width="800" height="490" loading="lazy"></picture></figure>')


class Inline(unittest.TestCase):
    def inline(self, text, **options):
        return blog.Markdown(**options).inline(text)

    def test_emphasis_and_code(self):
        self.assertEqual(self.inline("**bold**, *em*, _em_ and `a*b*`"),
                         "<strong>bold</strong>, <em>em</em>, <em>em</em> and <code>a*b*</code>")

    def test_underscores_inside_words_stay(self):
        self.assertEqual(self.inline("x86_64 and snake_case_name"), "x86_64 and snake_case_name")

    def test_emphasis_next_to_cjk(self):
        self.assertEqual(self.inline("**데몬 없음.** 실행"), "<strong>데몬 없음.</strong> 실행")

    def test_html_is_escaped(self):
        self.assertEqual(self.inline('<script>alert("x")</script> & co'),
                         '&lt;script&gt;alert("x")&lt;/script&gt; &amp; co')

    def test_backslash_escapes(self):
        self.assertEqual(self.inline(r"\*not em\* and \`tick\`"), "*not em* and `tick`")

    def test_links(self):
        self.assertEqual(self.inline('[the *docs*](https://example.com/a?b=1&c=2 "Docs")'),
                         '<a href="https://example.com/a?b=1&amp;c=2" title="Docs">the <em>docs</em></a>')
        self.assertEqual(self.inline("<https://podbag.dev>"),
                         '<a href="https://podbag.dev">https://podbag.dev</a>')

    def test_site_links_are_written_from_the_root(self):
        self.assertEqual(self.inline("[v](/media/intro.mp4)", root="../../"),
                         '<a href="../../media/intro.mp4">v</a>')
        self.assertEqual(self.inline("[v](/media/intro.mp4)", root="https://podbag.dev/"),
                         '<a href="https://podbag.dev/media/intro.mp4">v</a>')
        self.assertEqual(self.inline("[c](card.png)", root="../../../", base="/blog/x/"),
                         '<a href="../../../blog/x/card.png">c</a>')
        self.assertEqual(self.inline("[top](#install)", root="../"), '<a href="#install">top</a>')

    def test_numbers_follow_the_language(self):
        self.assertEqual(self.inline("{{n:2970}} MiB, {{n:4.1}} ms"), "2,970 MiB, 4.1 ms")
        self.assertEqual(self.inline("{{n:2970}} MiB, {{n:4.1}} ms", lang="es"), "2.970 MiB, 4,1 ms")
        self.assertEqual(self.inline("{{n:2970}}", lang="vi"), "2.970")
        self.assertEqual(self.inline("`{{n:1}}`"), "<code>&#123;&#123;n:1}}</code>")


class FrontMatter(unittest.TestCase):
    def test_values(self):
        meta, body = blog.front_matter(
            '---\ntitle: "podbag 0.1.0: out"\ndate: 2026-11-20\ntags: [a, "b, c"]\n'
            "draft: false\n# a comment\nsummary: x # y\n---\nBody\n")
        self.assertEqual(meta, {"title": "podbag 0.1.0: out", "date": "2026-11-20",
                                "tags": ["a", "b, c"], "draft": False, "summary": "x # y"})
        self.assertEqual(body, "Body\n")

    def test_errors(self):
        with self.assertRaises(ValueError):
            blog.front_matter("no front matter")
        with self.assertRaises(ValueError):
            blog.front_matter("---\ntitle: x\n")
        with self.assertRaises(ValueError):
            blog.front_matter("---\nnot a pair\n---\n")

    def write(self, folder, name, text):
        path = Path(folder) / "a-post" / name
        path.parent.mkdir(exist_ok=True)
        path.write_text(text)
        return path

    POST = ("---\ntitle: T\ndate: 2026-11-20\nauthor: team\ncategories: [announcements]\n"
            "summary: S\n{extra}---\nBody\n")

    def test_drafts_are_left_out(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self.write(tmp, "en.md", self.POST.format(extra="draft: true\n"))
            self.assertIsNone(blog.load(path, ["en"], {"team": {}}))
            self.write(tmp, "ko.md", self.POST.format(extra=""))
            posts = blog.load_all(Path(tmp), ["en", "ko"], {"team": {}})
            self.assertEqual(posts["en"], [])
            self.assertEqual([p.lang for p in posts["ko"]], ["ko"])
            self.assertEqual(posts["ko"][0].day, date(2026, 11, 20))

    def test_bad_posts_stop_the_build(self):
        with tempfile.TemporaryDirectory() as tmp:
            for extra in ["image: x.png\n", "colour: red\n"]:
                path = self.write(tmp, "en.md", self.POST.format(extra=extra))
                with self.assertRaises(SystemExit):
                    blog.load(path, ["en"], {"team": {}})
            path = self.write(tmp, "en.md", self.POST.replace("announcements", "news").format(extra=""))
            with self.assertRaises(SystemExit):
                blog.load(path, ["en"], {"team": {}})


class Helpers(unittest.TestCase):
    def post(self, slug, day, categories, tags):
        return blog.Post(slug, "en", slug, date(2026, 11, day), "team", categories, tags, "", "",
                         "", "")

    def test_related_prefers_shared_categories_then_tags(self):
        a = self.post("a", 1, ["announcements"], ["x"])
        b = self.post("b", 2, ["engineering"], ["x"])
        c = self.post("c", 3, ["announcements"], [])
        d = self.post("d", 4, ["how-to"], [])
        self.assertEqual([p.slug for p in blog.related(a, [a, b, c, d])], ["c", "b"])

    def test_dates(self):
        day = date(2026, 11, 20)
        self.assertEqual(blog.format_date(day, "en"), "20 Nov 2026")
        self.assertEqual(blog.format_date(day, "ko"), "2026년 11월 20일")
        self.assertEqual(blog.format_date(day, "zh-CN"), "2026年11月20日")
        self.assertEqual(blog.format_date(day, "es"), "20 de noviembre de 2026")
        self.assertEqual(blog.format_date(day, "fil"), "Nobyembre 20, 2026")
        self.assertEqual(blog.format_date(day, "vi"), "20 tháng 11, 2026")


class Built(unittest.TestCase):
    """Build the whole site once and look at the blog pages."""

    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location("podbag_site", HERE / "site.py")
        cls.site = importlib.util.module_from_spec(spec)
        sys.modules["podbag_site"] = cls.site
        spec.loader.exec_module(cls.site)
        cls.tmp = tempfile.TemporaryDirectory()
        cls.out = Path(cls.tmp.name) / "site"
        argv = sys.argv
        sys.argv = ["site.py", str(cls.out)]
        try:
            cls.site.main()
        finally:
            sys.argv = argv

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def pages(self):
        return [p for p in self.out.rglob("*.html")]

    def test_no_placeholder_is_left(self):
        for page in self.pages():
            self.assertNotIn("{{", page.read_text(), page)

    def test_no_broken_links(self):
        problems, count = check_links.check(self.out)
        self.assertEqual(problems, [])
        self.assertGreater(count, 100)

    def test_link_checker_finds_a_broken_link(self):
        page = self.out / "blog/index.html"
        text = page.read_text()
        try:
            page.write_text(text.replace("</main>", '<a href="nowhere/">x</a><a href="#none">y</a></main>'))
            problems, _ = check_links.check(self.out)
            self.assertEqual(len(problems), 2, problems)
        finally:
            page.write_text(text)

    def test_every_language_has_index_categories_feed(self):
        for code, _ in self.site.LANGS:
            base = self.out / self.site.path_of(code) / "blog"
            self.assertTrue((base / "index.html").exists(), code)
            self.assertTrue((base / "feed.xml").exists(), code)
            for category in blog.CATEGORIES:
                self.assertTrue((base / "category" / category / "index.html").exists())

    def test_feeds_are_rss(self):
        for feed in self.out.rglob("feed.xml"):
            root = ElementTree.parse(feed).getroot()
            self.assertEqual(root.tag, "rss")
            for item in root.iter("item"):
                self.assertTrue(item.findtext("link").startswith("https://podbag.dev/"))

    def test_post_page_has_search_and_sharing_tags(self):
        page = (self.out / "ko/blog/podbag-0-1-0/index.html").read_text()
        self.assertIn('<link rel="canonical" href="https://podbag.dev/ko/blog/podbag-0-1-0/">', page)
        self.assertIn('hreflang="en" href="https://podbag.dev/blog/podbag-0-1-0/"', page)
        self.assertIn('hreflang="x-default" href="https://podbag.dev/blog/podbag-0-1-0/"', page)
        self.assertIn('<meta property="og:type" content="article">', page)
        self.assertIn('content="https://podbag.dev/blog/podbag-0-1-0/card-ko.png"', page)
        self.assertIn('<meta name="twitter:card" content="summary_large_image">', page)
        self.assertIn('type="application/rss+xml"', page)
        data = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', page,
                                    re.S).group(1))
        self.assertEqual(data["@type"], "BlogPosting")
        self.assertEqual(data["inLanguage"], "ko")

    def test_github_author_and_team_byline(self):
        authors = json.loads((self.site.SITE / "blog/authors.json").read_text())
        langs = [code for code, _ in self.site.LANGS]
        posts = blog.load_all(self.site.SITE / "blog/posts", langs, authors)
        for code in langs:
            base = self.out / self.site.path_of(code) / "blog"
            team = authors["team"][code]["name"]
            credited = [p for p in posts[code] if p.author in ("team", "steelcrab")]
            pages = [("index.html", len(credited), any(p.author == "team" for p in credited))]
            pages.extend((f"{p.slug}/index.html", 2, p.author == "team") for p in credited)
            for path, count, show_team in pages:
                page = (base / path).read_text()
                links = re.findall(r'<a class="github-byline"[^>]* href="https://github.com/SteelCrab">'
                                   r'(.*?)</a>', page)
                self.assertEqual(len(links), count, (code, path))
                for contents in links:
                    self.assertIn('logos/steelcrab.png"', contents)
                    self.assertIn('logos/github.svg"', contents)
                    self.assertIn("<span>@SteelCrab</span>", contents)
                if show_team:
                    self.assertIn(team, page)

            creator = "{http://purl.org/dc/elements/1.1/}creator"
            items = ElementTree.parse(base / "feed.xml").findall(".//item")
            creators = {i.findtext("link"): i.findtext(creator) for i in items}
            for slug, name in [("compose-stop-timeout", "@SteelCrab"), ("podbag-0-1-0", team)]:
                url = self.site.URL + self.site.path_of(code) + f"blog/{slug}/"
                self.assertEqual(creators[url], name)

    def test_tutorial_download_and_steps(self):
        slug = "volume-api-lab"
        assets = self.out / "blog" / slug
        module = json.loads((assets / "volume-api.podbag").read_text())
        self.assertEqual(module["format"], "podbag-volume-api-lab-v1")
        self.assertIsInstance(json.loads(module["starter"]), dict)
        for code, _ in self.site.LANGS:
            post = self.out / self.site.path_of(code) / "blog" / slug / "index.html"
            html = post.read_text()
            self.assertIn(code, module["translations"])
            link, = re.findall(r'<a href="([^"]+volume-api\.podbag)"', html)
            self.assertTrue((post.parent / link).samefile(assets / "volume-api.podbag"))
            pictures = re.findall(r'<figure><img src="([^"]+)" alt="([^"]+)"', html)
            self.assertEqual(len(pictures), 9)
            for index, (src, alt) in enumerate(pictures, 1):
                path = post.parent / src
                self.assertTrue(path.is_file() and alt)
                self.assertTrue(path.name.startswith(f"{index:02}-") and path.name.endswith(f"-{code}.png"))

    def test_numbers_in_spanish_post(self):
        page = (self.out / "es/blog/podbag-0-1-0/index.html").read_text()
        self.assertIn("2.970 MiB", page)
        self.assertIn("4,1 ms", page)

    def test_headings_in_order(self):
        for page in self.out.rglob("blog/**/index.html"):
            levels = [int(n) for n in re.findall(r"<h([1-6])[ >]", page.read_text())]
            self.assertLessEqual(levels.count(1), 1, page)
            for before, after in zip(levels, levels[1:]):
                self.assertLessEqual(after, before + 1, page)

    def test_images_have_alt(self):
        for page in self.pages():
            for tag in re.findall(r"<img\b[^>]*>", page.read_text()):
                self.assertIn(" alt=", tag, page)

    def test_home_links_to_the_blog(self):
        page = (self.out / "index.html").read_text()
        self.assertIn('<a href="blog/">Blog</a>', page)
        self.assertIn('href="blog/feed.xml"', page)


if __name__ == "__main__":
    unittest.main()
