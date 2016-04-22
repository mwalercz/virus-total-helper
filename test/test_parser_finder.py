from unittest import TestCase

from app.parsing.finder import Finder
from app.parsing.parser import Parser


class TestParserFinder(TestCase):
    def setUp(self):
        self.parser = Parser()

    def test_short_div(self):
        data = '''
           <div class="enum">
  <div class="floated-field-key">MIMEType</div>
  <div class="floated-field-value">application/pdf</div>
  <br style="clear:both;"/>
</div>



<div class="enum">
  <div class="floated-field-key">XMPToolkit</div>
  <div class="floated-field-value">XMP toolkit 2.9.1-13, framework 1.6</div>
  <br style="clear:both;"/>
</div>
            '''
        attributes = ["XMPToolkit", "MIMEType"]
        element_list = self.parser.parse(data)
        finder = Finder(element_list)
        real_attributes_found = finder.find(attributes)
        expected_attributes_found = {"MIMEType": "application/pdf", "XMPToolkit": "XMP toolkit 2.9.1-13, framework 1.6"}

        self.assertEqual(real_attributes_found, expected_attributes_found)

