import logging

from htmlparser.finder import Finder
from htmlparser.parser import Parser
from server.customhttp import WrongHeader
from server.fileservice import read_from_file, NoSuchFile
from server.requesthandlers import vt_request


def virus_info_handler(request, response):
    try:
        param = request.json()
    except WrongHeader as error:
        logging.error(str(error))
        response.status = "400 Bad Request"
        response.body = {"error": "Wrong request header"}

    sha = param["SHA256"]
    if "attributes" in param: attributes = param["attributes"]
    try:
        file_content, sha = read_from_file(sha)

        parser = Parser()
        element_list = parser.parse(file_content)
        finder = Finder(element_list)

        response.body = finder.find_attributes_from_list(
            attributes) if "attributes" in param else finder.find_first_page_attributes()

    except NoSuchFile as error:
        logging.error(str(error))
        response.status = "404 Not Found"
        response.body = {"error": "Invalid sha256"}

    return response


class EmptyFile(Exception):
    pass
