from unittest import TestCase

from app.httprequest import HTTPRequest


class TestHTTPRequest(TestCase):
    def setUp(self):
        pass
    def test_request(self):
        request_text = '''
            'GET /who/ken/trust.html HTTP/1.1\r\n'
            'Host: cm.bell-labs.com\r\n'
            'Accept-Charset: ISO-8859-1,utf-8;q=0.7,*;q=0.3\r\n'
            'Accept: text/html;q=0.9,text/plain\r\n'
            '\r\n'
        '''
        request = HTTPRequest(request_text)
        print(request)
