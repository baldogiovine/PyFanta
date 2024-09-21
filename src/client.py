"""Client module."""

import json
from typing import Dict, List, Union

import requests
from requests import Response


def get_players_links(year: str) -> Union[Dict[str, List[Dict[str, str]]], None]:
    """Gets players' names and links.

    Parameters
    ----------
    year : str
        The year for which player links are to be fetched, e.g., "2023-24", "2022-23".

    Returns:
    -------
    Union[Dict[str, List[Dict[str, str]]], None]
        A dictionary with a key "data" containing a list of players' names and links.

        Otherwise, None.
    """
    url = f"http://127.0.0.1:8000/players-links/{year}"
    try:
        response: Response = requests.get(
            url,
            timeout=15,
            proxies={"http": "", "https": ""},
        )
        response.raise_for_status()
        data: Dict[str, List[Dict[str, str]]] = response.json()
        assert isinstance(data, Dict)
        return data
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None


if __name__ == "__main__":
    YEAR = "2023-24"
    data: Union[Dict[str, List[Dict[str, str]]], None] = get_players_links(year=YEAR)
    if data:
        filename = f"data/players_links_{YEAR}.json"
        with open(filename, "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, indent=4)
            print(f"data have been saved at {filename}")
    else:
        print("Failed to retrieve data.")
