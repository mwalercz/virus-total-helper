import requests

from server import App
from unittest import TestCase
from server.fileservice import Fileservice

class TestVtRequest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = App()
        cls.app.initialize()

    @classmethod
    def tearDownClass(cls):
        cls.app.exit_gracefully


    def test_not_found(self):
        payload = b'nieznany_plik'
        response = requests.post('http://localhost:5005/api/singleVirusTotal',
                                 data=payload)
        data = response.json()
        sha256 = data.get('sha256')
        with Fileservice.File(sha256) as file:
            file_content = file.read()
            self.assertEqual(file_content, "NOT FOUND")
            file.write("Test it!")
