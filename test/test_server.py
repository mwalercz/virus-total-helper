import json
import os

from htmlparser import is_not_found_on_vt
from server.fileservice import Fileservice, NoSuchFile
import hashlib
import requests
from unittest import TestCase
from server import Server
from server.fileservice import Fileservice
from server.requesthandlers.single_request import create_processingg_file


class TestApplication(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = Server()
        cls.server.try_serve()

    @classmethod
    def tearDownClass(cls):
        cls.server.exit_gracefully()

    # simple requests test
    def test_scheduler_request(self):
        payload = {"x": 5}
        response = requests.post('http://localhost:5005/test/scheduler',
                                 data=json.dumps(payload))
        self.assertEqual(response.text, '{"x": 5}')

    def test_binary_request(self):
        payload = b'heheheszki'
        response = requests.post('http://localhost:5005/test/binary',
                                 data=payload)
        # dostalismy z powrotem jsona bo nasz serwer umie tylko wysylac jsony
        self.assertEqual(response.text, '{"binary_request": "heheheszki"}')

    def test_no_such_url(self):
        response = requests.post('http://localhost:5005/test/no-such-url')
        self.assertEqual(response.status_code, 404)

    # / simple requests test

    # cycle request test
    def test_volidation(self):
        payload = {
            "sha256": "przykladowe_sha356",
            "cron": {
                "day": "1",
                "minute": "20"
            }
        }
        response = requests.post('http://localhost:5005/api/scheduleVirusTotal',
                                 data=json.dumps(payload)
                                 )
        self.assertNotEqual(406, response.status_code)

    def test_status(self):
        payload = {
            "sha256": "przykladowe_sha356",
            "cron": {
                "year": "2017",
                "month": "5",
                "day": "1",
                "week": "4",
                "day_of_week": "3",
                "hour": "17",
                "minute": "20",
                "second": "59"
            }
        }
        response = requests.post('http://localhost:5005/api/scheduleVirusTotal',
                                 data=json.dumps(payload)
                                 )

        self.assertEqual(202, response.status_code)

    def test_scheduler_reject(self):
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
                                 data=payload
                                 )

        self.assertEqual(415, response.status_code)

    # /cycle request test

    # single request test
    def test_single_status(self):
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

    def test_processing_file(self):
        create_processingg_file("processing")
        with Fileservice.File("processing") as file:
            file_content = file.read()
            self.assertEqual(file_content, "PROCESSING")
            file.write("It shouldn't exist")
            file.remove()
    # /single request test

    #  virus_info request test
    def test_simple_attributes(self):
        payload = {'sha256': 'found',
                   'attributes': ['MIMEType', 'XMPToolkit', 'Producer']}
        response = requests.post('http://localhost:5005/api/virus',
                                 data=json.dumps(payload))
        self.assertEqual(200, response.status_code)

    def test_no_attributes(self):
        payload = {'sha256': 'found'}
        response = requests.post('http://localhost:5005/api/virus',
                                 data=json.dumps(payload))
        self.assertEqual(200, response.status_code)

    def test_bad_json_syntax(self):
        payload = "{\"sha256\": \"found\" ,}"  # przecinek na końcu!
        response = requests.post('http://localhost:5005/api/virus',
                                 data=payload)
        self.assertEqual(415, response.status_code)

    def test_invalid_arguments_attributes(self):
        payload = {'sha256': 'found',
                   "ATTRIBUTES": ["MIMEType"]}
        response = requests.post('http://localhost:5005/api/virus',
                                 data=json.dumps(payload))
        self.assertEqual(400, response.status_code)

    def test_invalid_arguments_sha256(self):
        payload = {'SHA256': 'found'}
        response = requests.post('http://localhost:5005/api/virus',
                                 data=json.dumps(payload))
        self.assertEqual(400, response.status_code)

    def test_not_list_in_attributes(self):
        payload = {'sha256': 'found',
                   "attributes": "MIMEType"}
        response = requests.post('http://localhost:5005/api/virus',
                                 data=json.dumps(payload))
        self.assertEqual(400, response.status_code)

    def test_not_exists(self):
        payload = {'sha256': 'not-exists'}
        response = requests.post('http://localhost:5005/api/virus',
                                 data=json.dumps(payload))
        self.assertEqual(404, response.status_code)

    # / virus_info request test

    # VT request test
    def test_not_found(self):
        sha256 = 'test_not_found'
        with Fileservice.File(sha256) as file:
            file_content = file.read()
            self.assertEqual(file_content, "PROCESSING")
            file.write("PROCESSING")

    # /VT request test

    # Fileservice test

    def test_read_wrong_file(self):
        test_sha265 = "4321"
        path = Fileservice._get_filename(test_sha265)
        if os.path.isfile(path):
            os.remove(path)
        with self.assertRaises(NoSuchFile):
            with Fileservice.File(test_sha265) as file:
                file.read()

    def test_read_write(self):
        test_string = "Omijając kwieciste ostrowy burzanu"
        test_sha256 = "1234"
        with Fileservice.File(test_sha256) as file:
            file.write(test_string)
            file_content = file.read()
        self.assertEqual(file_content, test_string)

    def test_exists(self):
        with Fileservice.File("file-doesnt-exist") as file:
            if file.exists():
                self.assertTrue(False, "nigdy nie powinnismy tutaj wejsc")

    def test_remove(self):
        with Fileservice.File("remove") as file:
            file.write("remove it!")
            self.assertTrue(file.exists())
            file.remove()
            self.assertFalse(file.exists())

    # /Fileservice test

    # Htmlparser test

    def test_is_not_found_on_vt(self):
        with Fileservice.File("not_found_on_vt") as file:
            file_content = file.read()

        bool = is_not_found_on_vt(file_content)
        self.assertTrue(bool)

    def test_is_found_on_vt(self):
        with Fileservice.File("found") as file:
            file_content = file.read()

        bool = is_not_found_on_vt(file_content)
        self.assertFalse(bool)

    # /Htmlparser test

