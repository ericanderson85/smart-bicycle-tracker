from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json


class APIHandler(BaseHTTPRequestHandler):
    routes = {"GET": {}}

    def _set_cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")

    def _send_json(self, code: int, data: dict):
        self.send_response(code)
        self._set_cors()
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def do_OPTIONS(self):
        self.send_response(200)
        self._set_cors()
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        args = {
            k: v[0] if len(v) == 1 else v for k, v in parse_qs(parsed.query).items()
        }
        handler = self.routes["GET"].get(path)

        if not handler:
            self._send_json(404, {"error": "not found"})
            return

        try:
            result = handler(args)
            self._send_json(200, result)
        except Exception as e:
            self._send_json(500, {"error": str(e)})

    @classmethod
    def get(cls, path):
        def decorator(fn):
            cls.routes["GET"][path] = fn
            return fn

        return decorator
