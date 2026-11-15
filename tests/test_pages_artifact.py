"""Exercise the exact directory configured for the Pages artifact over HTTP."""

import functools
from html.parser import HTMLParser
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import re
import threading
from urllib.error import HTTPError
from urllib.request import urlopen
import unittest


ROOT = Path(__file__).resolve().parents[1]
INSTAGRAM_PROFILE = "https://www.instagram.com/domenico.massafraa/"
PROMISE = "Faccio lavorare gli agenti AI su problemi veri."
LEDE = "Ti mostro cosa funziona, anche se non programmi."
PAYOFF = "Non devi saper programmare. Devi capirne abbastanza."
PORTRAIT_ALT = "Ritratto pubblicato sul profilo Instagram di Domenico Massafra"
BADGES = {"Sì", "Dipende", "No"}
# Owner brand canon (BRAND.md). Any other value is off-palette.
CANON_TOKENS = {
    "--carbon": "#0b0b0d",
    "--paper": "#f5f0e8",
    "--signal": "#d63f28",
    "--signal-bright": "#ff5a3c",
    "--ash": "#9a948b",
    "--graphite": "#66615b",
}
PUBLIC_FILES = {
    ".nojekyll",
    "index.html",
    "styles.css",
    "app.js",
    "icons.svg",
    "ritratto-instagram.jpg",
    "strumentini-mark.svg",
    "dichiarazioni-mark.svg",
    "favicon.svg",
    "share.png",
    "fonts/archivo.woff2",
    "fonts/jetbrains-mono.woff2",
    "fonts/OFL.txt",
    "robots.txt",
    "sitemap.xml",
}


def root_tokens(css):
    match = re.search(r":root\{([^}]*)\}", css)
    if match is None:
        raise AssertionError("styles.css must declare its tokens in :root")
    return dict(re.findall(r"(--[a-z-]+):(#[0-9a-f]{6})", match.group(1)))


class Element:
    def __init__(self, tag, attrs):
        self.tag = tag
        self.attrs = attrs
        self.children = []  # Element or str

    @property
    def classes(self):
        return (self.attrs.get("class") or "").split()

    def find_all(self, tag=None, cls=None, attr=None):
        found = []
        for child in self.children:
            if isinstance(child, Element):
                if (tag is None or child.tag == tag) and (cls is None or cls in child.classes) and (attr is None or attr in child.attrs):
                    found.append(child)
                found += child.find_all(tag, cls, attr)
        return found

    def text(self):
        parts = []
        for child in self.children:
            if isinstance(child, str):
                parts.append(child)
            elif child.tag not in ("script", "style"):
                parts.append(child.text())
        return " ".join(" ".join(parts).split())


class TreeBuilder(HTMLParser):
    """Turn the page into a small element tree, so tests read structure instead of regexes."""

    VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}

    def __init__(self):
        super().__init__()
        self.root = Element("#document", {})
        self.stack = [self.root]

    def handle_starttag(self, tag, attrs):
        element = Element(tag, dict(attrs))
        self.stack[-1].children.append(element)
        if tag not in self.VOID:
            self.stack.append(element)

    def handle_startendtag(self, tag, attrs):
        self.stack[-1].children.append(Element(tag, dict(attrs)))

    def handle_endtag(self, tag):
        for index in range(len(self.stack) - 1, 0, -1):
            if self.stack[index].tag == tag:
                del self.stack[index:]
                return

    def handle_data(self, data):
        self.stack[-1].children.append(data)


def parse(html):
    builder = TreeBuilder()
    builder.feed(html)
    builder.close()
    return builder.root


def relative_luminance(hex_colour):
    def channel(value):
        value = value / 255
        return value / 12.92 if value <= 0.03928 else ((value + 0.055) / 1.055) ** 2.4

    red, green, blue = (int(hex_colour[i : i + 2], 16) for i in (1, 3, 5))
    return 0.2126 * channel(red) + 0.7152 * channel(green) + 0.0722 * channel(blue)


def contrast_ratio(foreground, background):
    light, dark = sorted(
        (relative_luminance(foreground), relative_luminance(background)), reverse=True
    )
    return (light + 0.05) / (dark + 0.05)


def artifact_directory():
    workflow = (ROOT / ".github/workflows/pages.yml").read_text()
    match = re.search(
        r"uses:\s*actions/upload-pages-artifact@v\d+\s*\n\s*with:\s*\n\s*path:\s*([^\s#]+)",
        workflow,
    )
    if match is None:
        raise AssertionError("Pages upload path must be explicit")
    path = (ROOT / match.group(1)).resolve()
    if not path.is_relative_to(ROOT):
        raise AssertionError("Pages upload must come from the repository")
    return path


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *_args):
        pass


class PagesArtifactTest(unittest.TestCase):
    def setUp(self):
        self.site = artifact_directory()
        self.html = (self.site / "index.html").read_text()
        self.css = (self.site / "styles.css").read_text()
        self.page = parse(self.html)
        self.threads = self.page.find_all("article", cls="thread")

    def test_only_the_public_files_are_uploaded(self):
        workflow = (ROOT / ".github/workflows/pages.yml").read_text()
        self.assertRegex(workflow, r"(?m)^\s*include-hidden-files:\s*true\s*$")
        self.assertEqual(
            {p.relative_to(self.site).as_posix() for p in self.site.rglob("*") if p.is_file()},
            PUBLIC_FILES,
        )

    def test_every_conversation_is_complete_and_its_links_lead_somewhere(self):
        self.assertEqual(len(self.page.find_all("h1")), 1)
        self.assertEqual(len(self.threads), 10)
        ids = [thread.attrs.get("id") for thread in self.threads]
        self.assertEqual(len(set(ids)), len(ids), f"duplicate conversation id in {ids}")
        self.assertEqual(ids[0], "chi-sono")
        self.assertIn("contatto", ids)

        for thread in self.threads:
            name = thread.attrs.get("id")
            with self.subTest(thread=name):
                self.assertTrue(name, "a conversation has no id")
                self.assertTrue((thread.attrs.get("data-group") or "").strip(), "data-group is empty")
                self.assertTrue((thread.attrs.get("data-keys") or "").strip(), "data-keys is empty")
                if "data-badge" in thread.attrs:
                    self.assertIn(thread.attrs["data-badge"], BADGES)

                asks = thread.find_all("h2", cls="ask")
                self.assertEqual(len(asks), 1)
                self.assertTrue(asks[0].text(), "the question is empty")

                runs = thread.find_all("details", cls="run")
                self.assertEqual(len(runs), 1)
                self.assertEqual(len(runs[0].find_all("summary")), 1)
                self.assertGreaterEqual(len(runs[0].find_all("li")), 1)

                replies = [div for div in thread.find_all("div", cls="reply")]
                self.assertEqual(len(replies), 1)
                self.assertTrue(replies[0].text(), "the answer is empty")

                nexts = thread.find_all("nav", cls="next")
                self.assertEqual(len(nexts), 1)
                self.assertGreaterEqual(len(nexts[0].find_all("a")), 2)

        # Guard for copy edited by hand: every suggested follow-up opens a real conversation.
        for nav in self.page.find_all("nav", cls="next"):
            for link in nav.find_all("a"):
                href = link.attrs.get("href", "")
                if href.startswith("#"):
                    with self.subTest(link=href, text=link.text()):
                        self.assertIn(href[1:], ids, f"suggested link {href} («{link.text()}») points to no conversation")

        contact = self.threads[ids.index("contatto")]
        handoffs = [a for a in contact.find_all("a", attr="data-handoff") if a.attrs.get("href") == INSTAGRAM_PROFILE]
        self.assertEqual(len(handoffs), 1, "the contatto conversation must hand off to the Instagram profile")

    def test_public_homepage_keeps_owner_copy_brand_and_real_portrait(self):
        text = self.page.text()
        for phrase in ("Domenico Massafra", PROMISE, LEDE, PAYOFF, "se disponibile"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

        hrefs = {a.attrs.get("href") for a in self.page.find_all("a")}
        for url in (INSTAGRAM_PROFILE, "https://strumentini.it/", "https://dichiarazionipubbliche.it/", "https://github.com/domenicomassafra"):
            with self.subTest(link=url):
                self.assertIn(url, hrefs)

        portraits = [img for img in self.page.find_all("img") if img.attrs.get("src") == "/ritratto-instagram.jpg"]
        self.assertTrue(portraits)
        self.assertIn(PORTRAIT_ALT, [img.attrs.get("alt") for img in portraits])
        theme = [m for m in self.page.find_all("meta") if m.attrs.get("name") == "theme-color"]
        self.assertEqual([m.attrs.get("content") for m in theme], ["#0b0b0d"])
        self.assertIn("prefers-reduced-motion", self.css)
        self.assertIn("color-scheme:dark", self.css)

        for forbidden in ("mailto:", "instagram.com/direct/", "ig.me/", "PROTOTIPO NON PUBBLICO"):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, self.html)
        self.assertEqual(self.page.find_all("form"), [])

        photo = (self.site / "ritratto-instagram.jpg").read_bytes()
        self.assertGreater(len(photo), 1000)
        self.assertTrue(photo.startswith(b"\xff\xd8"))
        sources = {img.attrs.get("src") for img in self.page.find_all("img")}
        for mark in ("strumentini-mark.svg", "dichiarazioni-mark.svg"):
            self.assertIn(f"/{mark}", sources)
            self.assertIn("<svg", (self.site / mark).read_text())

        # Social previews use the local share image.
        og = [m for m in self.page.find_all("meta") if m.attrs.get("property") == "og:image"]
        self.assertEqual([m.attrs.get("content") for m in og], ["https://domenicomassafra.it/share.png"])
        self.assertTrue((self.site / "share.png").read_bytes().startswith(b"\x89PNG\r\n\x1a\n"))

    def test_page_reads_without_the_script(self):
        # The inline script adds class «app»; in the source the page must start as a plain list.
        html_tag = self.page.find_all("html")[0]
        self.assertNotIn("class", html_tag.attrs)
        self.assertIn("html:not(.app)", self.css)

        composer = self.page.find_all("div", cls="composer")
        self.assertEqual(len(composer), 1)
        self.assertIn("only-app", composer[0].classes)
        for attr in ("data-menu", "data-new"):
            buttons = self.page.find_all("button", attr=attr)
            with self.subTest(button=attr):
                self.assertEqual(len(buttons), 1)
                self.assertIn("only-app", buttons[0].classes)

        scripts = [s for s in self.page.find_all("script") if s.attrs.get("src") == "/app.js"]
        self.assertEqual(len(scripts), 1)
        self.assertIn("defer", scripts[0].attrs)

    def test_page_makes_no_remote_font_or_third_party_request(self):
        for source in (self.html, self.css):
            self.assertNotIn("fonts.googleapis", source)
            self.assertNotIn("fonts.gstatic", source)
            self.assertNotRegex(source, r"url\(\s*[\"']?https?:")
        for element in self.page.find_all():
            with self.subTest(tag=element.tag, src=element.attrs.get("src")):
                self.assertNotRegex(element.attrs.get("src") or "", r"^(https?:)?//")
        for link in self.page.find_all("link"):
            if link.attrs.get("rel") != "canonical":
                self.assertNotRegex(link.attrs.get("href", ""), r"^(https?:)?//")

        # Every local reference (stylesheet, script, image, font, icon) resolves to a published file.
        references = [m.strip("\"'") for m in re.findall(r"url\(([^)]+)\)", self.css)]
        for element in self.page.find_all():
            for attr in ("src", "href"):
                value = element.attrs.get(attr) or ""
                if value.startswith("/") and not value.startswith("//"):
                    references.append(value.split("#")[0].split("?")[0])
        self.assertIn("/app.js", references)
        for reference in references:
            with self.subTest(reference=reference):
                target = self.site / (reference.lstrip("/") or "index.html")
                self.assertTrue(target.is_file(), f"{reference} is not in site/")

        # Every icon points at a symbol defined in the local sprite file.
        symbols = set(re.findall(r'<symbol id="([^"]+)"', (self.site / "icons.svg").read_text()))
        icons = {u.attrs["href"] for u in self.page.find_all("use") if "href" in u.attrs}
        self.assertTrue(icons)
        for icon in icons:
            with self.subTest(icon=icon):
                file, _, name = icon.partition("#")
                self.assertEqual(file, "/icons.svg")
                self.assertIn(name, symbols, f"<use href=\"{icon}\"> has no <symbol>")

        for font in ("archivo.woff2", "jetbrains-mono.woff2"):
            self.assertTrue((self.site / "fonts" / font).read_bytes().startswith(b"wOF2"))
        self.assertIn("SIL OPEN FONT LICENSE", (self.site / "fonts/OFL.txt").read_text().upper())

    def test_contact_stays_reachable_on_every_width(self):
        footer = self.page.find_all("footer", cls="footer")
        self.assertEqual(len(footer), 1)
        contacts = footer[0].find_all("a", cls="footer-contact")
        self.assertEqual([a.attrs.get("href") for a in contacts], [INSTAGRAM_PROFILE])

        # No CSS rule may hide the contact links.
        self.assertIn("@media(max-width:350px)", self.css)
        for selectors, body in re.findall(r"([^{}]+)\{([^{}]*)\}", self.css):
            if not re.search(r"display:none|visibility:hidden", body):
                continue
            for selector in selectors.split(","):
                selector = re.sub(r":not\([^)]*\)", "", selector)
                with self.subTest(hidden=selector.strip()):
                    self.assertNotIn("footer-contact", selector)
                    self.assertNotIn("data-handoff", selector)

    def test_brand_tokens_equal_the_owner_canon(self):
        tokens = root_tokens(self.css)
        for name, value in CANON_TOKENS.items():
            with self.subTest(token=name):
                self.assertEqual(tokens.get(name), value)

    def test_brand_tokens_keep_wcag_aa_contrast(self):
        tokens = root_tokens(self.css)
        # Body text 4.5:1 on every ground the chat uses: page, sidebar/composer, question bubble.
        for foreground, background in (
            ("--paper", "--carbon"),
            ("--paper", "--panel"),
            ("--paper", "--raise"),
            ("--white", "--raise"),
            ("--ash", "--carbon"),
            ("--ash", "--panel"),
            ("--ash", "--raise"),
            ("--signal-bright", "--carbon"),
            ("--carbon", "--signal-bright"),  # send button icon
            ("--carbon", "--paper"),  # Paper buttons and the «Sì» badge
        ):
            with self.subTest(foreground=foreground, background=background):
                ratio = contrast_ratio(tokens[foreground], tokens[background])
                self.assertGreaterEqual(round(ratio, 2), 4.5)

        # The page ground must stay a real dark theme, with white text on it.
        self.assertLess(relative_luminance(tokens["--carbon"]), 0.02)
        self.assertGreater(relative_luminance(tokens["--white"]), 0.7)

    def test_public_routes_and_private_repository_paths(self):
        handler = functools.partial(QuietHandler, directory=str(self.site))
        with ThreadingHTTPServer(("127.0.0.1", 0), handler) as server:
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            try:
                base = f"http://127.0.0.1:{server.server_port}"
                for path in (
                    "/",
                    "/styles.css",
                    "/app.js",
                    "/icons.svg",
                    "/favicon.svg",
                    "/ritratto-instagram.jpg",
                    "/strumentini-mark.svg",
                    "/dichiarazioni-mark.svg",
                    "/share.png",
                    "/fonts/archivo.woff2",
                    "/fonts/jetbrains-mono.woff2",
                    "/robots.txt",
                    "/sitemap.xml",
                ):
                    with self.subTest(path=path), urlopen(base + path) as response:
                        self.assertEqual(response.status, 200)
                        self.assertTrue(response.read())
                for path in ("/board.js", "/README.md", "/docs/domain-cutover.md", "/scripts/domain-status.sh"):
                    with self.subTest(path=path), self.assertRaises(HTTPError) as error:
                        urlopen(base + path)
                    self.assertEqual(error.exception.code, 404)
                    error.exception.close()
            finally:
                server.shutdown()
                thread.join(timeout=5)


if __name__ == "__main__":
    unittest.main()
