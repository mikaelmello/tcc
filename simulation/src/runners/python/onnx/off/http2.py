from http.server import BaseHTTPRequestHandler, HTTPServer
from classifier import Classifier
import json
import os

classifier = Classifier(os.getenv("MODEL_PATH"))


class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length)

        inp = json.loads(post_data.decode("utf-8"))["input"]
        res = classifier.classify(inp)

        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"output": res}).encode("utf-8"))


def run(server_class=HTTPServer, port=8080):
    server_address = ("", port)
    httpd = server_class(server_address, Handler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()


if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()