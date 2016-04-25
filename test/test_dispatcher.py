from unittest import TestCase

from app.dispatcher import Dispatcher, ArgumentLookupError
from app.http import HTTPResponse


def request_handler(request, response):
    response.body = {"request_handler": str(request)}
    return response


def request_scheduler_handler(request, response, scheduler):
    response.body = {"request_scheduler_handler": str(request)}
    return response


URLS = {'POST/schedule': request_scheduler_handler,
        'GET/request': request_handler}


class TestDispatcherAndResponse(TestCase):
    def setUp(self):
        self.urls = URLS
        self.scheduler = 'scheduler'
        self.dispatcher = Dispatcher(self.urls, self.scheduler)

    def test_request(self):
        response = self.dispatcher.dispatch(RequestMock('GET', '/request'))
        self.assertEqual(str(response), 'HTTP/1.1 200 OK\r\n'
                                        'Content-Type: application/json\r\n\r\n'
                                        '{"request_handler": "GET/request"}')

    def test_request_scheduler(self):
        response = self.dispatcher.dispatch(RequestMock('POST', '/schedule'))
        self.assertEqual(str(response), 'HTTP/1.1 200 OK\r\n'
                                        'Content-Type: application/json\r\n\r\n'
                                        '{"request_scheduler_handler": "POST/schedule"}')

    def test_fail_key(self):
        try:
            response = self.dispatcher.dispatch(RequestMock('GET', '/json'))
        except KeyError:
            response = 'KeyError'
        self.assertEqual(response, 'KeyError')


class RequestMock:
    def __init__(self, command, path):
        self.command = command
        self.path = path

    def __str__(self):
        return self.command + self.path

    def json(self):
        return {'key1': 'value1', 'key2': 'value2'}

    def binary(self):
        return b'binary'
