from app.parsing.parser import Content


class NoSuchAttribute:
    pass


class Finder:
    def __init__(self, element_list):
        self.element_list = element_list
        self.content_list = []
        for element in self.element_list:
            if isinstance(element, Content):
                self.content_list.append(element)

    def find(self, attributes_to_find):
        attributes_found = {}
        for element_to_find in attributes_to_find:
            found_element = self._find_one(element_to_find)
            attributes_found.update(found_element)
        return attributes_found

    # w przypadku prostych atrybutów zawsze szukamy następnego elementu typu Content
    def _find_one(self, element_to_find):
        j = -1
        for i, content in enumerate(self.content_list):
            if content.content == element_to_find:
                j = i + 1
                break
        if j == -1:
            raise NoSuchAttribute
        else:
            return {element_to_find: self.content_list[j].content}
