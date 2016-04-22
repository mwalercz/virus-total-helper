from unittest import TestCase


class TestDefault(TestCase):
    def test_def(self):
        a = 1
        b = 1
        self.assertEqual(a, b)


