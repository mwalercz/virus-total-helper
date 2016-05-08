from unittest import TestCase
import requests
import json
import hashlib
from server import App

class TestSingleRequest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = App()
        cls.app.initialize()

    @classmethod
    def tearDownClass(cls):
        cls.app.exit_gracefully()


    def test_single_request(self):
        # to jest ważne, nasz serwer po content-type rozroznia co jest binary a co json
        headers = {"Content-Type": "application/octet-stream"}
        payload = b'sprawdzamy_pojedyncze_zapytanie'
        response = requests.post('http://localhost:5005/test/binary',
                                 headers=headers,
                                 data=payload)
        # dostalismy z powrotem jsona bo nasz serwer umie tylko wysylac jsony
        self.assertEqual( 202, response.status_code)
        # responseSha256 = response.body.sha256
        # expectedSha256 = hashlib.sha256(payload)
        print(response.status_code)
        # self.assertEqual(responseSha256, expectedSha256)
#
