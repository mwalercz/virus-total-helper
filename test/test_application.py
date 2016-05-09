import json
from unittest import TestCase

import requests

from server import App


class TestApplication(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = App()
        cls.app.initialize()

    @classmethod
    def tearDownClass(cls):
        cls.app.exit_gracefully()

    # gadamy tylko postami
    # def test_default_request(self):
    #     response = requests.get('http://localhost:5005/test/default')
    #     self.assertEqual(response.text, '{"greetings": "hello world"}')
    #
    # # sprawdza czy można dwa razy się połączyć do naszego serwera
    # def test_default_request2(self):
    #     response = requests.get('http://localhost:5005/test/default')
    #     self.assertEqual(response.text, '{"greetings": "hello world"}')

    def test_scheduler_request(self):
        # to jest ważne, nasz serwer po content-type rozroznia co jest binary a co json
        headers = {"Content-Type": "application/json"}
        payload = {"x": 5}
        response = requests.post('http://localhost:5005/test/scheduler',
                                 headers=headers,
                                 data=json.dumps(payload))
        self.assertEqual(response.text, '{"x": 5}')

    def test_binary_request(self):
        # to jest ważne, nasz serwer po content-type rozroznia co jest binary a co json
        headers = {"Content-Type": "application/octet-stream"}
        payload = b'heheheszki'
        response = requests.post('http://localhost:5005/test/binary',
                                 headers=headers,
                                 data=payload)
        # dostalismy z powrotem jsona bo nasz serwer umie tylko wysylac jsony
        self.assertEqual(response.text, '{"binary_request": "heheheszki"}')

    def test_no_such_url(self):
        response = requests.post('http://localhost:5005/test/no-such-url')
        self.assertEqual(response.status_code, 404)