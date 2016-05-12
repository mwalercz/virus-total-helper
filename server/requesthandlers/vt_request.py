# author: Marek
#biblioteka BeautifulSoup sluzy do przegladania pliku .html i wyszukiwania w nim odpowiedniego naglowka
import logging

import requests
from server.fileservice import Fileservice
from bs4 import BeautifulSoup


def request_to_vt(sha256):
    headers = {"Cache-Control": "no-cache",
               "Accept": "text/html",
               "Connection": "keep-alive",
               "Accept-Language": "pl,en-US;q=0.7,en;q=0.3",
               "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:46.0) Gecko/20100101 Firefox/46.0"}
    url = 'https://www.virustotal.com/en/file/' + sha256 + '/analysis/'
    try:
        responsevt = requests.get(url, headers=headers)
    except Exception:
        logging.error("No internet connection! Couldn't connect with virustotal.com")
        return
    data = responsevt.text
    soup = BeautifulSoup(data, 'html.parser')
    mydiv = soup.findAll('h2', {"class" : "alert-heading"})

    empty_file = ""
    # TODO: sprawdzic czy otrzymany plik jest pusty
    if mydiv != empty_file:
        with Fileservice.File(sha256) as file:
            if file.read() == "PROCESSING":
                file.write("NOT FOUND")
        logging.info("File " + sha256 + ".html is empty")
    else:
        with Fileservice.File(sha256) as file:
            data = file.read()
            # print(data)
            file.write(data)
            logging.info("File: " + sha256 + ".html updated")
