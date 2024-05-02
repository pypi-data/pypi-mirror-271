# tests/test_log_function_call.py

import os
import unittest
from unittest.mock import patch
from logkontrol.logkontrol import LogKonfig, log_function_call, truncate_string


class TestLogFunctionCall(unittest.TestCase):
    def setUp(self):
        self.log_konfig = LogKonfig()
        self.log_konfig.set_logging_config(
            {"log_file_paths": {"test_log": "test_log.log"}}
        )
        self.log_file_key = "test_log"
        self.log_file_path = "test_log.log"
        self.function_name = "test_function"
        self.log_level = "DEBUG"
        self.kwargs = {"arg1": "value1", "arg2": 123}

    def tearDown(self):
        if os.path.exists(self.log_file_path):
            os.remove(self.log_file_path)

    def test_log_function_call(self):
        log_function_call(self.log_file_key, self.function_name, **self.kwargs)
        with open(self.log_file_path, "r") as log_file:
            log_content = log_file.read()
        self.assertIn(f"Function Call: {self.function_name}()", log_content)
        for arg_name, arg_value in self.kwargs.items():
            self.assertIn(f"  {arg_name}: {arg_value}", log_content)

    def test_log_function_call_with_truncated_level(self):
        long_arg_value = "This is a very long argument value that will be truncated."
        kwargs = {"long_arg": long_arg_value}
        log_function_call(
            self.log_file_key, self.function_name, log_level="TRUNCATED", **kwargs
        )
        with open(self.log_file_path, "r") as log_file:
            log_content = log_file.read()
        self.assertIn(f"Function Call: {self.function_name}()", log_content)
        self.assertIn(f"  long_arg: {truncate_string(long_arg_value)}", log_content)

    def test_log_function_call_without_log_file_key(self):
        log_function_call(None, self.function_name, **self.kwargs)
        self.assertTrue(os.path.exists(self.log_file_path))
        with open(self.log_file_path, "r") as log_file:
            log_content = log_file.read()
        self.assertIn(f"Function Call: {self.function_name}()", log_content)

    def test_log_function_call_without_logging_config(self):
        self.log_konfig.set_logging_config(None)  # type: ignore
        with patch("builtins.print") as mock_print:
            log_function_call(self.log_file_key, self.function_name, **self.kwargs)
            mock_print.assert_called_with(
                "Logging configuration is not initialized. Please call init_logging() first."
            )
