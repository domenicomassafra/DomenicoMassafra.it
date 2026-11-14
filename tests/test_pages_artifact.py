"""Exercise the exact directory configured for the Pages artifact over HTTP."""

import functools
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import re
import threading
from urllib.error import HTTPError
from urllib.request import urlopen
import unittest


ROOT = Path(__file__).resolve().parents[1]
INSTAGRAM_PROFILE = "https://www.instagram.com/domenico.massafraa/"
PUBLIC_FILES = {
    ".nojekyll",
    "index.html",
    "styles.css",
    "ritratto-instagram.jpg",
    "strumentini-mark.svg",
    "dichiarazioni-mark.svg",
    "favicon.svg",
    "robots.txt",
    "sitemap.xml",
}


def root_tokens(css):
    match = re.search(r":root\{([^}]*)\}", css)
    if match is None:
        raise AssertionError("styles.css must declare its tokens in :root")
    return dict(re.findall(r"(--[a-z-]+):(#[0-9a-f]{6})", match.group(1)))


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
        self.assertIn("Domenico Massafra", html)
        # Approved promise (owner 28/10/2026) and payoff, Area Divulgazione positioning-v2.
        text = re.sub(r"<[^>]+>", "", html)
        self.assertIn("Faccio lavorare gli agenti AI su problemi veri.", text)
        self.assertIn("Ti mostro cosa funziona, anche se non programmi.", html)
        self.assertIn("Non devi saper programmare.", html)
        self.assertIn("Vale il tuo tempo?", html)
        # Editorial verdicts must say they are not measured tests.
        self.assertIn("non il risultato di un test", html)
        self.assertIn('id="esperimenti"', html)
        self.assertIn('id="contatti"', html)
        self.assertIn('class="method-example"', html)
        self.assertGreaterEqual(html.count("<details"), 3)
        self.assertIn("https://www.instagram.com/domenico.massafraa/", html)
        self.assertIn("https://strumentini.it/", html)
        self.assertIn("https://dichiarazionipubbliche.it/", html)
        self.assertIn("prefers-reduced-motion", css)
        self.assertIn("color-scheme:dark", css)
        self.assertIn('name="theme-color" content="#0d1114"', html)
        self.assertNotIn("L'officina di Domenico", html)
        self.assertNotIn("PROTOTIPO NON PUBBLICO", html)
        self.assertNotIn("mailto:", html)
        self.assertIn('src="/ritratto-instagram.jpg"', html)
        self.assertIn('alt="Ritratto pubblicato sul profilo Instagram di Domenico Massafra"', html)
        photo = (site / "ritratto-instagram.jpg").read_bytes()
        self.assertGreater(len(photo), 1000)
        self.assertTrue(photo.startswith(b"\xff\xd8"))
        for mark in ("strumentini-mark.svg", "dichiarazioni-mark.svg"):
            self.assertIn(f'src="/{mark}"', html)
            self.assertIn("<svg", (site / mark).read_text())

    def test_contact_is_the_first_action_without_unverified_routes(self):
        html = (artifact_directory() / "index.html").read_text()
        css = (artifact_directory() / "styles.css").read_text()

        nav = html.split('<nav class="main-nav"', 1)[1].split("</nav>", 1)[0]
        nav_links = re.findall(r"<a\b[^>]*>", nav)
        self.assertGreaterEqual(len(nav_links), 2)
        self.assertIn('href="#contatti"', nav_links[0])

        actions = html.split('<div class="hero-actions">', 1)[1].split("</div>", 1)[0]
        action_links = re.findall(r"<a\b[^>]*>", actions)
        self.assertEqual(len(action_links), 2)
        self.assertIn('class="button button-primary"', action_links[0])
        self.assertIn(f'href="{INSTAGRAM_PROFILE}"', action_links[0])
        self.assertIn('href="#esperimenti"', action_links[1])
        self.assertIn("Raccontami il tuo problema", actions)
        self.assertIn("se disponibile", html.lower())

        footer = html.split('<footer class="footer">', 1)[1].split("</footer>", 1)[0]
        self.assertIn(f'href="{INSTAGRAM_PROFILE}"', footer)
        self.assertIn('class="footer-contact"', footer)

        # Narrow layouts must keep the contact action visible and usable.
        self.assertNotIn(".main-nav a:first-child{display:none}", css)
        self.assertIn("@media(max-width:350px)", css)
        self.assertNotIn("mailto:", html)
        self.assertNotIn("instagram.com/direct/", html)
        self.assertNotIn("ig.me/", html)
        self.assertNotRegex(html, r"<form\b")

    def test_dark_theme_keeps_wcag_aa_contrast(self):
        site = artifact_directory()
        tokens = root_tokens((site / "styles.css").read_text())
        # Body text 4.5:1, large text 3:1; borders are decoration and are not asserted.
        for foreground, background, minimum in (
            ("--ink", "--paper", 4.5),
            ("--ink-soft", "--paper", 4.5),
            ("--ink-soft", "--sheet", 4.5),
            ("--ink-soft", "--surface", 4.5),
            ("--signal", "--paper", 4.5),
            ("--signal", "--sheet", 4.5),
            ("--signal", "--surface", 4.5),
            ("--ink", "--footer", 4.5),
            ("--ink-on-light", "--cream", 4.5),
            ("--signal-on-light", "--cream", 4.5),
            ("--cream", "--ember", 4.5),
            ("--ink-on-light", "--ink", 4.5),
        ):
            with self.subTest(foreground=foreground, background=background):
                ratio = contrast_ratio(tokens[foreground], tokens[background])
                self.assertGreaterEqual(round(ratio, 2), minimum)

        # The page ground must stay a real dark theme, not a light one.
        self.assertLess(relative_luminance(tokens["--paper"]), 0.02)
        self.assertGreater(relative_luminance(tokens["--ink"]), 0.7)

    def test_public_routes_and_private_repository_paths(self):
        site = artifact_directory()
        handler = functools.partial(QuietHandler, directory=str(site))
        with ThreadingHTTPServer(("127.0.0.1", 0), handler) as server:
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            try:
                base = f"http://127.0.0.1:{server.server_port}"
                for path in ("/", "/styles.css", "/favicon.svg", "/ritratto-instagram.jpg", "/strumentini-mark.svg", "/dichiarazioni-mark.svg", "/robots.txt", "/sitemap.xml"):
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
