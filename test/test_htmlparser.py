from unittest import TestCase

from server.fileservice import Fileservice
from htmlparser import is_not_found_on_vt


class TestHtmlParser(TestCase):
    def test_is_not_found_on_vt(self):
        with Fileservice.File("not_found_on_vt") as file:
            file_content = file.read()

        bool = is_not_found_on_vt(file_content)
        self.assertTrue(bool)

    def test_is_found_on_vt(self):
        with Fileservice.File("found") as file:
            file_content = file.read()

        bool = is_not_found_on_vt(file_content)
        self.assertFalse(bool)
