"""
Loads configuration from a JSON file.
"""

import json

def load_config(file_path: str) -> dict:
    """
    Load configuration from a JSON file.

    Args:
        file_path (str): The path to the JSON configuration file.

    Returns:
        dict: The loaded configuration.
    """
    with open(file_path, 'r') as f:
        return json.load(f)
