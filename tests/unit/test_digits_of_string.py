from unittest import TestCase
from utils.find_digits_in_string import digits_of_string


class TestDigitFinder(TestCase):

    def test_digits_of_string_finder(self):
        result = digits_of_string('01 of test 12 testing 67')
        self.assertEqual(result, '011267')

        result = digits_of_string('121 95')
        self.assertEqual(result, '12195')