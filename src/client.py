"""Client module."""

import json
import time
from pathlib import Path
from random import randint
from typing import Any, Dict, List, Union

import pandas as pd
import requests
from pandas import DataFrame
from requests import Response
from tqdm import tqdm

from src.api.models import PlayerLink

# FIXME: the functions to connect to three endpoints are basically the same except for
# the endpoint url. Make a single function that can accept different urls or a general
# class where the classes that inherit it pass a different url.

# FIXME: what stated in the previous fixme applies as well in the client code, for
# example when fectching mathces_data and players_summary_data. A common function can
# probably be defined.

# FIXME: when an error occurs, only an empty dictionary - not even containing the name
# of the player - is returned is retruned. a Dictionary following the pydantic model
# structur, but containing information about the error should be returned instead.

# FIXME: find a way to put player_name in the endpoints' urls

# FIXME: change jsons type hints to pydantics correspective response models


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


def get_outfield_player_summary_stats(
    player_link: Dict[str, str],
) -> Dict[str, List[Union[int, float, str, None]]]:
    """Get's information about an outfield player summary stats in a season.

    Outfield players are:
    - attackers
    - midfilders
    - defenders

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
        Information about an outfield player summary stats in a season.
    """
    url = "http://127.0.0.1:8000/v1/player-summary-stats/outfield"
    try:
        response: Response = requests.post(
            url,
            json=player_link,
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


def get_goalkeeper_summary_stats(
    player_link: Dict[str, str],
) -> Dict[str, List[Union[int, float, str, None]]]:
    """Get's information about a goalkeeper summary stats in a season.

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
        Information about a goalkeeper summary stats in a season.
    """
    url = "http://127.0.0.1:8000/v1/player-summary-stats/goalkeper"
    try:
        response: Response = requests.post(
            url,
            json=player_link,
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
    # TODO: add the possibility to expose a different port
    # TODO: check if some type hints can be substituted by PlayerLink

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
            desc="Scraping players mathces information",
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

    # Get outfield players summary stats
    outfield_players_summary_data_json = Path(
        f"data/outfiled_players_summary_stats_data_{YEAR}.json"
    )
    if not outfield_players_summary_data_json.is_file():
        data_list = []
        goalkeepers_links: List[PlayerLink] = []
        with tqdm(
            total=len(players_links.get("data")),
            desc="Scraping outfield players summary stats information",
            unit="player",
        ) as pbar:
            for player_link in players_links.get("data"):
                player_name = player_link.get("name")
                assert isinstance(player_name, str)
                pbar.set_description(f"Scraping {player_name}")

                player_summary_data: Dict[str, List[Union[int, float, str, None]]] = (
                    get_outfield_player_summary_stats(player_link=player_link)
                )
                assert isinstance(player_summary_data, Dict)

                if not player_summary_data:
                    if player_link is not None:
                        goalkeepers_links.append(player_link)
                        print(f"{player_name} added to goalkeepers list.")
                else:
                    data_list.append(player_summary_data)

                random_sleep()
                pbar.update(1)

        players_summary_data: Dict[
            str, List[Dict[str, List[Union[int, float, str, None]]]]
        ] = {"data": data_list}

        with outfield_players_summary_data_json.open(
            mode="w", encoding="utf-8"
        ) as file:
            json.dump(players_summary_data, file, indent=4)

        goalkeepers_links_json: Dict[str, List[PlayerLink]] = {
            "data": goalkeepers_links
        }
        goalkeepers_list_path = Path(f"data/goalkeepers_list_{YEAR}.json")
        with goalkeepers_list_path.open(mode="w", encoding="utf-8") as file:
            json.dump(goalkeepers_links_json, file, indent=4)

    # Get goalkeepers players summary stats
    goalkeepers_summary_data_json = Path(
        f"data/goalkeepers_summary_stats_data_{YEAR}.json"
    )
    if not goalkeepers_summary_data_json.is_file():
        with goalkeepers_list_path.open(mode="r", encoding="utf-8") as file:
            goalkeepers_links_json = json.load(file)
        goalkeepers_links = goalkeepers_links_json.get("data")  # type: ignore
        data_list = []
        with tqdm(
            total=len(goalkeepers_links),
            desc="Scraping goalkeepers summary stats information",
            unit="player",
        ) as pbar:
            for player_link in goalkeepers_links:
                player_name = player_link.get("name")
                assert isinstance(player_name, str)
                pbar.set_description(f"Scraping {player_name}")

                player_summary_data = get_goalkeeper_summary_stats(
                    player_link=player_link
                )
                assert isinstance(player_summary_data, Dict)
                data_list.append(player_summary_data)

                random_sleep()
                pbar.update(1)

        players_summary_data = {"data": data_list}

        with goalkeepers_summary_data_json.open(mode="w", encoding="utf-8") as file:
            json.dump(players_summary_data, file, indent=4)

    # Export json files as Excel files
    json_files: List[Path] = [
        matches_data_json,
        outfield_players_summary_data_json,
        goalkeepers_summary_data_json,
    ]
    for file_path in json_files:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        open_json: List[Any] = [
            entry["data"]
            for entry in data["data"]  # type: ignore
            if "data" in entry
        ]
        df: DataFrame = pd.DataFrame(open_json)
        output_file: Path = file_path.with_suffix(".xlsx")
        df.to_excel(output_file, index=False)
