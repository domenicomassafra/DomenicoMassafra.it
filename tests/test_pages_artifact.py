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
    "favicon.svg",
    "robots.txt",
    "sitemap.xml",
}


def artifact_directory():
    workflow = (ROOT / ".github/workflows/pages.yml").read_text()
    match = re.search(
        r"uses:\s*actions/upload-pages-artifact@v3\s*\n\s*with:\s*\n\s*path:\s*([^\s#]+)",
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
        self.assertEqual(
            {p.relative_to(site).as_posix() for p in site.rglob("*") if p.is_file()},
            PUBLIC_FILES,
        )

    def test_public_homepage_uses_approved_officina_direction(self):
        site = artifact_directory()
        html = (site / "index.html").read_text()
        css = (site / "styles.css").read_text()
        self.assertIn("Hai un problema?", html)
        self.assertIn("Proviamo con l'AI.", html)
        self.assertIn("L'officina di Domenico", html)
        self.assertIn('id="laboratorio"', html)
        self.assertIn('id="contatti"', html)
        self.assertIn('class="verdict"', html)
        self.assertIn("https://www.instagram.com/domenico.massafraa/", html)
        self.assertIn("https://strumentini.it/", html)
        self.assertIn("https://dichiarazionipubbliche.it/", html)
        self.assertIn("prefers-reduced-motion", css)
        self.assertIn("--red:#ff725f", css)
        self.assertNotIn("Capire abbastanza.", html)
        self.assertNotIn("PROTOTIPO NON PUBBLICO", html)
        self.assertNotIn("mailto:", html)

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
        self.assertIn('href="#laboratorio"', action_links[1])
        self.assertIn("Apri Instagram per contattarmi", actions)
        self.assertIn("se disponibile", html.lower())

        footer = html.split('<footer class="footer">', 1)[1].split("</footer>", 1)[0]
        self.assertIn(f'href="{INSTAGRAM_PROFILE}"', footer)
        self.assertIn('class="footer-contact"', footer)

        # Narrow layouts must keep the first (contact) nav item visible.
        self.assertNotIn(".main-nav a:first-child{display:none}", css)
        self.assertNotIn("mailto:", html)
        self.assertNotIn("instagram.com/direct/", html)
        self.assertNotIn("ig.me/", html)
        self.assertNotRegex(html, r"<form\b")

    def test_public_routes_and_private_repository_paths(self):
        site = artifact_directory()
        handler = functools.partial(QuietHandler, directory=str(site))
        with ThreadingHTTPServer(("127.0.0.1", 0), handler) as server:
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            try:
                base = f"http://127.0.0.1:{server.server_port}"
                for path in ("/", "/styles.css", "/favicon.svg", "/robots.txt", "/sitemap.xml"):
                    with self.subTest(path=path), urlopen(base + path) as response:
                        self.assertEqual(response.status, 200)
                        self.assertTrue(response.read())
                for path in ("/README.md", "/docs/domain-cutover.md", "/scripts/domain-status.sh"):
                    with self.subTest(path=path), self.assertRaises(HTTPError) as error:
                        urlopen(base + path)
                    self.assertEqual(error.exception.code, 404)
            finally:
                server.shutdown()
                thread.join(timeout=5)


if __name__ == "__main__":
    unittest.main()
