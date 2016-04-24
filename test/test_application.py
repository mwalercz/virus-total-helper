from unittest import TestCase

import requests

from app import App


class ApplicationTest(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = App()
        cls.app.initialize()

    @classmethod
    def tearDownClass(cls):
        cls.app.exit_gracefully()

    def test_default_request(self):
        response = requests.get('http://localhost:5005/default')
        self.assertEqual(response.text, 'Hello world')

    # sprawdza czy można dwa razy się połączyć do jednego socketa
    def test_default_request2(self):
        response = requests.get('http://localhost:5005/default')
        self.assertEqual(response.text, 'Hello world')
