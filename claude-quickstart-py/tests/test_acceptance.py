# tests/test_acceptance.py
# Acceptance tests for success criteria:
#  - /hello?name=Alice -> 200 JSON greeting
#  - /hello           -> 200 JSON default "Developer"
#  - /hello?name=%20  -> 400 JSON error
#  - /nope            -> 404 JSON error
# Ensures Content-Type is application/json and server shuts down cleanly.

import threading
import time
import json
import socket
import unittest
from http.server import HTTPServer
from urllib.request import urlopen
from urllib.error import HTTPError
from src.server import HelloHandler


def _free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


class AcceptanceHTTPServerTest(unittest.TestCase):
    def setUp(self):
        self.host = "127.0.0.1"
        self.port = _free_port()
        self.httpd = HTTPServer((self.host, self.port), HelloHandler)
        self.thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)
        self.thread.start()
        time.sleep(0.05)

    def tearDown(self):
        self.httpd.shutdown()
        self.thread.join(timeout=2)

    def _get(self, path: str):
        return urlopen(f"http://{self.host}:{self.port}{path}")

    def test_hello_with_name_200(self):
        with self._get("/hello?name=Alice") as resp:
            self.assertEqual(resp.status, 200)
            self.assertTrue(
                resp.getheader("Content-Type").startswith("application/json")
            )
            data = json.loads(resp.read().decode("utf-8"))
            self.assertEqual(data, {"ok": "True", "message": "Hello, Alice!"})

    def test_hello_default_name_200(self):
        with self._get("/hello") as resp:
            self.assertEqual(resp.status, 200)
            data = json.loads(resp.read().decode("utf-8"))
            self.assertEqual(data, {"ok": "True", "message": "Hello, Developer!"})

    def test_hello_invalid_name_400(self):
        try:
            self._get("/hello?name=%20")
            self.fail("Expected 400 HTTPError")
        except HTTPError as e:
            self.assertEqual(e.code, 400)
            self.assertTrue(
                e.headers.get("Content-Type", "").startswith("application/json")
            )
            body = json.loads(e.read().decode("utf-8"))
            self.assertEqual(body["ok"], False)
            self.assertIn("non-empty string", body["error"])

    def test_not_found_404(self):
        try:
            self._get("/nope")
            self.fail("Expected 404 HTTPError")
        except HTTPError as e:
            self.assertEqual(e.code, 404)
            self.assertTrue(
                e.headers.get("Content-Type", "").startswith("application/json")
            )
            body = json.loads(e.read().decode("utf-8"))
            self.assertEqual(body, {"ok": False, "error": "Not Found"})


if __name__ == "__main__":
    unittest.main()
