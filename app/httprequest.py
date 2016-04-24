import json
import re


class HTTPRequest:
    def __init__(self, raw_data):
        self.raw_data = raw_data
        self.path = None
        self.command = None
        self.body = None
        self._parse_request()

    def _parse_request(self):
        first_line, host, rest = self.raw_data.split(sep='\r\n', maxsplit=2)
        self.command, self.path, protocol = first_line.split(maxsplit=2)
        line_end = re.compile(r'\r\n\r\n')
        headers, self.body = line_end.split(rest, maxsplit=1)

    def json(self):
        return json.loads(self.body)
