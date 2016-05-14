# import json
# import os
# from server.fileservice import Fileservice, NoSuchFile
# import hashlib
# import requests
# from unittest import TestCase
# from server import App
# from server.fileservice import Fileservice
# from server.requesthandlers import vt_request
# from server.requesthandlers.single_request import create_processingg_file
#
#
# class test_all_request(TestCase):
#     @classmethod
#     def setUpClass(cls):
#         cls.app = App()
#         cls.app.initialize()
#
#     @classmethod
#     def tearDownClass(cls):
#         cls.app.exit_gracefully()
#
# # cycle request test
#     def test_volidation(self):
#         payload = {
#             "sha256": "przykladowe_sha356",
#             "cron": {
#                 "day": "1",
#                 "minute": "20"
#             }
#         }
#         response = requests.post('http://localhost:5005/api/scheduleVirusTotal',
#                                  data=json.dumps(payload)
#                                  )
#         self.assertNotEqual(406, response.status_code)
#
#     def test_status(self):
#         # to jest ważne, nasz serwer po content-type rozroznia co jest binary a co json
#         payload = {
#             "sha256": "przykladowe_sha356",
#             "cron": {
#                 "year": "2017",
#                 "month": "5",
#                 "day": "1",
#                 "week": "4",
#                 "day_of_week": "3",
#                 "hour": "17",
#                 "minute": "20",
#                 "second": "59"
#             }
#         }
#         response = requests.post('http://localhost:5005/api/scheduleVirusTotal',
#                                  data=json.dumps(payload)
#                                  )
#
#         self.assertEqual(202, response.status_code)
#
#     def test_scheduler_reject(self):
#         # to jest ważne, nasz serwer po content-type rozroznia co jest binary a co json
#         payload = {
#             "sha256": "przykladowe_sha356",
#             "cron": {
#                 "seconde": "59"
#             }
#         }
#         response = requests.post('http://localhost:5005/api/scheduleVirusTotal',
#                                  data=json.dumps(payload)
#                                  )
#
#         self.assertEqual(406, response.status_code)
#
#     def test_wrong_json(self):
#         payload = {
#             "sha256": "przykladowe_sha356",
#             "cron": {
#                 "day": "1",
#                 "minute": "20"
#             }
#         }
#         response = requests.post('http://localhost:5005/api/scheduleVirusTotal',
#                                  data=payload
#                                  )
#
#         self.assertEqual(415, response.status_code)
#
#     def test_wrong_cron_minute(self):
#         payload = {
#             "sha256": "przykladowe_sha356",
#             "cron": {
#                 "day": "1",
#                 "minute": "66"
#             }
#         }
#         response = requests.post('http://localhost:5005/api/scheduleVirusTotal',
#                                  data=json.dumps(payload)
#                                  )
#         json_content = response.json()
#         message = json_content.get("error")
#         self.assertEqual(400, response.status_code)
#         self.assertEqual("Wrong minute parameter", message)
#
# # /cycle request test
#
# # single request test
#     def test_status(self):
#         payload = b'sprawdzamy_pojedyncze_zapytanie'
#         response = requests.post('http://localhost:5005/api/singleVirusTotal',
#                                     data=payload)
#         # dostalismy z powrotem jsona bo nasz serwer umie tylko wysylac jsony
#         self.assertEqual(202, response.status_code)
#
#     def test_sha256(self):
#         payload = b'sprawdzamy_pojedyncze_zapytanie'
#         response = requests.post('http://localhost:5005/api/singleVirusTotal',
#                                     data=payload)
#         data = response.json()
#         responseSha256 = data.get('sha256')
#         expectedShaObcjet = hashlib.sha256(payload)
#         expectedSha = expectedShaObcjet.hexdigest()
#         self.assertEqual(responseSha256, expectedSha)
#
#     def test_processing_fiel(self):
#         create_processingg_file("processing")
#         with Fileservice.File("processing") as file:
#             file_content = file.read()
#             self.assertEqual(file_content, "PROCESSING")
#             file.write("It shouldn't exist")
#             file.remove()
# # /single request test
#
# # test virus_info request
#     def test_simple_attributes(self):
#         payload = {'sha256': 'found',
#                     'attributes': ['MIMEType', 'XMPToolkit', 'Producer']}
#         response = requests.post('http://localhost:5005/api/virus',
#                                              data=json.dumps(payload))
#         self.assertEqual(200, response.status_code)
#
#     def test_no_attributes(self):
#         payload = {'sha256': 'found'}
#         response = requests.post('http://localhost:5005/api/virus',
#                                         data=json.dumps(payload))
#         self.assertEqual(200, response.status_code)
#
#     def test_bad_json_syntax(self):
#         payload = "{\"sha256\": \"found\" ,}"  # przecinek na końcu!
#         response = requests.post('http://localhost:5005/api/virus',
#                                     data=payload)
#         self.assertEqual(415, response.status_code)
#
#     def test_invalid_arguments_attributes(self):
#         payload = {'sha256': 'found',
#                     "ATTRIBUTES": ["MIMEType"]}
#         response = requests.post('http://localhost:5005/api/virus',
#                                     data=json.dumps(payload))
#         self.assertEqual(400, response.status_code)
#
#     def test_invalid_arguments_sha256(self):
#         payload = {'SHA256': 'found'}
#         response = requests.post('http://localhost:5005/api/virus',
#                                     data=json.dumps(payload))
#         self.assertEqual(400, response.status_code)
#
#     def test_not_list_in_attributes(self):
#         payload = {'sha256': 'found',
#                     "attributes": "MIMEType"}
#         response = requests.post('http://localhost:5005/api/virus',
#                                     data=json.dumps(payload))
#         self.assertEqual(400, response.status_code)
#
#     def test_not_found(self):
#         payload = {'sha256': 'not-exists'}
#         response = requests.post('http://localhost:5005/api/virus',
#                                     data=json.dumps(payload))
#         self.assertEqual(404, response.status_code)
# # /test virus_info request
#
# # test VT request
#     def test_not_found(self):
#         sha256 = 'test_not_found'
#         vt_request.not_found(sha256)
#         with Fileservice.File(sha256) as file:
#             file_content = file.read()
#             self.assertEqual(file_content, "NOT FOUND")
#             file.write("PROCESSING")
#             file_content = file.read()
#             self.assertEqual(file_content, "PROCESSING")
#
#
# # /test VT request
#
# # test Fileservice
#
# def test_read_wrong_file(self):
#     test_sha265 = "4321"
#     path = Fileservice._get_filename(test_sha265)
#     if os.path.isfile(path):
#         os.remove(path)
#     with self.assertRaises(NoSuchFile):
#         with Fileservice.File(test_sha265) as file:
#             file.read()
#
#
# def test_read_write(self):
#     test_string = "Omijając kwieciste ostrowy burzanu"
#     test_sha256 = "1234"
#     with Fileservice.File(test_sha256) as file:
#         file.write(test_string)
#         file_content = file.read()
#     self.assertEqual(file_content, test_string)
#
#
# def test_exists(self):
#     with Fileservice.File("file-doesnt-exist") as file:
#         if file.exists():
#             self.assertTrue(False, "nigdy nie powinnismy tutaj wejsc")
#
#
# def test_remove(self):
#     with Fileservice.File("remove") as file:
#         file.write("remove it!")
#         self.assertTrue(file.exists())
#         file.remove()
#         self.assertFalse(file.exists())
#
# # /test Fileservice