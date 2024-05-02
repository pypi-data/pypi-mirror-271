# tests/test_initialize_log_file.py

import os
import unittest
from unittest.mock import patch
from logkontrol.logkontrol import LogKonfig


class TestInitializeLogFile(unittest.TestCase):
    def setUp(self):
        self.log_konfig = LogKonfig()
        self.log_file_key = "test_log"
        self.log_file_path = "test_log.log"

    def tearDown(self):
        if os.path.exists(self.log_file_path):
            os.remove(self.log_file_path)

    def test_initialize_log_file_with_log_konfig(self):
        self.log_konfig.set_logging_config(
            {"log_file_paths": {"test_log": "test_log.log"}}
        )
        self.log_konfig.initialize_log_file(self.log_file_key)
        self.assertTrue(os.path.exists(self.log_file_path))
        with open(self.log_file_path, "r") as log_file:
            log_content = log_file.read()
        self.assertEqual(log_content, "Log File Initialized\n\n")

    def test_initialize_existing_log_file_with_log_konfig(self):
        self.log_konfig.set_logging_config(
            {"log_file_paths": {"test_log": "test_log.log"}}
        )
        with open(self.log_file_path, "w") as log_file:
            log_file.write("Existing log content\n")
        self.log_konfig.initialize_log_file(self.log_file_key)
        with open(self.log_file_path, "r") as log_file:
            log_content = log_file.read()
        self.assertEqual(log_content, "Existing log content\n")

    def test_initialize_log_file_without_log_file_key_with_log_konfig(self):
        self.log_konfig.set_logging_config(
            {"log_file_paths": {"test_log": "test_log.log"}}
        )
        self.log_konfig.initialize_log_file(None)
        self.assertTrue(os.path.exists(self.log_file_path))
        with open(self.log_file_path, "r") as log_file:
            log_content = log_file.read()
        self.assertEqual(log_content, "Log File Initialized\n\n")

    def test_initialize_log_file_without_logging_config_with_log_konfig(self):
        self.log_konfig.set_logging_config(None)  # type: ignore
        with self.assertRaises(ValueError) as cm:
            self.log_konfig.initialize_log_file(self.log_file_key)
        self.assertEqual(
            str(cm.exception),
            "Logging configuration is not initialized. Please call init_logging() first",
        )
