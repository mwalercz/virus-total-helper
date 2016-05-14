# from unittest import TestCase
#
# import json
#
# import requests
#
# from server import App
# from server.customhttp import HTTPRequest
#
#
# class TestVirusInfo(TestCase):
#     @classmethod
#     def setUpClass(cls):
#         cls.app = App()
#         cls.app.initialize()
#
#     @classmethod
#     def tearDownClass(cls):
#         cls.app.exit_gracefully()
#
#     def test_simple_attributes(self):
#         payload = {'sha256': 'found',
#                    'attributes': ['MIMEType', 'XMPToolkit', 'Producer']}
#         response = requests.post('http://localhost:5005/api/virus',
#                                  data=json.dumps(payload))
#         self.assertEqual(200, response.status_code)
#
#     def test_no_attributes(self):
#         payload = {'sha256': 'found'}
#         response = requests.post('http://localhost:5005/api/virus',
#                                  data=json.dumps(payload))
#         self.assertEqual(200, response.status_code)
#
#     def test_bad_json_syntax(self):
#         payload = "{\"sha256\": \"found\" ,}"  # przecinek na końcu!
#         response = requests.post('http://localhost:5005/api/virus',
#                                  data=payload)
#         self.assertEqual(415, response.status_code)
#
#     def test_invalid_arguments_attributes(self):
#         payload = {'sha256': 'found',
#                    "ATTRIBUTES": ["MIMEType"]}
#         response = requests.post('http://localhost:5005/api/virus',
#                                  data=json.dumps(payload))
#         self.assertEqual(400, response.status_code)
#
#     def test_invalid_arguments_sha256(self):
#         payload = {'SHA256': 'found'}
#         response = requests.post('http://localhost:5005/api/virus',
#                                  data=json.dumps(payload))
#         self.assertEqual(400, response.status_code)
#
#     def test_not_list_in_attributes(self):
#         payload = {'sha256': 'found',
#                    "attributes": "MIMEType"}
#         response = requests.post('http://localhost:5005/api/virus',
#                                  data=json.dumps(payload))
#         self.assertEqual(400, response.status_code)
#
#     def test_not_found(self):
#         payload = {'sha256': 'not-exists'}
#         response = requests.post('http://localhost:5005/api/virus',
#                                  data=json.dumps(payload))
#         self.assertEqual(404, response.status_code)
