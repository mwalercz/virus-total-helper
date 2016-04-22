from unittest import TestCase

from app.parser import Parser, Tag


class TestParser(TestCase):
    def setUp(self):
        self.parser = Parser()

    def test_short_div(self):
        data = '''
            <div id="cookies-disabled-alert" class="alert center hide"
            style="margin: 55px auto 0; width: 600px;">
            '''
        expected_element_list = [Tag(tagname="div", attributes={'id': 'cookies-disabled-alert',
                                                                'class': 'alert center hide',
                                                                'style': 'margin: 55px auto 0; width: 600px;'})]
        real_element_list = self.parser.parse(data)
        self.assertEqual(real_element_list[0].tagname,
                         expected_element_list[0].tagname)
        self.assertEqual(real_element_list[0].attributes,
                         expected_element_list[0].attributes)

    def test_alert(self):
        data = '''
            alert("App</SCRIPT>"BZZ)
            '''

        real_element_list = self.parser.parse(data)

    def test_script(self):
        data = '''
            <html>
            <script type="text/javascript">
            var collapseBasicInfo  true;
            var mustRefresh  false;
            function load(tab, url) {
              $('#' + tab + '-list').stream({
                url: url,
                page: 1,
                show: {
                  waiting: '#' + tab + '-wait',
                  empty: '#no-' + tab,
                  more: '#btn-more-' + tab,
                  error: '#' + tab + '-error'
                }
              }).stream('start');
            }

            </script>
            </html>
            '''
        real_element_list = self.parser.parse(data)
        print(real_element_list)

