import collections
import logging

from .parser import Content, Tag


class NoSuchAttribute(Exception):
    pass


class Finder:
    def __init__(self, element_list):
        self.first_page_simple_element_list = ['SHA256', 'File name', 'Detection ratio', 'Analysis date']
        self.element_list = element_list
        self.content_list = []
        for element in self.element_list:
            if isinstance(element, Content):
                self.content_list.append(element)

    def find_attributes_from_list(self, attributes_to_find):
        attributes_found = collections.OrderedDict()
        for element_to_find in attributes_to_find:
            found_element = self._find_simple_attribute(element_to_find)
            attributes_found.update(found_element)
        return attributes_found

    def find_first_page_attributes(self):
        attributes_found = self.find_attributes_from_list(self.first_page_simple_element_list)
        attributes_found['Antyviruses'] = self._find_antyviruses_info()
        return attributes_found

    # w przypadku prostych atrybutów zawsze szukamy następnego elementu typu Content
    def _find_simple_attribute(self, element_to_find):
        elements_found = []
        for i, content in enumerate(self.content_list):
            if element_to_find in content.content:
                elements_found.append(self.content_list[i+1].content)
        if len(elements_found) == 0:
            return {element_to_find: "Element not found"}
        elif len(elements_found) == 1:
            return {element_to_find: elements_found[0]}
        else:
            logging.info("Found more than one element for " + element_to_find + ", which are " +
                         str(elements_found) + ". Arbitrally picked second element: " + elements_found[1])
            return {element_to_find: elements_found[1]}

    def _find_antyviruses_info(self):
        antyviruses_found = {}
        antyviruses_found = self._find_red_antyviruses_info(antyviruses_found)
        antyviruses_found = self._find_green_antyviruses_info(antyviruses_found)
        return antyviruses_found

    def _find_green_antyviruses_info(self, antyviruses_found):
        for index in self._next_antyvirus({'class': 'ltr text-green'}):
            antyvirus = {self.element_list[index - 2].content: {
                "Result": self.element_list[index + 1].attributes['title'],
                "Update": self.element_list[index + 5].content}
            }
            antyviruses_found.update(antyvirus)
        return antyviruses_found

    def _find_red_antyviruses_info(self, antyviruses_found):
        for index in self._next_antyvirus({'class': 'ltr text-red'}):
            antyvirus = {self.element_list[index - 2].content: {
                "Result": self.element_list[index + 1].content,
                "Update": self.element_list[index + 4].content}
            }
            antyviruses_found.update(antyvirus)
        return antyviruses_found

    def _next_antyvirus(self, attributes):
        antyvirusTag = Tag(tagname='td', attributes=attributes)
        for i, element in enumerate(self.element_list):
            if antyvirusTag == element:
                yield i
        return None

    def is_content_present(self, string_searched_one, string_searched_two):
        content_found = [content for content in self.content_list if
                         string_searched_one in content.content or string_searched_two in content.content]
        return len(content_found) > 0
