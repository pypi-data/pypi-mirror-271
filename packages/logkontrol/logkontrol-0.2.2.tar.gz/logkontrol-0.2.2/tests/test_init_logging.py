# tests/test_init_logging.py

import os
import unittest
from unittest.mock import patch
from logkontrol import logkontrol


class TestInitLogging(unittest.TestCase):
    def setUp(self):
        self.log_konfig = logkontrol.LogKonfig()
        self.default_config_path = "logging_config.yaml"
        self.default_log_directory = "logs"
        self.custom_config_path = "custom_config.yaml"
        self.custom_log_directory = "custom_logs"

    def tearDown(self):
        # Clean up generated files and directories after each test
        if os.path.exists(self.default_config_path):
            os.remove(self.default_config_path)
        if os.path.exists(self.default_log_directory):
            for file in os.listdir(self.default_log_directory):
                os.remove(os.path.join(self.default_log_directory, file))
            os.rmdir(self.default_log_directory)
        if os.path.exists(self.custom_config_path):
            os.remove(self.custom_config_path)
        if os.path.exists(self.custom_log_directory):
            for file in os.listdir(self.custom_log_directory):
                os.remove(os.path.join(self.custom_log_directory, file))
            os.rmdir(self.custom_log_directory)

    def test_default_config_creation(self):
        # Test case: Configuration file doesn't exist
        self.log_konfig.init_logging()
        self.assertTrue(os.path.exists(self.default_config_path))
        self.assertTrue(os.path.exists(self.default_log_directory))

    @patch.object(logkontrol.LogKonfig, "load_logging_config")
    def test_existing_config_loading(self, mock_load_config):
        # Test case: Configuration file exists
        with open(self.default_config_path, "w") as file:
            file.write("# Existing configuration")
        self.log_konfig.init_logging()
        mock_load_config.assert_called_once_with(self.default_config_path)

    def test_custom_config_path(self):
        # Test case: Custom configuration file path
        self.log_konfig.init_logging(config_file_path=self.custom_config_path)
        self.assertTrue(os.path.exists(self.custom_config_path))

    def test_custom_log_directory(self):
        # Test case: Custom log directory
        self.log_konfig.init_logging(log_directory=self.custom_log_directory)
        self.assertTrue(os.path.exists(self.custom_log_directory))

    @patch("builtins.open", side_effect=IOError("Failed to open file"))
    def test_invalid_config_file(self, mock_open):
        # Test case: Invalid configuration file
        with self.assertRaises(IOError):
            self.log_konfig.init_logging()
