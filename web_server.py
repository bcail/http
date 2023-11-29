'''
See https://github.com/python/cpython/blob/main/Lib/http/server.py
'''
from http.server import HTTPServer, HTTPStatus, BaseHTTPRequestHandler
import sys


class Handler(BaseHTTPRequestHandler):
    def version_string(self):
        return 'Apache'

    def log_request(self):
        self.log_message('"%s" path="%s"', self.requestline, self.path)

    def do_GET(self):
        self.log_request()
        self.send_response_only(HTTPStatus.OK)
        self.send_header('Server', self.version_string())
        self.send_header('Date', self.date_time_string())
        self.end_headers()
        self.wfile.write('response text'.encode('utf8'))

    def do_POST(self):
        self.log_request()
        self.send_response_only(HTTPStatus.OK)
        self.send_header('Server', self.version_string())
        self.send_header('Date', self.date_time_string())
        self.end_headers()


def main(port=8000):
    with HTTPServer(('', port), Handler) as httpd:
        print(f'Serving on port {port}...')
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nKeyboard interrupt received, exiting.")
            sys.exit(0)


if __name__ == '__main__':
    main()
