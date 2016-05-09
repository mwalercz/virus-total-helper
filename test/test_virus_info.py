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
        payload = {'SHA256': '70ed0f6db9c50f9d05f3497386dba768f5efef59b6709c682bbc1951a93c47bf',
                   'attributes': ['MIMEType', 'XMPToolkit', 'Producer']}
        headers = {'Content-Type': 'application/json'}

        response = requests.post('http://localhost:5005/api/virus',
                                 headers=headers,
                                 data=json.dumps(payload))
        print(response.text)
        self.assertEqual(200, response.status_code)