import json
import unittest
import threading
import time
import http.client
from src.server import HelloHandler
import socketserver


class TestServer(unittest.TestCase):
    def setUp(self):
        self.httpd = socketserver.TCPServer(("", 0), HelloHandler)
        self.port = self.httpd.server_address[1]
        self.server_thread = threading.Thread(target=self.httpd.serve_forever)
        self.server_thread.daemon = True
        self.server_thread.start()
        time.sleep(0.1)  # Give server time to start
    
    def tearDown(self):
        self.httpd.shutdown()
        self.httpd.server_close()
        self.server_thread.join(timeout=1)
    
    def _make_request(self, path):
        conn = http.client.HTTPConnection(f"localhost:{self.port}")
        try:
            conn.request("GET", path)
            response = conn.getresponse()
            data = response.read().decode('utf-8')
            return response.status, response.getheader('Content-Type'), json.loads(data)
        finally:
            conn.close()
    
    def test_hello_endpoint_success(self):
        status, content_type, data = self._make_request("/hello?name=Alice")
        
        self.assertEqual(status, 200)
        self.assertEqual(content_type, "application/json")
        self.assertEqual(data["ok"], "True")
        self.assertEqual(data["message"], "Hello, Alice!")
    
    def test_hello_endpoint_with_whitespace(self):
        status, content_type, data = self._make_request("/hello?name=%20Bob%20")
        
        self.assertEqual(status, 200)
        self.assertEqual(content_type, "application/json")
        self.assertEqual(data["message"], "Hello, Bob!")
    
    def test_hello_endpoint_missing_name(self):
        status, content_type, data = self._make_request("/hello")
        
        self.assertEqual(status, 400)
        self.assertEqual(content_type, "application/json")
        self.assertIn("error", data)
        self.assertEqual(data["error"], "name parameter is required")
    
    def test_hello_endpoint_empty_name(self):
        status, content_type, data = self._make_request("/hello?name=")
        
        self.assertEqual(status, 400)
        self.assertEqual(content_type, "application/json")
        self.assertIn("error", data)
    
    def test_hello_endpoint_whitespace_only_name(self):
        status, content_type, data = self._make_request("/hello?name=%20%20")
        
        self.assertEqual(status, 400)
        self.assertEqual(content_type, "application/json")
        self.assertIn("error", data)
    
    def test_unknown_route_returns_404(self):
        status, content_type, data = self._make_request("/unknown")
        
        self.assertEqual(status, 404)
        self.assertEqual(content_type, "application/json")
        self.assertEqual(data["error"], "Not found")
    
    def test_server_starts_and_shuts_down_cleanly(self):
        # This test verifies the setUp and tearDown work correctly
        # Server should be running at this point
        status, _, _ = self._make_request("/hello?name=Test")
        self.assertEqual(status, 200)


if __name__ == "__main__":
    unittest.main()