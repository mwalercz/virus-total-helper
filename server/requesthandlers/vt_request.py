# author: Marek
import logging

import requests
from server.fileservice import write_to_file


def request_to_vt(sha256):
    headers = {"Cache-Control": "no-cache",
               "Cookie": "__utma=194538546.1374540295.1458168968.1462804416.1462835638.29; __utmz=194538546.1462534007.22.10.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); VT_CSRF=7307f46a6f03a9a38eed4f19c801187a; VT_PREFERRED_LANGUAGE=en; __utmb=194538546.2.10.1462835638; __utmc=194538546; __utmt=1",
               "Accept": "text/html",
               "Connection": "keep-alive",
               "Accept-Language": "pl,en-US;q=0.7,en;q=0.3",
               "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:46.0) Gecko/20100101 Firefox/46.0"}
    url = 'https://www.virustotal.com/en/file/' + sha256 + '/analysis/'
    responseVT = requests.get(url, headers=headers)
    data = responseVT.text
    empty_file = ""
    if (data == empty_file):
        logging.info("No file with sha256:" + sha256 + " on VirusTotal.")
    else:
        write_to_file(sha256, data)
