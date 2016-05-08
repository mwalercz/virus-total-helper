import logging
import hashlib
import requests

from htmlparser.finder import Finder
from htmlparser.parser import Parser
from server.customhttp import WrongHeader
from server.fileservice import read_from_file, NoSuchFile
from server.requesthandlers import vt_request


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


# Marek
# pojdeyncze zapytanie do VT
# TODO: obsluzyc wyjatek rzucany prze request.binary()
def single_handler(request, response, scheduler):
    # obliczamy sha256 dla pliku binarnego
    try:
        binary = request.binary()
    except WrongHeader:
        logging.error("Wrong Header! Expected: octet-stream")
        response.status = "415 Unsupported Media Type"
        response.body = {
            "error": "Please use content_type: application/octet-stream"
        }
        return response


    sha256 = hashlib.sha256(binary)
    sha = sha256.hexdigest()

    # tworzymy response
    response.status = "202 Accepted"
    response.body = {
        "sha256": sha,
        "message": "Task has been accepted, please ask us again about that file in some time using method /api/virus"
    }

    # pojedyncze zapytanie do VT
    scheduler.add_job(lambda: vt_request.request_to_VT(sha))

    return response