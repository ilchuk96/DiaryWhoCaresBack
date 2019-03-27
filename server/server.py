import re
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from PIL import Image
import os
import base64
from io import BytesIO
from dwc_adviser.dwc_adviser import MainAdviser


class Server(BaseHTTPRequestHandler):
    adviser = MainAdviser()

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
        print(os.path.curdir)
        content_len = int(self.headers['content-length'])
        post_body = self.rfile.read(content_len)
        data = json.loads(post_body)  # here is json with dairy text
        self._set_headers()
        film = self.adviser.make_suggestion(data['text'])[0]
        letter = film[0]
        if re.match('[0-9]|\?', letter):
            letter = '0-9'
        recommendation = {}
        with open('html/' + letter + '/' + film + '/' + film + '.json') as film_json:
            map = json.load(film_json)
            recommendation['title'] = map['title']
            recommendation['description'] = map['description']

        if os.path.isfile('html/' + letter + '/' + film + '/' + film + '.jpg'):
            basehight = 300
            with Image.open('html/' + letter + '/' + film + '/' + film + '.jpg') as img:
                hpercent = (basehight / float(img.size[1]))
                wsize = int((float(img.size[0]) * float(hpercent)))
                img = img.resize((wsize, basehight), Image.ANTIALIAS)
                buffered = BytesIO()
                img.save(buffered, format="JPEG")
                img_str = base64.b64encode(buffered.getvalue())
                recommendation['img'] = img_str.decode("utf-8")

        self.wfile.write(json.dumps(recommendation).encode())


def run(server_class=HTTPServer, handler_class=Server, port=8090):
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
