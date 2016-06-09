import json


class MethodNotSupported(Exception):
    pass


class NotJsonError(Exception):
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
        try:
            return json.loads(self.body.decode("utf-8"))
        except Exception:
            raise NotJsonError

    def is_content_app_json(self):
        return "Content-Type" in self.headers and "application/json" in self.headers["Content-Type"]


    def is_json(self):
        try:
            json.loads(self.body.decode("utf-8"))
        except Exception:
            return False
        return True

    def binary(self):
        return self.body

    def is_finished(self):
        if self.command == "POST":
            return self._is_post_finished()
        else:
            raise MethodNotSupported

    def _parse_request(self, raw_data):
        raw_beginning, self.body = self._split_headers_and_body(raw_data)
        beginning = raw_beginning.decode("utf-8")
        first_line, sep, rest = beginning.partition('\r\n')
        self.command, self.path, self.protocol = self._split_first_line(first_line)
        host, sep, rest = rest.partition('\r\n')
        self._parse_headers(rest)

    def _split_headers_and_body(self, raw_data):
        index = raw_data.find(b'\r\n\r\n')
        raw_beginning = raw_data[:index]
        body = raw_data[index + 4:]
        return raw_beginning, body

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
