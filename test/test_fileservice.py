import os
import unittest
from server import App
from server.fileservice import Fileserver, NoSuchFile


class TestFileService(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = App()
        cls.app.initialize()

    @classmethod
    def tearDownClass(cls):
        cls.app.exit_gracefully()

    def test_read_wrong_file(self):
        test_sha265 = "4321"
        path = Fileserver._get_filename(test_sha265)
        if os.path.isfile(path):
            os.remove(path)
        with self.assertRaises(NoSuchFile):
            with Fileserver.File(test_sha265) as file:
                file.read()

    def test_read_write(self):
        test_string = "Omijając kwieciste ostrowy burzanu"
        test_sha256 = "1234"
        with Fileserver.File(test_sha256) as file:
            file.write(test_string)
            file_content = file.read()
        self.assertEqual(file_content, test_string)


