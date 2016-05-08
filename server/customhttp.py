import json
import re


class MethodNotSupported(Exception):
    pass


class WrongHeader(Exception):
    pass


class HTTPRequest:
    def __init__(self, raw_data):
        self.raw_data = raw_data
        self.path = None
        self.command = None
        self.body = None
        self.protocol = None
        self.headers = {}
        self._parse_request(raw_data)

    def json(self):
        content_type = "Content-Type"
        if content_type in self.headers:
            if "application/json" in self.headers[content_type]:
                return json.loads(self.body)
            else:
                raise WrongHeader("Content-Type doesn't include application/json")
        else:
            raise WrongHeader("No Content-Type in headers")

    def binary(self):
        content_type = "Content-Type"
        if content_type in self.headers:
            if "application/octet-stream" in self.headers[content_type]:
                return self.body.encode("utf-8")
            else:
                raise WrongHeader("Content-Type doesn't include application/octet-stream")
        else:
            raise WrongHeader("No Content-Type in headers")

    def is_finished(self):
        if self.command == "GET":
            return self._is_get_finished()
        elif self.command == "POST":
            return self._is_post_finished()
        else:
            raise MethodNotSupported

    def _parse_request(self, raw_data):
        first_line, sep, rest = self.raw_data.partition('\r\n')
        self.command, self.path, self.protocol = self._split_first_line(first_line)
        host, sep, rest = rest.partition('\r\n')
        raw_headers, self.body = self._split_headers_and_body(rest)
        self._parse_headers(raw_headers)

    def _split_headers_and_body(self, rest):
        raw_headers, sep, body = rest.partition('\r\n\r\n')
        return raw_headers, body

    def _split_first_line(self, first_line):
        command, sep, rest, = first_line.partition(' ')
        path, sep, protocol = rest.partition(' ')
        return command, path, protocol

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
