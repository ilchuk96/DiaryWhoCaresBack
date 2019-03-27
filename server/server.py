import re
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from ms import make_suggestion


class Server(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_HEAD(self):
        self._set_headers()

    def do_GET(self):
        self._set_headers()
        self.wfile.write(json.dumps({'hello': 'world', 'received': 'ok'}).encode())

    def do_POST(self):
        content_len = int(self.headers['content-length'])
        post_body = self.rfile.read(content_len)
        data = json.loads(post_body)  # here is json with dairy text
        self._set_headers()
        film = make_suggestion(data)
        letter = film[0]
        if re.match('[0-9]|\?', letter):
            letter = '0-9'
        recommendation = {}
        with open('../html/' + letter + '/' + film + '/' + film + '.json') as film_json:
            map = json.load(film_json.read())
            recommendation['title'] = map['title']
            recommendation['description'] = map['description']

        self.wfile.write(json.dumps(recommendation).encode())


def run(server_class=HTTPServer, handler_class=Server, port=8081):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)

    print('Starting httpd on port %d...' % port)
    httpd.serve_forever()


if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()