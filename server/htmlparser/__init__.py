from .finder import Finder
from .parser import Parser


def init_parser_and_finder(file_content):
    parser = Parser()
    element_list = parser.parse(file_content)
    finder = Finder(element_list)
    return finder


def is_not_found_on_vt(file_content):
    finder = init_parser_and_finder(file_content)
    return file_content == "" or \
           finder.is_content_present("File not found", "Page not found")


def parse_and_find(file_content, attributes):
    finder = init_parser_and_finder(file_content)
    if attributes is not None:
        return finder.find_attributes_from_list(attributes)
    else:
        return finder.find_first_page_attributes()
