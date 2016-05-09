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

        headers = {'Content-Type': 'application/json'}
        headers400 = {'Content-Type': 'application/octet-stream'}

        payload200a = {'SHA256': 'b69e745d27eb131de6703ec58c4e67bc8cb8a63c0ed45ec440f4e0061f71b7d1',
                    'attributes': ['MIMEType', 'XMPToolkit', 'Producer']}
        payload200b = {'SHA256': 'b69e745d27eb131de6703ec58c4e67bc8cb8a63c0ed45ec440f4e0061f71b7d1'}
        payload400 = {'SHA256': 'b69e745d27eb131de6703ec58c4e67bc8cb8a63c0ed45ec440f4e0061f71b7d1',
                    'attributes': ['MIMEType', 'XMPToolkit', 'Producer']}
        payload404 = {'SHA256': 'nie_istnieje131de6703ec58c4e67bc8cb8a63c0ed45ec440f4e0061f71b7d1',
                    'attributes': ['MIMEType', 'XMPToolkit', 'Producer']}
        payload500 = {'SHA256': 'pusty45d27eb131de6703ec58c4e67bc8cb8a63c0ed45ec440f4e0061f71b7d1',
                    'attributes': ['MIMEType', 'XMPToolkit', 'Producer']}

        response200a = requests.post('http://localhost:5005/api/virus',
                                    headers=headers,
                                    data=json.dumps(payload200a))
        response200b = requests.post('http://localhost:5005/api/virus',
                                    headers=headers,
                                    data=json.dumps(payload200b))
        response400 = requests.post('http://localhost:5005/api/virus',
                                    headers=headers400,
                                    data=json.dumps(payload400))
        response404 = requests.post('http://localhost:5005/api/virus',
                                    headers=headers,
                                    data=json.dumps(payload404))
        response500 = requests.post('http://localhost:5005/api/virus',
                                    headers=headers,
                                    data=json.dumps(payload500))

        self.assertEqual(200, response200a.status_code)
        self.assertEqual(200, response200b.status_code)
        self.assertEqual(400, response400.status_code)
        self.assertEqual(404, response404.status_code)
        self.assertEqual(500, response500.status_code)