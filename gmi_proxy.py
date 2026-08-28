"""
Minimal CORS proxy for GMI Cloud MiniMax Music 3.0.
Run: python3 gmi_proxy.py
Then open http://localhost:8765 in your browser.
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
import json
import os
import sys

GMI_BASE = "https://console.gmicloud.ai/api/v1/ie/requestqueue/apikey"
PORT = 8765
HERE = os.path.dirname(os.path.abspath(__file__))
INDEX_HTML = os.path.join(HERE, "index.html")

CORS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
    "Access-Control-Allow-Headers": "Authorization, Content-Type",
}


class ProxyHandler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        sys.stderr.write("[proxy] " + (fmt % args) + "\n")

    def _set_cors(self):
        for k, v in CORS.items():
            self.send_header(k, v)

    def do_OPTIONS(self):
        self.send_response(204)
        self._set_cors()
        self.end_headers()

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length) if length else b""
        auth = self.headers.get("Authorization", "")

        # Path: /requests -> POST {GMI_BASE}/requests
        target = GMI_BASE + self.path

        req = Request(target, data=body, method="POST")
        if auth:
            req.add_header("Authorization", auth)
        req.add_header("Content-Type", "application/json")

        try:
            with urlopen(req, timeout=180) as resp:
                resp_body = resp.read()
                self.send_response(resp.status)
                self._set_cors()
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(resp_body)))
                self.end_headers()
                self.wfile.write(resp_body)
        except HTTPError as e:
            err_body = e.read()
            self.send_response(e.code)
            self._set_cors()
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(err_body)))
            self.end_headers()
            self.wfile.write(err_body)
        except URLError as e:
            msg = json.dumps({"error": str(e.reason)}).encode()
            self.send_response(502)
            self._set_cors()
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(msg)))
            self.end_headers()
            self.wfile.write(msg)

    def do_GET(self):
        # Serve index.html at root
        if self.path in ("/", "/index.html"):
            try:
                with open(INDEX_HTML, "rb") as f:
                    body = f.read()
                self.send_response(200)
                self._set_cors()
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
                return
            except FileNotFoundError:
                msg = b"index.html not found next to gmi_proxy.py"
                self.send_response(500)
                self._set_cors()
                self.send_header("Content-Type", "text/plain")
                self.send_header("Content-Length", str(len(msg)))
                self.end_headers()
                self.wfile.write(msg)
                return

        # /requests/{id} -> GET {GMI_BASE}/requests/{id}
        target = GMI_BASE + self.path
        auth = self.headers.get("Authorization", "")
        req = Request(target, method="GET")
        if auth:
            req.add_header("Authorization", auth)
        try:
            with urlopen(req, timeout=60) as resp:
                resp_body = resp.read()
                self.send_response(resp.status)
                self._set_cors()
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(resp_body)))
                self.end_headers()
                self.wfile.write(resp_body)
        except HTTPError as e:
            err_body = e.read()
            self.send_response(e.code)
            self._set_cors()
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(err_body)))
            self.end_headers()
            self.wfile.write(err_body)
        except URLError as e:
            msg = json.dumps({"error": str(e.reason)}).encode()
            self.send_response(502)
            self._set_cors()
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(msg)))
            self.end_headers()
            self.wfile.write(msg)


if __name__ == "__main__":
    server = HTTPServer(("127.0.0.1", PORT), ProxyHandler)
    print(f"GMI Music proxy listening on http://localhost:{PORT}")
    print("Open: http://localhost:8765 in your browser (not file://)")
    print("Ctrl+C to stop")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
