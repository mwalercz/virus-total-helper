from unittest import TestCase

from server.customhttp import HTTPRequest


class TestHTTPRequest(TestCase):
    def test_post_req(self):
        data = b'POST /haha HTTP/1.1\r\n' \
               b'Host: onet.pl\r\n' \
               b'Content-Type: application/json\r\n' \
               b'Cache-Control: no-cache\r\n' \
               b'Postman-Token: 3f51ed67-38ae-48be-c787-873d3bf96ac5\r\n\r\n' \
               b'{"key1": "value1", "key2": "value2"}'

        request = HTTPRequest(data)
        real_json = request.json()
        expected_json = {"key1": "value1", "key2": "value2"}
        self.assertEqual(real_json, expected_json)
        self.assertEqual(request.command, "POST")
        self.assertEqual(request.path, "/haha")
