from http.server import BaseHTTPRequestHandler
import io

class HTTPRequest(BaseHTTPRequestHandler):
    def __init__(self, request_text):
        request_text = request_text.encode('utf-8')
        self.rfile = io.StringIO(request_text)
        self.raw_requestline = self.rfile.readline()
        self.error_code = self.error_message = None
        self.parse_request()

    def send_error(self, code, message):
        self.error_code = code
        self.error_message = message