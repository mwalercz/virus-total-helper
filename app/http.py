import json
import re


class MethodNotSupported(Exception):
    pass


class HTTPRequest:
    def __init__(self, raw_data):
        self.raw_data = raw_data
        self.path = None
        self.command = None
        self.body = None
        self.headers = {}
        self._parse_request()

    def _parse_request(self):
        first_line, host, rest = self.raw_data.split(sep='\r\n', maxsplit=2)
        self.command, self.path, protocol = first_line.split(maxsplit=2)
        line_end = re.compile(r'\r\n\r\n')
        raw_headers, self.body = line_end.split(rest, maxsplit=1)
        self._parse_headers(raw_headers)

    def _parse_headers(self, raw_headers):
        head, sep, rest = raw_headers.partition('\r\n')
        if rest == "":
            if head:
                key, sep, value = head.partition(':')
                self.headers.update({key: value})
            else:
                return
        else:
            key, sep, value = head.partition(':')
            self.headers.update({key: value})
            self._parse_headers(rest)

    def is_finished(self):
        if self.command == "GET":
            return self._is_get_finished()
        elif self.command == "POST":
            return self._is_post_finished()
        else:
            raise MethodNotSupported

    def _is_post_finished(self):
        content_length = int(self.headers['Content-Length'])
        body_length = len(self.body)
        return content_length == len(self.body)

    def _is_get_finished(self):
        if self.raw_data:
            length = len(self.raw_data)
            last_chars = self.raw_data[length - 4:length]
            return last_chars == '\r\n\r\n'
        else:
            return False

    def json(self):
        content_type = "Content-Type"
        if content_type in self.headers:
            if "application/json" in self.headers[content_type]:
                return json.loads(self.body)
            else:
                return None
        else:
            return None

    def binary(self):
        content_type = "Content-Type"
        if content_type in self.headers:
            if "application/octet-stream" in self.headers[content_type]:
                return self.body.encode("utf-8")
            else:
                return None
        else:
            return None


# zwracamy tylko JSONY więc content-type jest już zdefiniowany
class HTTPResponse:
    def __init__(self):
        self.protocol = "HTTP/1.1"
        self.status = "200 OK"
        self.headers = {"Content-Type": "application/json"}
        self.body = {}

    def __str__(self):
        string = self.protocol + " " + self.status + '\r\n'
        for key, value in self.headers.items():
            string += key + ': ' + value + '\r\n'
        string += '\r\n'
        json_body = json.dumps(self.body)
        string += json_body
        return string
