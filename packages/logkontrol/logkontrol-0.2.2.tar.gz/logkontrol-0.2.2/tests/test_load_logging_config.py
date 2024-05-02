# tests/test_load_logging_config.py

import os
import unittest
from unittest.mock import patch, mock_open
from logkontrol import logkontrol
import yaml


class TestLoadLoggingConfig(unittest.TestCase):
    def setUp(self):
        self.log_konfig = logkontrol.LogKonfig()
        self.valid_config_path = "valid_config.yaml"
        self.invalid_config_path = "invalid_config.yaml"
        self.nonexistent_config_path = "nonexistent_config.yaml"

    def tearDown(self):
        # Clean up generated files after each test
        if os.path.exists(self.valid_config_path):
            os.remove(self.valid_config_path)
        if os.path.exists(self.invalid_config_path):
            os.remove(self.invalid_config_path)

    def test_valid_yaml_config(self):
        # Test case: Valid YAML configuration file
        valid_config = {
            "log_file_paths": {"general": "logs/general.log"},
            "log_format": "[{timestamp}] [{level}] {message}",
            "timestamp_format": "%Y-%m-%d %H:%M:%S",
            "log_level": "INFO",
            "console_output": True,
        }
        with patch("builtins.open", mock_open(read_data=yaml.dump(valid_config))):
            loaded_config = self.log_konfig.load_logging_config(self.valid_config_path)
        self.log_konfig.set_logging_config(loaded_config)
        self.assertEqual(loaded_config, valid_config)

    def test_invalid_yaml_config(self):
        # Test case: Invalid YAML configuration file
        invalid_yaml = "invalid: yaml: format"
        with patch("builtins.open", mock_open(read_data=invalid_yaml)):
            with self.assertRaises(yaml.YAMLError):
                self.log_konfig.load_logging_config(self.invalid_config_path)

    def test_nonexistent_config_file(self):
        # Test case: Non-existent configuration file
        with self.assertRaises(FileNotFoundError):
            self.log_konfig.load_logging_config(self.nonexistent_config_path)
