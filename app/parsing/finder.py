from app.parsing.parser import Content, Tag


class NoSuchAttribute(Exception):
    pass


class NoMoreAntyviruses(Exception):
    pass


class Finder:
    def __init__(self, element_list):
        self.first_page_simple_element_list = ['SHA256', 'File name', 'Detection ratio', 'Analysis date']
        self.element_list = element_list
        self.content_list = []
        for element in self.element_list:
            if isinstance(element, Content):
                self.content_list.append(element)

    def find_attributes(self, attributes_to_find):
        if len(attributes_to_find) == 0:
            return self._find_first_page_info()
        else:
            return self._find_simple_attributes(attributes_to_find)

    def _find_simple_attributes(self, attributes_to_find):
        attributes_found = {}
        for element_to_find in attributes_to_find:
            found_element = self._find_simple_attribute(element_to_find)
            attributes_found.update(found_element)
        return attributes_found

    def _find_first_page_info(self):
        attributes_found = self._find_simple_attributes(self.first_page_simple_element_list)
        attributes_found['antyviruses'] = self._find_antyviruses_info()
        return attributes_found

    # w przypadku prostych atrybutów zawsze szukamy następnego elementu typu Content
    def _find_simple_attribute(self, element_to_find):
        j = -1
        for i, content in enumerate(self.content_list):
            if element_to_find in content.content:
                j = i + 1
                break
        if j == -1:
            raise NoSuchAttribute
        else:
            return {element_to_find: self.content_list[j].content}

    def _next_antyvirus_tag_index(self):
        antyvirusTag = Tag(tagname='td', attributes={'class': 'ltr text-green'})
        for i, element in enumerate(self.element_list):
            if antyvirusTag == element:
                yield i
        return None

    def _find_antyviruses_info(self):
        antyviruses_found = {}
        for index in self._next_antyvirus_tag_index():
            antyvirus = {self.element_list[index - 2].content:
                             self.element_list[index + 1].attributes['title']}

            antyviruses_found.update(antyvirus)
        return antyviruses_found