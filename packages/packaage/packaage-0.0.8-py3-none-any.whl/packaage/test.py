"""This module is used to test if the code works"""

import unittest

from unittest import TestCase

from nlp import clean_text


class TestCleanText(TestCase):

    def test_with_string(self):
        cleaned = clean_text('Très cool!!!')
        self.assertEqual(
            cleaned,
            'tres cool'
        )

    def test_with_int(self):
        self.assertEqual(
            clean_text(1),
            '1'
        )

    def test_with_none(self):
        self.assertEqual(
            clean_text(None),
            ''
        )


if __name__ == '__main__':
    unittest.main()
