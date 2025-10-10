import json
import http.server
import socketserver
from urllib.parse import urlparse, parse_qs

try:
    from .app import greet
except ImportError:
    from app import greet


class HelloHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_url = urlparse(self.path)

        if parsed_url.path == "/hello":
            query_params = parse_qs(parsed_url.query)
            name = query_params.get("name", [""])[0]

            if not name:
                self._send_json_response(
                    400, {"ok": False, "error": "name parameter is required"}
                )
                return

            try:
                result = greet(name)
                self._send_json_response(200, result)
            except ValueError as e:
                self._send_json_response(400, {"ok": False, "error": str(e)})
        else:
            self._send_json_response(404, {"ok": False, "error": "Not Found"})

    def _send_json_response(self, status_code, data):
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

    def log_message(self, format, *args):
        pass


def create_server(port=8000):
    with socketserver.TCPServer(("", port), HelloHandler) as httpd:
        return httpd


if __name__ == "__main__":
    PORT = 8000
    with socketserver.TCPServer(("", PORT), HelloHandler) as httpd:
        print(f"Server running at http://localhost:{PORT}")
        print("Try: curl 'http://localhost:8000/hello?name=Alice'")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server...")
