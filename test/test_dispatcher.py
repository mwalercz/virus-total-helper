from unittest import TestCase

from app.dispatcher import Dispatcher, ArgumentLookupError


def request_handler(request):
    return "request_handler: request: " + str(request)


def request_scheduler_handler(request, scheduler):
    return "request_scheduler: request: " + str(request) + ", scheduler: " + str(scheduler)


URLS = {'POST/schedule': request_scheduler_handler,
        'GET/request': request_handler}


class TestDispatcher(TestCase):
    def setUp(self):
        self.urls = URLS
        self.scheduler = 'scheduler'
        self.dispatcher = Dispatcher(self.urls, self.scheduler)

    def test_request(self):
        response = self.dispatcher.dispatch(RequestMock('GET', '/request'))
        self.assertEqual(response, "request_handler: request: GET/request")

    def test_request_scheduler(self):
        response = self.dispatcher.dispatch(RequestMock('POST', '/schedule'))
        self.assertEqual(response, "request_scheduler: request: " +
                         'POST/schedule' + ", scheduler: " + self.scheduler)

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
        return 'binary'
