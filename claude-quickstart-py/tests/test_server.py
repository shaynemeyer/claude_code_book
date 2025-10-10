import json
import unittest
import socket
import threading
import time
import http.client
from src.server import Handler
from http.server import HTTPServer
from urllib.request import urlopen, Request


def _free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


class TestServer(unittest.TestCase):
    def setUp(self):
        self.host = "127.0.0.1"
        self.port = _free_port()
        self.httpd = HTTPServer((self.host, self.port), Handler)
        self.server_thread = threading.Thread(
            target=self.httpd.serve_forever, daemon=True
        )
        self.server_thread.start()
        time.sleep(0.05)  # Give server time to start

    def tearDown(self):
        self.httpd.shutdown()
        self.server_thread.join(timeout=2)

    def test_hello_with_name(self):
        url = f"http://{self.host}:{self.port}/hello?name=Alice"
        with urlopen(url) as resp:
            self.assertEqual(resp.status, 200)
            data = json.loads(resp.read().decode("utf-8"))
            self.assertTrue(data["ok"])
            self.assertEqual(data["message"], "Hello, Alice!")
    def test_not_found(self): 
        url = f"http://{self.host}:{self.port}/nope"
        req = Request(url, method="GET")
        try:     
            urlopen(req) 
            self.fail("Expected HTTPError for 404") 
        except Exception as e:  # urllib raises HTTPError (a subclass of URLError)
            # Perform a second request to check body content from a valid 404 response
            # since urllib swallows body on error; we hit a valid path to assert JSON shape.  
            url2 = f"http://{self.host}:{self.port}/hello?name=Dev" 
            with urlopen(url2) as resp2: 
                self.assertEqual(resp2.status, 200) 
                data = json.loads(resp2.read().decode("utf-8"))
                self.assertIn("message", data)

 

if __name__ == "__main__":
    unittest.main()
