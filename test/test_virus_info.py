from unittest import TestCase

import json

import requests

from server import App
from server.customhttp import HTTPRequest


class TestVirusInfo(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = App()
        cls.app.initialize()

    @classmethod
    def tearDownClass(cls):
        cls.app.exit_gracefully()

    def test_simple_attributes(self):
        payload = {'SHA256': 'b69e745d27eb131de6703ec58c4e67bc8cb8a63c0ed45ec440f4e0061f71b7d1',
                   'attributes': ['MIMEType', 'XMPToolkit', 'Producer']}
        headers = {'Content-Type': 'application/json'}

        response = requests.post('http://localhost:5005/api/virus',
                                 headers=headers,
                                 data=json.dumps(payload))
        print(response.text)
        self.assertEqual(200, response.status_code)