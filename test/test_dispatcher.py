from unittest import TestCase

from app.dispatcher import Dispatcher, ArgumentLookupError


def json_handler(json):
    return "json_handler: json: " + str(json)


def binary_handler(binary):
    return "binary_handler: binary: " + str(binary)


def request_handler(request):
    return "request_handler: request: " + str(request)


def request_wrong_args(wrong_arg):
    return "wrong_arg_handler: wrong_arg: " + str(wrong_arg)


URLS = {'POST/json': json_handler,
        'POST/binary': binary_handler,
        'GET/request': request_handler,
        'POST/wrong_args': request_wrong_args}


class TestDispatcher(TestCase):
    def setUp(self):
        self.urls = URLS
        self.dispatcher = Dispatcher(self.urls)

    def test_json(self):
        request = RequestMock('POST', '/json')
        response = self.dispatcher.dispatch_request(request)
        self.assertEqual(response, "json_handler: json: " + str(request.get_json()))

    def test_binary(self):
        request = RequestMock('POST', '/binary')
        response = self.dispatcher.dispatch_request(request)
        self.assertEqual(response, "binary_handler: binary: " + str(request.get_binary()))

    def test_request(self):
        response = self.dispatcher.dispatch_request(RequestMock('GET', '/request'))
        self.assertEqual(response, "request_handler: request: GET/request")

    def test_fail_key(self):
        try:
            response = self.dispatcher.dispatch_request(RequestMock('GET', '/json'))
        except KeyError:
            response = 'KeyError'
        self.assertEqual(response, 'KeyError')

    def test_fail_arguments(self):
        try:
            response = self.dispatcher.dispatch_request(RequestMock('POST', '/wrong_args'))
        except ArgumentLookupError:
            response = 'ArgumentLookupError'
        self.assertEqual(response, 'ArgumentLookupError')


class RequestMock:
    def __init__(self, command, path):
        self.command = command
        self.path = path

    def __str__(self):
        return self.command + self.path

    def get_json(self):
        return {'key1': 'value1', 'key2': 'value2'}

    def get_binary(self):
        return 'binary'
