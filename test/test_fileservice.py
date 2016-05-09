import os
import unittest
from server import App
from server.fileservice import read_from_file, write_to_file, Fileserver, NoSuchFile


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
            read_from_file(test_sha265)

    def test_read_write(self):
        test_string = "Omijając kwieciste ostrowy burzanu"
        test_sha256 = "1234"
        write_to_file(test_sha256,test_string)
        file_content = read_from_file(test_sha256)
        self.assertEqual(file_content, test_string)


