"""Check the local script that turns the conversations into the chat interface."""

import json
import re
import shutil
import subprocess
import unittest

from test_pages_artifact import artifact_directory, parse


class AppScriptTest(unittest.TestCase):
    def setUp(self):
        self.site = artifact_directory()
        self.threads = parse((self.site / "index.html").read_text()).find_all("article", cls="thread")

    def test_app_script_is_local_and_private(self):
        script_path = self.site / "app.js"
        script = script_path.read_text()
        self.assertIn("prefers-reduced-motion", script)
        for forbidden in (
            "http://", "https://", "fetch(", "XMLHttpRequest", "localStorage", "sessionStorage",
            "document.cookie", "eval(", "innerHTML", "insertAdjacentHTML",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, script)

        # CI's runner may lack Node; the syntax check runs wherever it exists.
        if shutil.which("node"):
            result = subprocess.run(["node", "--check", str(script_path)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)

    def test_visitor_messages_reach_the_right_conversation(self):
        if not shutil.which("node"):
            return
        script = (self.site / "app.js").read_text()
        # Run the page's own code, not a copy: take from app.js the one-line arrow
        # `const plain = (text) => …;` and the body of `function match(text) { … }`
        # (closed by the first line holding only "  }"). If app.js is refactored and
        # these no longer match, update the extraction here: do not delete the test.
        plain = re.search(r"^\s*const plain = (\(text\) => .+);$", script, re.M)
        match = re.search(r"^  function match\(text\) \{\n(.*?)\n  \}$", script, re.M | re.S)
        self.assertIsNotNone(plain, "app.js: `const plain = (text) => …;` not found on one line; update this test")
        self.assertIsNotNone(match, "app.js: `function match(text) { … }` not found; update this test")

        threads = [[t.attrs["id"], t.attrs["data-keys"]] for t in self.threads]
        expected = {
            "quanto costa?": "gratis",
            "devo saper programmare?": "programmare",
            "chi sei": "chi-sono",
            "cosa hai costruito": "costruito",
            "privacy dei clienti": "dati",
            "come ti contatto": "contatto",
            "zzz qwerty": None,
        }
        program = (
            "const input = JSON.parse(require('fs').readFileSync(0, 'utf8'));\n"
            f"const plain = {plain.group(1)};\n"
            "const threads = input.threads.map(([id, keys]) => ({ id, dataset: { keys } }));\n"
            f"function match(text) {{\n{match.group(1)}\n}}\n"
            "console.log(JSON.stringify(input.phrases.map((p) => (match(p) || {}).id || null)));\n"
        )
        result = subprocess.run(
            ["node", "-e", program],
            input=json.dumps({"threads": threads, "phrases": list(expected)}),
            capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(dict(zip(expected, json.loads(result.stdout))), expected)


if __name__ == "__main__":
    unittest.main()
