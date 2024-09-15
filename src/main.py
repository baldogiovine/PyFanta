"""Main module.

This module, together with main_constants.py is temporarly used to test
if code works properly.
"""

import json

import requests

from src.main_constants import MainConstants


def get_links():
    """Main function."""
    response: requests.Response = requests.get(
        MainConstants.get_players_link_endpoint,
        timeout=10,
        proxies={"http": None, "https": None},
    )
    response.raise_for_status()

    data = response.json()
    with open("data/player_links.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

    print("Fetched Player Links")


if __name__ == "__main__":
    get_links()
