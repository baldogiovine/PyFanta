"""Client module."""

import json
from pathlib import Path
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
    url = f"http://127.0.0.1:8000/v1/players-links/{year}"
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
    # TODO: some code to startup and close the api
    data_folder_path: Path = Path("data")
    if not data_folder_path.exists():
        data_folder_path.mkdir(parents=True, exist_ok=True)

    YEAR = "2024-25"
    players_links_json: Path = Path(f"data/players_links_{YEAR}.json")

    if not players_links_json.is_file():
        data: Union[Dict[str, List[Dict[str, str]]], None] = get_players_links(
            year=YEAR
        )
        if data:
            with players_links_json.open(mode="w", encoding="utf-8") as file:
                json.dump(data, file, indent=4)
        else:
            print("Failed to retrieve data.")

    # TODO: get_macth_stats with tdqm()
