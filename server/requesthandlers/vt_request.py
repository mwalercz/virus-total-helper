#author: Marek
import logging

import requests
from server.fileservice import write_to_file

def request_to_vt(sha256):
    url = 'https://www.virustotal.com/en/file/' + sha256 + '/analysis/'
    responseVT = requests.get(url)
    data = responseVT.content
    empty_file = b''

    if(data == empty_file):
        logging.info("No file with sha256:" + sha256 + " on VirusTotal.")
        return
    else:
        write_to_file(sha256, data)