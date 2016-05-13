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


    def test_status(self):
        # to jest ważne, nasz serwer po content-type rozroznia co jest binary a co json
        payload = {
            "sha256": "przykladowe_sha356",
            "cron": {
                "year" : "2017",
                "month" : "5",
                "day":"1",
                "week" : "4",
                "day_of_week" : "3",
                "hour" : "17",
                "minute" : "20",
                "second" : "59"
            }
        }
        response = requests.post('http://localhost:5005/api/scheduleVirusTotal',
                                 data=json.dumps(payload)
                                 )

        self.assertEqual( 202, response.status_code)

    def test_scheduler_reject(self):
        # to jest ważne, nasz serwer po content-type rozroznia co jest binary a co json
        payload = {
            "sha256": "przykladowe_sha356",
            "cron": {
                "seconde": "59"
            }
        }
        response = requests.post('http://localhost:5005/api/scheduleVirusTotal',
                                    data=json.dumps(payload)
                                    )

        self.assertEqual(406, response.status_code)


    def test_wrong_json(self):
        payload = {
            "sha256": "przykladowe_sha356",
            "cron": {
                "day": "1",
                "minute": "20"
            }
        }
        response = requests.post('http://localhost:5005/api/scheduleVirusTotal',
                                 data = payload
                                 )

        self.assertEqual(415, response.status_code)

    def test_wrong_cron_minute(self):
        payload = {
            "sha256": "przykladowe_sha356",
            "cron": {
                "day": "1",
                "minute": "66"
            }
        }
        response = requests.post('http://localhost:5005/api/scheduleVirusTotal',
                                 data=json.dumps(payload)
                                 )
        json_content = response.json()
        message = json_content.get("error")
        self.assertEqual(400, response.status_code)
        self.assertEqual("Wrong minute parameter", message)