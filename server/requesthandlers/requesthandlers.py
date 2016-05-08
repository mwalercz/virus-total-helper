import logging
import hashlib
import requests

from htmlparser.finder import Finder
from htmlparser.parser import Parser
from server.fileservice import read_from_file, write_to_file, NoSuchFile


def virus_info_handler(request, response):
    param = request.json()
    sha = int(param["sha256"])
    attributes = param["attributes"]
    try:
        file_content = read_from_file(sha)
        parser = Parser()
        element_list = parser.parse(file_content)
        finder = Finder(element_list)

        response.body = finder.find_attributes_from_list(
            attributes) if attributes else finder.find_first_page_attributes()

    except NoSuchFile as error:
        logging(str(error))
        response.status = "404 Not found"
        response.body = {"error": "Invalid sha256"}

    return response

#Marek
#pojdeyncze zapytanie do VT
def single_handler(request, response, scheduler):
    # obliczamy sha256 dla pliku binarnego
    binary = request.binary()
    sha256 = hashlib.sha256(binary)

    # dajemy odpowiedz
    response.status = "202 Accepted"
    response.body = {
        "sha256": sha256,
        "message": "Task has been accepted, please ask us again about that file in some time using method /api/virus"
    }
    url = 'https://www.virustotal.com/en/file/' + (sha256) + '/analysis/'
    responseVT = requests.post(url)

    # zapisanie do pliku
    write_to_file(sha256, responseVT)

    # zwracamy response
    return response
