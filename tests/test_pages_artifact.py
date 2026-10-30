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
        self.assertIn("Prima lo", html)
        self.assertIn("Poi te lo racconto", html)
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
