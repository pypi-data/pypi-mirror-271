# This file by voidfemme is released under CC0 1.0 Universal (CC0 1.0) Public Domain Dedication.
# https://creativecommons.org/publicdomain/zero/1.0

import os
import json
from pathlib import Path
from typing import Any
import yaml
from datetime import datetime


logging_config = None


def init_logging(config_file_path: str | None = None, log_directory: str = "logs"):
    """
    Initializes the logging configuration.

    Args:
        config_file_path (str | None, optional): The path to the logging configuration file.
            If not provided, defaults to "logging_config.yaml".
        log_directory (str, optional): The directory where log files will be stored.
            Defaults to "logs".
    """
    global logging_config

    if config_file_path is None:
        config_file_path = "logging_config.yaml"

    if not os.path.exists(config_file_path):
        # Create the log directory if it doesn't exist
        os.makedirs(log_directory, exist_ok=True)

        # Generate a default YAML configuration
        default_config = {
            "log_file_paths": {
                "general": f"{log_directory}/general.log",
            },
            "log_format": "[{timestamp}] [{level}] {message}",
            "timestamp_format": "%Y-%m-%d %H:%M:%S",
            "log_level": "INFO",
            "console_output": True,
        }

        # Write the default configuration to the YAML file
        with open(config_file_path, "w") as config_file:
            yaml.dump(default_config, config_file)

    # Load the logging configuration from the YAML file
    logging_config = load_logging_config(config_file_path)

    # Initialize the log files
    for log_file_key in logging_config["log_file_paths"]:
        initialize_log_file(log_file_key)


def load_logging_config(config_file_path: str):
    """
    Loads the logging configuration from a YAML file.

    Args:
        config_file_path (str): The path to the logging configuration file.

    Returns:
        dict: The loaded logging configuration.
    """
    config_path = Path(config_file_path)
    with open(config_path, "r") as config_file:
        config = yaml.safe_load(config_file)
    return config


def truncate_string(value: Any, max_length: int = 500):
    """
    Truncates a string to a maximum length and appends "..." if truncated.

    Args:
        value: The value to truncate.
        max_length (int, optional): The maximum length of the truncated string.

    Returns:
        str: The truncated string.
    """
    str_value = str(value)
    if len(str_value) > max_length:
        return str_value[:max_length] + "..."
    return str_value


def log_message(
    log_file_key: str | None,
    message: str | None = None,
    variables: dict | None = None,
    log_level: str = "DEBUG",
):
    """
    Logs a message and/or variable values to a file.

    Args:
        log_file_key (str): The key of the log file path in the logging configuration.
        message (str, optional): The message to log. Defaults to None.
        variables (dict, optional): A dictionary of variables and their values to log.
            Defaults to None.
        log_level (str, optional): The log level of the message. Defaults to "DEBUG".
    """

    if logging_config is None:
        print(
            "Logging configuration is not initialized. Please call init_logging() first."
        )
        return

    # Check if log_file_key is not provided and if only one log path is configured
    if log_file_key is None:
        keys = list(logging_config["log_file_paths"].keys())
        if len(keys) == 1:
            log_file_key = keys[0]
        else:
            print("Multiple log files configured, please specify a log_file_key.")
            return

    log_file_path = logging_config["log_file_paths"][log_file_key]
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] [{log_level}]\n"

    if message:
        if log_level == "TRUNCATED":
            message = truncate_string(message)
        log_entry += f"Message: {message}\n"

    if variables:
        for variable_name, variable_value in variables.items():
            if log_level == "TRUNCATED":
                variable_value = truncate_string(variable_value)
            log_entry += f"{variable_name}: {variable_value}\n"
    log_entry += "\n"

    if logging_config.get("console_output", False):
        print(log_entry)
    else:
        with open(log_file_path, "a") as log_file:
            log_file.write(log_entry)


def log_function_call(
    log_file_key: str | None, function_name: str, log_level: str = "DEBUG", **kwargs
):
    """
    Logs a function call with its arguments.

    Args:
        log_file_key (str): The key of the log file path in the logging configuration.
        function_name (str): The name of the function being called.
        log_level (str, optional): The log level of the function call. Defaults to "DEBUG".
        **kwargs: Keyword arguments representing the function's arguments.
    """
    if logging_config is None:
        print(
            "Logging configuration is not initialized. Please call init_logging() first."
        )
        return

    # Check if log_file_key is not provided and if only one log path is configured
    if log_file_key is None:
        keys = list(logging_config["log_file_paths"].keys())
        if len(keys) == 1:
            log_file_key = keys[0]
        else:
            print("Multiple log files configured, please specify a log_file_key.")
            return

    log_entry = f"Function Call: {function_name}()\n"
    for arg_name, arg_value in kwargs.items():
        if log_level == "TRUNCATED":
            arg_value = truncate_string(arg_value)
        log_entry += f"  {arg_name}: {arg_value}\n"
    log_message(log_file_key, log_entry, log_level=log_level)


def log_variable(
    log_file_key: str | None,
    variable_name: str,
    variable_value: Any,
    log_level: str = "DEBUG",
):
    """
    Logs a variable and its value.

    Args:
        log_file_key (str): The key of the log file path in the logging configuration.
        variable_name (str): The name of the variable.
        variable_value: The value of the variable.
        log_level (str, optional): The log level of the variable. Defaults to "DEBUG".
    """
    if logging_config is None:
        print(
            "Logging configuration is not initialized. Please call init_logging() first."
        )
        return

    # Check if log_file_key is not provided and if only one log path is configured
    if log_file_key is None:
        keys = list(logging_config["log_file_paths"].keys())
        if len(keys) == 1:
            log_file_key = keys[0]
        else:
            print("Multiple log files configured, please specify a log_file_key.")
            return

    if log_level == "TRUNCATED":
        variable_value = truncate_string(variable_value)
    log_message(
        log_file_key, variables={variable_name: variable_value}, log_level=log_level
    )


def initialize_log_file(log_file_key: str | None):
    """
    Initializes the log file by creating it if it doesn't exist and adding a header.

    Args:
        log_file_key (str): The key of the log file path in the logging configuration.
    """
    if logging_config is None:
        print(
            "Logging configuration is not initialized. Please call init_logging() first."
        )
        return

    # Check if log_file_key is not provided and if only one log path is configured
    if log_file_key is None:
        keys = list(logging_config["log_file_paths"].keys())
        if len(keys) == 1:
            log_file_key = keys[0]
        else:
            print("Multiple log files configured, please specify a log_file_key.")
            return

    log_file_path = logging_config["log_file_paths"][log_file_key]
    if not os.path.exists(log_file_path):
        with open(log_file_path, "w") as log_file:
            log_file.write("Log File Initialized\n\n")


def log_json_content(
    log_file_key: str | None, json_content: dict | list[dict], log_level: str = "DEBUG"
):
    """
    Logs the content of a JSON object or a list of JSON objects in a pretty-printed format.

    Args:
        log_file_key (str): The key of the log file path in the logging configuration.
        json_content (dict | list[dict]): The JSON object or list of JSON objects to log.
        log_level (str, optional): The log level of the JSON content. Defaults to "DEBUG".
    """
    if logging_config is None:
        print(
            "Logging configuration is not initialized. Please call init_logging() first."
        )
        return

    # Check if log_file_key is not provided and if only one log path is configured
    if log_file_key is None:
        keys = list(logging_config["log_file_paths"].keys())
        if len(keys) == 1:
            log_file_key = keys[0]
        else:
            print("Multiple log files configured, please specify a log_file_key.")
            return

    log_file_path = logging_config["log_file_paths"][log_file_key]
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] [{log_level}]\n"
    log_entry += "JSON Content:\n"

    if isinstance(json_content, dict):
        log_entry += json.dumps(json_content, indent=2)
    elif isinstance(json_content, list):
        for item in json_content:
            if isinstance(item, dict):
                log_entry += json.dumps(item, indent=2)
                log_entry += "\n"
            else:
                log_entry += f"{item}\n"
    else:
        log_entry += f"{json_content}\n"

    log_entry += "\n"

    with open(log_file_path, "a") as log_file:
        log_file.write(log_entry)


def load_logging_konfig(konfig_file_path: str):
    """
    Easter Egg function! Loads the logging configuration from a YAML file.

    Args:
        konfig_file_path (str): The path to the logging configuration file.

    Returns:
        dict: The loaded logging configuration.
    """
    return load_logging_config(konfig_file_path)


def log_funktion_kall(
    log_file_key: str, funktion_name: str, log_level: str = "DEBUG", **kwargs
):
    """
    Easter Egg function! Logs a function call with its arguments.

    Args:
        log_file_key (str): The key of the log file path in the logging configuration.
        funktion_name (str): The name of the function being called.
        log_level (str, optional): The log level of the function call. Defaults to "DEBUG".
        **kwargs: Keyword arguments representing the function's arguments.
    """
    return log_function_call(log_file_key, funktion_name, log_level, **kwargs)


def log_json_kontent(
    log_file_key: str, json_kontent: dict | list[dict], log_level: str = "DEBUG"
):
    """
    Easter Egg function! Logs the content of a JSON object or a list of JSON objects in a pretty-printed format.

    Args:
        log_file_key (str): The key of the log file path in the logging configuration.
        json_kontent (dict | list[dict]): The JSON object or list of JSON objects to log.
        log_level (str, optional): The log level of the JSON content. Defaults to "DEBUG".
    """
    return log_json_content(log_file_key, json_kontent, log_level)
