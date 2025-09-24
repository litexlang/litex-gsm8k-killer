"""http_utils.py

HTTP utility functions for interacting with the Litex API.
"""

import requests
import sys
import os

# Add the project root to the Python path to enable imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.config_utils import get_info


def get_example_list(length: int = 10) -> list[dict[str, str]]:
    """
    Fetch a list of example tasks from the API.

    :param length: Number of examples to fetch (default: 10)
    :return: List of dictionaries containing example tasks
    """
    user_info = get_info("user_info")
    collaboration_info = get_info("collaboration_info")
    url = f"https://litexlang.com/api/task/like?keyWord=&collaborationId={collaboration_info['id']}&progress=Solved&solver=All&sort=Most+Reward&requestUsername={user_info['username']}&pageNum=0&pageSize={length}"
    resp = requests.get(url).json()
    return resp["data"]["list"]


def get_task_list(length: int = 100) -> list[dict[str, str]]:
    """
    Fetch a list of tasks from the API.

    :param length: Number of tasks to fetch (default: 100)
    :return: List of dictionaries containing tasks
    """
    user_info = get_info("user_info")
    collaboration_info = get_info("collaboration_info")
    url = f"https://litexlang.com/api/task/like?keyWord=&collaborationId={collaboration_info['id']}&progress=All&solver=All&sort=Most+Reward&requestUsername={user_info['username']}&pageNum=0&pageSize={length}"
    resp = requests.get(url).json()
    return resp["data"]["list"]
