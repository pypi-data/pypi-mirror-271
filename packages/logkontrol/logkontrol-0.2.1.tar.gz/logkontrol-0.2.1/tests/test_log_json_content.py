# tests/test_log_json_content.py

import os
import unittest
from unittest.mock import patch, mock_open
from logkontrol.logkontrol import LogKonfig, log_json_content


class TestLogJsonContent(unittest.TestCase):
    def setUp(self):
        self.log_konfig = LogKonfig()
        self.log_konfig.set_logging_config(
            {"log_file_paths": {"test_log": "test_log.log"}}
        )
        self.log_file_key = "test_log"
        self.log_file_path = "test_log.log"
        self.json_object = {"key1": "value1", "key2": {"nested_key": "nested_value"}}
        self.json_list = [{"item1": "value1"}, {"item2": "value2"}]
        self.log_level = "DEBUG"

    def tearDown(self):
        if os.path.exists(self.log_file_path):
            os.remove(self.log_file_path)

    def test_log_json_object(self):
        log_json_content(self.log_file_key, self.json_object)
        with open(self.log_file_path, "r") as log_file:
            log_content = log_file.read()
        self.assertIn("JSON Content:", log_content)
        self.assertIn('"key1": "value1"', log_content)
        self.assertIn('"key2": {', log_content)
        self.assertIn('"nested_key": "nested_value"', log_content)

    def test_log_json_list(self):
        log_json_content(self.log_file_key, self.json_list)
        with open(self.log_file_path, "r") as log_file:
            log_content = log_file.read()
        self.assertIn("JSON Content:", log_content)
        self.assertIn('"item1": "value1"', log_content)
        self.assertIn('"item2": "value2"', log_content)

    def test_log_invalid_json_content(self):
        invalid_json = "invalid_json_content"
        log_json_content(self.log_file_key, invalid_json)  # type: ignore
        with open(self.log_file_path, "r") as log_file:
            log_content = log_file.read()
        self.assertIn("JSON Content:", log_content)
        self.assertIn(invalid_json, log_content)

    def test_log_json_content_without_log_file_key(self):
        log_json_content(None, self.json_object)
        self.assertTrue(os.path.exists(self.log_file_path))
        with open(self.log_file_path, "r") as log_file:
            log_content = log_file.read()
        self.assertIn("JSON Content:", log_content)

    def test_log_json_content_without_logging_config(self):
        self.log_konfig.set_logging_config(None)  # type: ignore
        with patch("builtins.print") as mock_print:
            log_json_content(self.log_file_key, self.json_object)
            mock_print.assert_called_with(
                "Logging configuration is not initialized. Please call init_logging() first."
            )
