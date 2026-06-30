from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

class httphandler(BaseHTTPRequestHandler):
    def send_json(self, code, data):
        self.send_response(code)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def do_GET(self):
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        parsed = parse_qs(parsed_url.query)

        if path not in {"/add", "/subtract", "/multiply"}:
            self.send_json(404, {"error": "Endpoint not found"})
            return

        if "a" not in parsed or "b" not in parsed:
            self.send_json(400, {"error": "Missing a or b query parameter"})
            return

        try:
            a = float(parsed["a"][0])
            b = float(parsed["b"][0])
        except ValueError:
            self.send_json(400, {"error": "a and b must be numbers"})
            return

        if path == "/add":
            result = add(a, b)
            operation = "addition"
        elif path == "/subtract":
            result = subtract(a, b)
            operation = "subtraction"
        else:
            result = multiply(a, b)
            operation = "multiplication"

        response = {
            "a": a,
            "b": b,
            "operation": operation,
            "result": result,
        }
        self.send_json(200, response)

def run(server_class=HTTPServer, handler_class=httphandler):
    server_address = ("", 5001)
    httpd = server_class(server_address, handler_class)
    print("Starting calculator server on port 5001...")
    httpd.serve_forever()

if __name__ == "__main__":
    run()