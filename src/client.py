"""Client module."""

import json
import time
from pathlib import Path
from random import randint
from typing import Dict, List, Union

import requests
from requests import Response
from tqdm import tqdm


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


def get_matches_stats(
    player_link: Dict[str, str],
) -> Dict[str, List[Union[int, float, str, None]]]:
    """Get's information about a player performance in a match.

    Parameters
    ----------
    player_link : Dict[str, str]
        Dictionary following the structure:
        - name: str
        - link: str

    player_link can be obtained from the `get_players_links` endpoint.

    Returns:
    -------
    Dict[str, List[Union[int, float, str, None]]]
        Information about a player performance in a match.
    """
    url = "http://127.0.0.1:8000/v1/matches-stats"
    try:
        response: Response = requests.post(
            url,
            json=player_link,  # .json(),
            timeout=15,
            proxies={"http": "", "https": ""},
        )
        response.raise_for_status()
        data: Dict[str, List[Union[int, float, str, None]]] = response.json()
        assert isinstance(data, Dict)
        return data
    except requests.exceptions.HTTPError as e:
        print(f"An error occurred: {e}")
        print(f"Response content: {response.content.decode()}")
        return {}
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return {}


def random_sleep() -> None:
    """Sets a random sleep up to a maximum of 3 seconds."""
    sleepy_number = randint(0, 10)
    if sleepy_number in [3, 5, 7]:
        time.sleep(randint(0, 300) / 100)


if __name__ == "__main__":
    # TODO: some code to startup and close the api
    data_folder_path: Path = Path("data")
    if not data_folder_path.exists():
        data_folder_path.mkdir(parents=True, exist_ok=True)

    # Get players's links
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

    with players_links_json.open(mode="r", encoding="utf-8") as file:
        players_links = json.load(file)

    # Get matches stats
    matches_data_json = Path(f"data/matches_data_{YEAR}.json")
    if not matches_data_json.is_file():
        data_list: List[Dict[str, List[Union[int, float, str, None]]]] = []
        with tqdm(
            total=len(players_links.get("data")),
            desc="Scraping players",
            unit="player",
        ) as pbar:
            for player_link in players_links.get("data"):
                player_name: str = player_link.get("name")
                assert isinstance(player_name, str)
                pbar.set_description(f"Scraping {player_name}")

                match_data: Dict[str, List[Union[int, float, str, None]]] = (
                    get_matches_stats(player_link=player_link)
                )
                assert isinstance(match_data, Dict)
                data_list.append(match_data)

                random_sleep()
                pbar.update(1)

        matches_data: Dict[str, List[Dict[str, List[Union[int, float, str, None]]]]] = {
            "data": data_list
        }

        with matches_data_json.open(mode="w", encoding="utf-8") as file:
            json.dump(matches_data, file, indent=4)
