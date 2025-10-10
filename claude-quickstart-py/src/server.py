import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from src.app import greet


class Handler(BaseHTTPRequestHandler):
    server_version = "ClaudeQuickstartHTTP/1.0"

    def _send_json(self, status_code: int, payload: dict) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json;charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802 (stdlb method name)
        parsed_url = urlparse(self.path)

        if parsed_url.path != "/hello":
            self._send_json(404, {"ok": False, "error": "Not Found"})
            return

        params = parse_qs(parsed_url.query)
        name = (params.get("name", ["Developer"])[0]).strip()

        try:
            result = greet(name)
            self._send_json(200, result)
        except ValueError as e:
            self._send_json(400, {"ok": False, "error": str(e)})


def run(host: str = "127.0.0.1", port: int = 3000) -> None:
    with HTTPServer((host, port), Handler) as httpd:
        print(f"Serving on http://{host}:{port}")
        httpd.serve_forever()


if __name__ == "__main__":
    run()
