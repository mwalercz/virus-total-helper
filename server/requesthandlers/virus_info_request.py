import logging

from htmlparser.finder import Finder
from htmlparser.parser import Parser
from server.customhttp import WrongHeader
from server.fileservice import read_from_file, NoSuchFile


def virus_info_handler(request, response):
    try:
        params = request.json()
    except WrongHeader as error:
        logging.error(str(error))
        response.status = "400 Bad Request"
        response.body = {"error": "Wrong request header"}
        return response
    sha = params["sha256"]
    try:
        file_content = read_from_file(sha)
    except NoSuchFile as error:
        logging.error(str(error))
        response.status = "404 Not Found"
        response.body = {"error": "Invalid sha256"}
        return response

    parser = Parser()
    element_list = parser.parse(file_content)
    finder = Finder(element_list)
    if "attributes" in params:
        response.body = finder.find_attributes_from_list(params["attributes"])
    else:
        response.body = finder.find_first_page_attributes()
    return response
