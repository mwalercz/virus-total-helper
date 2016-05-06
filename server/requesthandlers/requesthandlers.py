import logging

from htmlparser.finder import Finder
from htmlparser.parser import Parser
from server.fileservice import read_from_file, NoSuchFile


def virus_info_handler(request, response):
    param = request.json()
    sha = int(param["sha256"])
    attributes = param["attributes"]
    try:
        file_content = read_from_file(sha)
        parser = Parser()
        element_list = parser.parse(file_content)
        finder = Finder(element_list)

        response.body = finder.find_attributes_from_list(attributes) if attributes else finder.find_first_page_attributes()

    except NoSuchFile as error:
        logging(str(error))
        response.status = "404 Not found"
        response.body = {"error": "Invalid sha256"}

    return response
