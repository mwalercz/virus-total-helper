from unittest import TestCase
import requests
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

    def test_status(self):
        payload = b'sprawdzamy_pojedyncze_zapytanie'
        response = requests.post('http://localhost:5005/api/singleVirusTotal',
                                 data=payload)
        # dostalismy z powrotem jsona bo nasz serwer umie tylko wysylac jsony
        self.assertEqual(202, response.status_code)

    def test_sha256(self):
        payload = b'sprawdzamy_pojedyncze_zapytanie'
        response = requests.post('http://localhost:5005/api/singleVirusTotal',
                                 data=payload)
        data = response.json()
        responseSha256 = data.get('sha256')
        expectedShaObcjet = hashlib.sha256(payload)
        expectedSha = expectedShaObcjet.hexdigest()
        self.assertEqual(responseSha256, expectedSha)

