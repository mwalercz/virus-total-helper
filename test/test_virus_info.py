from unittest import TestCase

import json

import requests

from server.customhttp import HTTPRequest


class TestVirusInfo(TestCase):
#    def setUp(self):
 #       self.parser = Parser()

    def test_simple_attributes(self):
        payload = {'SHA256': '70ed0f6db9c50f9d05f3497386dba768f5efef59b6709c682bbc1951a93c47bf',
                   'attributes': ['MIMEType', 'XMPToolkit', 'Producer']}
        headers = {'Content-Type': 'application/json'}

        response = requests.post('http://localhost:5005/api/virus/',
                                 headers=headers,
                                 data=json.dumps(payload))
        print(response.text)
        self.assertEqual(200, response.status_code)

        #attributes = ["XMPToolkit", "MIMEType"]
        #element_list = self.parser.parse(data)
        #finder = Finder(element_list)
        #real_attributes_found = finder.find_attributes_from_list(attributes)
        #expected_attributes_found = {"MIMEType": "application/pdf", "XMPToolkit": "XMP toolkit 2.9.1-13, framework 1.6"}
        #self.assertEqual(real_attributes_found, expected_attributes_found)