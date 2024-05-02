# tests/test_truncate_string.py

import unittest
from logkontrol.logkontrol import truncate_string


class TestTruncateString(unittest.TestCase):
    def test_string_within_max_length(self):
        value = "Hello, world!"
        max_length = 20
        truncated_string = truncate_string(value, max_length)
        self.assertEqual(truncated_string, value)

    def test_string_exceeds_max_length(self):
        value = "This is a long string that exceeds the maximum length."
        max_length = 20
        truncated_string = truncate_string(value, max_length)
        self.assertEqual(truncated_string, "This is a long strin...")

    def test_non_string_value(self):
        value = 12345
        max_length = 10
        truncated_string = truncate_string(value, max_length)
        self.assertEqual(truncated_string, "12345")
