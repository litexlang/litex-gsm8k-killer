"""config_utils.py

Configuration utility functions for loading settings from JSON files.
"""

import json
from pathlib import Path
from typing import Dict, Any


def load_config(config_filename: str = "config.json") -> Dict[str, Any]:
    """
    Load configuration from a JSON file.

    :param config_filename: Name of the configuration file (default: "config.json")
    :return: Dictionary containing configuration data
    :raises FileNotFoundError: If the config file doesn't exist
    :raises json.JSONDecodeError: If the config file contains invalid JSON
    """
    # Get the project root directory (parent of utils folder)
    project_root = Path(__file__).parent.parent
    config_path = project_root / config_filename

    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    try:
        with open(config_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(
            f"Invalid JSON in config file {config_path}: {e.msg}", e.doc, e.pos
        )


def get_info(config_key: str, config_filename: str = "config.json") -> Dict[str, str]:
    """
    Get information from configuration file.

    :param config_key: Key name for the information in config
    :param config_filename: Name of the configuration file (default: "config.json")
    :return: Dictionary containing information
    :raises KeyError: If the information is not found in config
    """
    config = load_config(config_filename)
    if config_key not in config:
        raise KeyError(
            f"User information '{config_key}' not found in configuration file"
        )
    return config[config_key]
