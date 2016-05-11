import logging

from htmlparser.finder import Finder
from htmlparser.parser import Parser
from server.customhttp import WrongHeader, NotJsonError
from server.fileservice import read_from_file, NoSuchFile, Fileservice


class InvalidArguments(Exception):
    pass


def _get_validated_args(params):
    if len(params) == 2 and "sha256" in params and "attributes" in params and isinstance(params["attributes"], list):
        return params["sha256"], params["attributes"]
    elif len(params) == 1 and "sha256" in params:
        return params["sha256"], None
    else:
        raise InvalidArguments


def _parse_and_find(file_content, attributes):
    parser = Parser()
    element_list = parser.parse(file_content)
    finder = Finder(element_list)
    if attributes is not None:
        return finder.find_attributes_from_list(attributes)
    else:
        return finder.find_first_page_attributes()


def _process_file_and_eventually_parse(sha256, attributes):
    with Fileservice.File(sha256) as file:
        file_content = file.read()
        if file_content == "PROCESSING":
            status = "202 Accepted"
            body = {"message": "Your request is being processed, please wait some time"}
        elif file_content == "NOT_FOUND":
            status = "404 Not Found"
            body = {"message": "VirusTotal doesn't have information about your file"}
        else:
            status = "200 OK"
            body = _parse_and_find(file_content, attributes)
    return status, body


def virus_info_handler(request, response):
    try:
        json = request.json()
    except NotJsonError:
        logging.info("Given body is not json")
        response.status = "415 Unsupported Media Type"
        response.body = {"error": "Given body is not json"}
        return response
    try:
        sha256, attributes = _get_validated_args(json)
    except InvalidArguments:
        logging.info("Given arguments are invalid")
        response.status = "400 Bad Request"
        response.body = {
            "error": "Given arguments are invalid. Please provide sha256: string and attributes: [] arguments"
        }
        return response
    try:
        response.status, response.body = _process_file_and_eventually_parse(sha256, attributes)
    except NoSuchFile:
        logging.info("Invalid sha256, we dont have file with sha256: " + sha256)
        response.status = "404 Not Found"
        response.body = {"error": "Invalid sha256. We don't have your file."}
        return response
    return response
