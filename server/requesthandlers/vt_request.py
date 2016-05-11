# author: Marek
import logging

import requests
from server.fileservice import write_to_file


def request_to_vt(sha256):
    headers = {"Cache-Control": "no-cache",
               "Accept": "text/html",
               "Connection": "keep-alive",
               "Accept-Language": "pl,en-US;q=0.7,en;q=0.3",
               "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:46.0) Gecko/20100101 Firefox/46.0"}
    url = 'https://www.virustotal.com/en/file/' + sha256 + '/analysis/'
    try:
        responseVT = requests.get(url, headers=headers)
    except Exception:
        logging.error("No internet connection! Couldn't connect with virustotal.com")
        return
    data = responseVT.text
    empty_file = ""
    if data == empty_file:
        logging.info("No file with sha256:" + sha256 + " on VirusTotal.")
    else:
        write_to_file(sha256, data)
