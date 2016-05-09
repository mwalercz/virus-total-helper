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

        payload1 = {'sha256': 'b69e745d27eb131de6703ec58c4e67bc8cb8a63c0ed45ec440f4e0061f71b7d1',
                    'attributes': ['MIMEType', 'XMPToolkit', 'Producer']}
        payload2 = {'sha256': 'b69e745d27eb131de6703ec58c4e67bc8cb8a63c0ed45ec440f4e0061f71b7d1'}
        payload404 = {'sha256': 'nie_istnieje131de6703ec58c4e67bc8cb8a63c0ed45ec440f4e0061f71b7d1',
                    'attributes': ['MIMEType', 'XMPToolkit', 'Producer']}

        response200a = requests.post('http://localhost:5005/api/virus',
                                    headers=headers,
                                    data=json.dumps(payload1))
        response200b = requests.post('http://localhost:5005/api/virus',
                                    headers=headers,
                                    data=json.dumps(payload2))
        response400 = requests.post('http://localhost:5005/api/virus',
                                    headers=headers400,
                                    data=json.dumps(payload1))
        response404 = requests.post('http://localhost:5005/api/virus',
                                    headers=headers,
                                    data=json.dumps(payload404))
        response500 = requests.post('http://localhost:5005/api/virus',
                                    headers=headers,
                                    json=json.dumps(payload2))

        self.assertEqual(200, response200a.status_code)
        self.assertEqual(200, response200b.status_code)
        self.assertEqual(400, response400.status_code)
        self.assertEqual(404, response404.status_code)
        self.assertEqual(500, response500.status_code)