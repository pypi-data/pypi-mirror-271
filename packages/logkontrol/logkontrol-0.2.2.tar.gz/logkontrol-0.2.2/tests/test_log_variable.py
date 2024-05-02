# tests/test_log_variable.py

import os
import unittest
from unittest.mock import patch
from logkontrol.logkontrol import LogKonfig, log_variable, truncate_string


class TestLogVariable(unittest.TestCase):
    def setUp(self):
        self.log_konfig = LogKonfig()
        self.log_konfig.set_logging_config(
            {"log_file_paths": {"test_log": "test_log.log"}}
        )
        self.log_file_key = "test_log"
        self.log_file_path = "test_log.log"
        self.variable_name = "test_variable"
        self.variable_value = "test_value"
        self.log_level = "DEBUG"

    def tearDown(self):
        if os.path.exists(self.log_file_path):
            os.remove(self.log_file_path)

    def test_log_variable(self):
        log_variable(self.log_file_key, self.variable_name, self.variable_value)
        with open(self.log_file_path, "r") as log_file:
            log_content = log_file.read()
        self.assertIn(f"{self.variable_name}: {self.variable_value}", log_content)

    def test_log_variable_with_truncated_level(self):
        long_variable_value = (
            "This is a very long variable value that will be truncated." * 100
        )
        log_variable(
            self.log_file_key,
            self.variable_name,
            long_variable_value,
            log_level="TRUNCATED",
        )
        with open(self.log_file_path, "r") as log_file:
            log_content = log_file.read()
        self.assertIn(
            f"{self.variable_name}: {truncate_string(long_variable_value)}", log_content
        )

    def test_log_variable_without_log_file_key(self):
        log_variable(None, self.variable_name, self.variable_value)
        self.assertTrue(os.path.exists(self.log_file_path))
        with open(self.log_file_path, "r") as log_file:
            log_content = log_file.read()
        self.assertIn(f"{self.variable_name}: {self.variable_value}", log_content)

    def test_log_variable_without_logging_config(self):
        self.log_konfig.set_logging_config(None)  # type: ignore
        with patch("builtins.print") as mock_print:
            log_variable(self.log_file_key, self.variable_name, self.variable_value)
            mock_print.assert_called_with(
                "Logging configuration is not initialized. Please call init_logging() first."
            )
