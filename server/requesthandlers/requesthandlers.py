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
        logging(str(error))
        response.status = "400 Bad Request"
        response.body = {"error": "Wrong request header"}

    sha = param["SHA256"]
    attributes = param["attributes"]
    try:
        file_content = read_from_file(sha)

        # jeśli puste, 302 err
        try:
            if file_content == "":
                raise EmptyFile
        except EmptyFile as error:
            logging(str(error))
            response.status = "302 Found"
            response.body = {"error": "Requested virus information is not ready yet, please try again later"}

        parser = Parser()
        element_list = parser.parse(file_content[0])
        finder = Finder(element_list)

        response.body = finder.find_attributes_from_list(
            attributes) if attributes else finder.find_first_page_attributes()

    except NoSuchFile as error:
        logging(str(error))
        response.status = "404 Not Found"
        response.body = {"error": "Invalid sha256"}

    return response


class EmptyFile(Exception):
    pass
