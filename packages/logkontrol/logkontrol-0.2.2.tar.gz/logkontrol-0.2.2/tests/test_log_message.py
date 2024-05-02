# tests/test_log_message.py

import os
import unittest
from unittest.mock import patch
from logkontrol.logkontrol import LogKonfig, log_message, truncate_string


class TestLogMessage(unittest.TestCase):
    def setUp(self):
        self.log_konfig = LogKonfig()
        self.log_konfig.set_logging_config(
            {"log_file_paths": {"test_log": "test_log.log"}}
        )
        self.log_file_key = "test_log"
        self.log_file_path = "test_log.log"
        self.message = "Test log message"
        self.variables = {"var1": "value1", "var2": "value2"}
        self.log_level = "DEBUG"

    def tearDown(self):
        if os.path.exists(self.log_file_path):
            os.remove(self.log_file_path)

    def test_log_message_to_file(self):
        log_message(self.log_file_key, self.message)
        with open(self.log_file_path, "r") as log_file:
            log_content = log_file.read()
        self.assertIn(self.message, log_content)

    def test_log_message_with_variables(self):
        log_message(self.log_file_key, variables=self.variables)
        with open(self.log_file_path, "r") as log_file:
            log_content = log_file.read()
        for variable_name, variable_value in self.variables.items():
            self.assertIn(f"{variable_name}: {variable_value}", log_content)

    def test_log_message_with_truncated_level(self):
        long_message = "This is a very long message that will be truncated." * 100
        log_message(self.log_file_key, long_message, log_level="TRUNCATED")
        with open(self.log_file_path, "r") as log_file:
            log_content = log_file.read()
        self.assertIn(truncate_string(long_message), log_content)

    def test_log_message_without_log_file_key(self):
        log_message(None, self.message)
        self.assertTrue(os.path.exists(self.log_file_path))
        with open(self.log_file_path, "r") as log_file:
            log_content = log_file.read()
        self.assertIn(self.message, log_content)

    def test_log_message_without_logging_config(self):
        self.log_konfig.set_logging_config(None)  # type: ignore
        with patch("builtins.print") as mock_print:
            log_message(self.log_file_key, self.message)
            mock_print.assert_called_with(
                "Logging configuration is not initialized. Please call init_logging() first."
            )
