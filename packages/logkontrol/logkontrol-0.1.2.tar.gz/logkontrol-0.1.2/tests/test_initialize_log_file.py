# tests/test_initialize_log_file.py

import os
import unittest
from unittest.mock import patch, mock_open
from logkontrol.logkontrol import initialize_log_file


class TestInitializeLogFile(unittest.TestCase):
    def setUp(self):
        self.log_file_key = "test_log"
        self.log_file_path = "test_log.log"

    def tearDown(self):
        if os.path.exists(self.log_file_path):
            os.remove(self.log_file_path)

    @patch(
        "logkontrol.logkontrol.logging_config",
        {"log_file_paths": {"test_log": "test_log.log"}},
    )
    def test_initialize_log_file(self):
        initialize_log_file(self.log_file_key)
        self.assertTrue(os.path.exists(self.log_file_path))
        with open(self.log_file_path, "r") as log_file:
            log_content = log_file.read()
        self.assertEqual(log_content, "Log File Initialized\n\n")

    @patch(
        "logkontrol.logkontrol.logging_config",
        {"log_file_paths": {"test_log": "test_log.log"}},
    )
    def test_initialize_existing_log_file(self):
        with open(self.log_file_path, "w") as log_file:
            log_file.write("Existing log content\n")
        initialize_log_file(self.log_file_key)
        with open(self.log_file_path, "r") as log_file:
            log_content = log_file.read()
        self.assertEqual(log_content, "Existing log content\n")

    @patch(
        "logkontrol.logkontrol.logging_config",
        {"log_file_paths": {"test_log": "test_log.log"}},
    )
    def test_initialize_log_file_without_log_file_key(self):
        initialize_log_file(None)
        self.assertTrue(os.path.exists(self.log_file_path))
        with open(self.log_file_path, "r") as log_file:
            log_content = log_file.read()
        self.assertEqual(log_content, "Log File Initialized\n\n")

    @patch("logkontrol.logkontrol.logging_config", None)
    def test_initialize_log_file_without_logging_config(self):
        with patch("builtins.print") as mock_print:
            initialize_log_file(self.log_file_key)
            mock_print.assert_called_with(
                "Logging configuration is not initialized. Please call init_logging() first."
            )
