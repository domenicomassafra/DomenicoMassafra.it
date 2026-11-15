"""Exercise the exact directory configured for the Pages artifact over HTTP."""

import functools
from html.parser import HTMLParser
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import re
import shutil
import subprocess
import threading
from urllib.error import HTTPError
from urllib.request import urlopen
import unittest


ROOT = Path(__file__).resolve().parents[1]
INSTAGRAM_PROFILE = "https://www.instagram.com/domenico.massafraa/"
PROMISE = "Faccio lavorare gli agenti AI su problemi veri. Ti mostro cosa funziona, anche se non programmi."
PAYOFF = "Non devi saper programmare. Devi capirne abbastanza."
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
    "board.js",
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


def visible_text(html):
    html = re.sub(r"(?s)<(script|style)\b.*?</\1>", " ", html)
    return " ".join(re.sub(r"<[^>]+>", " ", html).split())


class FlapText(HTMLParser):
    """Collect the source text inside every element marked data-flap."""

    VOID = {"area", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}

    def __init__(self):
        super().__init__()
        self.stack = []  # one entry per open element: index into self.texts, or None
        self.texts = []

    def handle_starttag(self, tag, attrs):
        if tag in self.VOID:
            return
        if "data-flap" in dict(attrs):
            self.texts.append("")
            self.stack.append(len(self.texts) - 1)
        else:
            self.stack.append(None)

    def handle_endtag(self, tag):
        if tag not in self.VOID and self.stack:
            self.stack.pop()

    def handle_data(self, data):
        for index in self.stack:
            if index is not None:
                self.texts[index] += data


def flap_texts(html):
    parser = FlapText()
    parser.feed(html)
    parser.close()
    return [" ".join(text.split()) for text in parser.texts]


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
    def test_only_the_public_files_are_uploaded(self):
        site = artifact_directory()
        workflow = (ROOT / ".github/workflows/pages.yml").read_text()
        self.assertRegex(workflow, r"(?m)^\s*include-hidden-files:\s*true\s*$")
        self.assertEqual(
            {p.relative_to(site).as_posix() for p in site.rglob("*") if p.is_file()},
            PUBLIC_FILES,
        )

    def test_public_homepage_matches_owner_brand_and_uses_real_portrait(self):
        site = artifact_directory()
        html = (site / "index.html").read_text()
        css = (site / "styles.css").read_text()
        text = visible_text(html)
        self.assertIn("Domenico Massafra", text)
        self.assertIn(PROMISE, text)
        self.assertIn(PAYOFF, text)
        for section in ("verdetti", "esperimenti", "chi-sono", "contatti"):
            self.assertIn(f'id="{section}"', html)

        # «Vale il tuo tempo?»: four native exclusive verdicts, one open at load.
        verdicts = re.findall(r'<details\b[^>]*\bname="verdetto"[^>]*>', html)
        self.assertEqual(len(verdicts), 4)
        self.assertEqual(sum(bool(re.search(r"\sopen\b", tag)) for tag in verdicts), 1)

        self.assertIn(INSTAGRAM_PROFILE, html)
        self.assertIn("https://strumentini.it/", html)
        self.assertIn("https://dichiarazionipubbliche.it/", html)
        self.assertIn('src="/ritratto-instagram.jpg"', html)
        self.assertIn('alt="Ritratto pubblicato sul profilo Instagram di Domenico Massafra"', html)
        self.assertIn('name="theme-color" content="#0b0b0d"', html)
        self.assertIn("prefers-reduced-motion", css)
        self.assertIn("color-scheme:dark", css)
        self.assertNotIn("PROTOTIPO NON PUBBLICO", html)
        self.assertNotIn("mailto:", html)

        photo = (site / "ritratto-instagram.jpg").read_bytes()
        self.assertGreater(len(photo), 1000)
        self.assertTrue(photo.startswith(b"\xff\xd8"))
        for mark in ("strumentini-mark.svg", "dichiarazioni-mark.svg"):
            self.assertIn(f'src="/{mark}"', html)
            self.assertIn("<svg", (site / mark).read_text())

        # Social previews use the local share image.
        self.assertRegex(html, r'<meta property="og:image" content="https://domenicomassafra\.it/share\.png">')
        self.assertTrue((site / "share.png").read_bytes().startswith(b"\x89PNG\r\n\x1a\n"))

        # «Tabellone»: the departure board is the real site navigation.
        scripts = re.findall(r"<script\b[^>]*\bsrc=\"/board\.js\"[^>]*>", html)
        self.assertEqual(len(scripts), 1)
        self.assertRegex(scripts[0], r"\sdefer\b")
        self.assertIn('<nav class="board"', html)
        board = html.split('<nav class="board"', 1)[1].split("</nav>", 1)[0]
        rows = re.findall(r'<a\b[^>]*\bclass="row\b[^>]*>', board)
        self.assertEqual(
            [re.search(r'href="([^"]*)"', row).group(1) for row in rows],
            ["#contatti", "#verdetti", "https://strumentini.it/", "https://dichiarazionipubbliche.it/", "#chi-sono"],
        )
        self.assertEqual(sum("row-live" in row for row in rows), 1)

        # Without the script every split-flap element still shows its words.
        flaps = flap_texts(html)
        self.assertGreaterEqual(len(flaps), len(rows) * 2)
        for index, flap in enumerate(flaps):
            with self.subTest(flap=index):
                self.assertTrue(flap, "a data-flap element is empty in the source")

        # Sound stays hidden and off until the script and the visitor turn it on.
        sound = re.findall(r"<button\b[^>]*\bdata-sound\b[^>]*>", html)
        self.assertEqual(len(sound), 1)
        self.assertRegex(sound[0], r"\shidden\b")
        self.assertIn('aria-pressed="false"', sound[0])

    def test_board_script_is_local_optional_and_silent_until_asked(self):
        script_path = artifact_directory() / "board.js"
        script = script_path.read_text()
        self.assertIn("prefers-reduced-motion", script)
        for forbidden in ("http://", "https://", "fetch(", "XMLHttpRequest", "localStorage", "document.cookie", "eval(", "innerHTML"):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, script)

        # Audio is created only by the visitor's click on the sound button.
        self.assertEqual(script.count("new AudioContextClass()"), 1)
        self.assertNotRegex(script, r"new\s+(window\.)?(webkit)?AudioContext\b")
        self.assertIn("addEventListener('click'", script)
        self.assertGreater(script.index("new AudioContextClass()"), script.index("addEventListener('click'"))

        # CI's runner may lack Node; the syntax check runs wherever it exists.
        if shutil.which("node"):
            result = subprocess.run(["node", "--check", str(script_path)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)

    def test_page_makes_no_remote_font_or_third_party_request(self):
        site = artifact_directory()
        html = (site / "index.html").read_text()
        css = (site / "styles.css").read_text()
        for source in (html, css):
            self.assertNotIn("fonts.googleapis", source)
            self.assertNotIn("fonts.gstatic", source)
            self.assertNotRegex(source, r"url\(\s*[\"']?https?:")
        self.assertNotRegex(html, r'\bsrc="(https?:)?//')
        for tag in re.findall(r"<link\b[^>]*>", html):
            if 'rel="canonical"' not in tag:
                self.assertNotRegex(tag, r'href="(https?:)?//')

        # Every local reference resolves to a published file.
        references = [m.strip("\"'") for m in re.findall(r"url\(([^)]+)\)", css)]
        references += re.findall(r'(?:src|href)="(/[^"#?]*)"', html)
        self.assertIn("/board.js", references)
        for reference in references:
            with self.subTest(reference=reference):
                target = site / (reference.lstrip("/") or "index.html")
                self.assertTrue(target.is_file(), f"{reference} is not in site/")

        # Every inline SVG icon points at a symbol defined in the page.
        icons = re.findall(r'<use\b[^>]*\bhref="#([^"]+)"', html)
        self.assertIn("freccia", icons)
        for icon in set(icons):
            with self.subTest(icon=icon):
                self.assertIn(f'id="{icon}"', html)

        for font in ("archivo.woff2", "jetbrains-mono.woff2"):
            self.assertTrue((site / "fonts" / font).read_bytes().startswith(b"wOF2"))
        self.assertIn("SIL OPEN FONT LICENSE", (site / "fonts/OFL.txt").read_text().upper())

    def test_contact_is_the_first_action_without_unverified_routes(self):
        html = (artifact_directory() / "index.html").read_text()
        css = (artifact_directory() / "styles.css").read_text()

        nav = html.split('<nav class="main-nav"', 1)[1].split("</nav>", 1)[0]
        nav_links = re.findall(r"<a\b[^>]*>", nav)
        self.assertGreaterEqual(len(nav_links), 2)
        self.assertIn('href="#contatti"', nav_links[-1])

        actions = html.split('<div class="hero-actions">', 1)[1].split("</div>", 1)[0]
        action_links = re.findall(r"<a\b[^>]*>", actions)
        self.assertEqual(len(action_links), 2)
        self.assertIn("button-primary", action_links[0])
        self.assertIn(f'href="{INSTAGRAM_PROFILE}"', action_links[0])
        self.assertIn('href="#esperimenti"', action_links[1])
        self.assertIn("se disponibile", html.lower())

        footer = html.split('<footer class="footer">', 1)[1].split("</footer>", 1)[0]
        self.assertIn(f'href="{INSTAGRAM_PROFILE}"', footer)
        self.assertIn('class="footer-contact"', footer)

        self.assertNotIn("mailto:", html)
        self.assertNotIn("instagram.com/direct/", html)
        self.assertNotIn("ig.me/", html)
        self.assertNotRegex(html, r"<form\b")

        # Narrow layouts must keep the contact action visible and usable.
        self.assertIn("@media(max-width:350px)", css)
        for selectors, body in re.findall(r"([^{}]+)\{([^{}]*)\}", css):
            if not re.search(r"display:none|visibility:hidden", body):
                continue
            for selector in selectors.split(","):
                selector = re.sub(r":not\([^)]*\)", "", selector)
                with self.subTest(hidden=selector.strip()):
                    self.assertNotIn("nav-contact", selector)
                    self.assertNotIn("footer-contact", selector)
                    self.assertNotIn(":first-child", selector.replace("::", ""))

    def test_brand_tokens_equal_the_owner_canon(self):
        tokens = root_tokens((artifact_directory() / "styles.css").read_text())
        for name, value in CANON_TOKENS.items():
            with self.subTest(token=name):
                self.assertEqual(tokens.get(name), value)

    def test_brand_tokens_keep_wcag_aa_contrast(self):
        tokens = root_tokens((artifact_directory() / "styles.css").read_text())
        # Body text 4.5:1, large text 3:1; borders are decoration and are not asserted.
        for foreground, background, minimum in (
            ("--white", "--carbon", 4.5),
            ("--ash", "--carbon", 4.5),
            ("--ash", "--panel", 4.5),
            ("--signal-bright", "--carbon", 4.5),
            ("--signal-bright", "--panel", 4.5),
            ("--carbon", "--paper", 4.5),
            ("--graphite", "--paper", 4.5),
            ("--graphite", "--white", 4.5),
            ("--carbon", "--signal-bright", 4.5),
            ("--white", "--signal", 4.5),
            ("--signal", "--paper", 3.0),  # large text only
            # Split-flap cells, and the board row hover background.
            ("--white", "--flap", 4.5),
            ("--signal-bright", "--flap", 4.5),
            ("--ash", "--flap", 4.5),
        ):
            with self.subTest(foreground=foreground, background=background):
                ratio = contrast_ratio(tokens[foreground], tokens[background])
                self.assertGreaterEqual(round(ratio, 2), minimum)

        # The page ground must stay a real dark theme, with white text on it.
        self.assertLess(relative_luminance(tokens["--carbon"]), 0.02)
        self.assertGreater(relative_luminance(tokens["--white"]), 0.7)

    def test_public_routes_and_private_repository_paths(self):
        site = artifact_directory()
        handler = functools.partial(QuietHandler, directory=str(site))
        with ThreadingHTTPServer(("127.0.0.1", 0), handler) as server:
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            try:
                base = f"http://127.0.0.1:{server.server_port}"
                for path in (
                    "/",
                    "/styles.css",
                    "/board.js",
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
                for path in ("/README.md", "/docs/domain-cutover.md", "/scripts/domain-status.sh"):
                    with self.subTest(path=path), self.assertRaises(HTTPError) as error:
                        urlopen(base + path)
                    self.assertEqual(error.exception.code, 404)
                    error.exception.close()
            finally:
                server.shutdown()
                thread.join(timeout=5)


if __name__ == "__main__":
    unittest.main()
