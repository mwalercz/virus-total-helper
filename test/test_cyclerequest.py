import requests
import json

from unittest import TestCase
from server import App


class TestCycleRequest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = App()
        cls.app.initialize()

    @classmethod
    def tearDownClass(cls):
        cls.app.exit_gracefully()

    def test_header(self):
        headers = {"Content-Type": "application/octet-stream"}
        payload = {
            "sha256": "przykladowe_sha356",
            "cron": {
                "day": "2",
                "minute": "40"
            }
        }
        response = requests.post('http://localhost:5005/api/scheduleVirusTotal',
                                 headers=headers)
        self.assertEqual(415, response.status_code)

    def test_status(self):
        # to jest ważne, nasz serwer po content-type rozroznia co jest binary a co json
        headers = {"Content-Type": "application/json"}
        payload = {
            "sha256": "przykladowe_sha356",
            "cron": {
                "day":"1",
                "minute" : "20"
            }
        }
        response = requests.post('http://localhost:5005/api/scheduleVirusTotal',
                                 headers=headers,
                                 data=json.dumps(payload)
                                 )

        self.assertEqual( 202, response.status_code)