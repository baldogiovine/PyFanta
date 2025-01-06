"""Module to define front-end actions related to the matches_stats dataframe."""

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Union

import pandas as pd
from pandas import DataFrame

# my_team: Dict[str, List[str]] = {
#     "goalkeepers": [
#         "Sommer",
#     ],
#     "defenders": [
#         "Bastoni",
#         "Hernandez T.",
#         "Miranda J.",
#         "Rrahmani",
#     ],
#     "midfilders": [
#         "Pulisic",
#         "Saelemaekers",
#         "Strefezza",
#     ],
#     "attackers": [
#         "Lookman",
#         "Gudmundsson A.",
#         "Yildiz",
#     ],
# }


def load_matches_dataframe(path_to_json: Union[str, Path]) -> pd.DataFrame:
    """Read a JSON file and return a DataFrame.

    Parameters
    ----------
    path_to_json : Union[str, Path]
        Path to the JSON file to be read.

    Returns:
    -------
    df : pd.DataFrame
        DataFrame containing the data from the JSON file.
    """
    with open(Path(path_to_json), "r", encoding="utf-8") as file:
        data = json.load(file)
    open_json: List[Any] = []
    for entry in data["data"]:
        if "data" in entry:
            open_json.extend(entry["data"])
    df: DataFrame = pd.DataFrame(open_json)

    return df


def load_players_dataframe(path_to_json: Union[str, Path]) -> pd.DataFrame:
    """Read a JSON file and return a DataFrame.

    Parameters
    ----------
    path_to_json : Union[str, Path]
        Path to the JSON file to be read.

    Returns:
    -------
    df : pd.DataFrame
        DataFrame containing the data from the JSON file.
    """
    with open(path_to_json, "r", encoding="utf-8") as file:
        data = json.load(file)
    open_json: List[Any] = [entry["data"] for entry in data["data"] if "data" in entry]
    df: DataFrame = pd.DataFrame(open_json)

    return df


def download_json(data: Dict[str, Any]) -> bytes:
    """Convert a JSON serializable object to bytes to be downloaded.

    Parameters
    ----------
    data : Dict[str, Any]
        JSON serializable object to be converted to bytes.

    Returns:
    -------
    json_bytes : bytes
        Bytes representation of the input data.
    """
    json_data = json.dumps(data, indent=4)
    json_bytes = json_data.encode("utf-8")

    return json_bytes


def download_json_in_server(data: Dict[str, List[str]], team_name: str) -> None:
    """Save a dictionary as a JSON file on the server.

    Parameters
    ----------
    data : Dict[str, List[str]]
        A dictionary containing team data to be saved in JSON format.

    Notes:
    -----
    The JSON file is saved to the 'data/my_teams' directory with the filename 'my_team.json'.
    If the directory does not exist, it will be created.
    """
    directory = "data/my_teams"
    file_path = os.path.join(directory, f"{team_name}.json")
    os.makedirs(directory, exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def run_python_script(script_path: Union[str, Path]) -> None:
    """Run a Python script and return True if it executes successfully, False otherwise.

    Parameters
    ----------
    script_path : Union[str, Path]
        Path to the Python script to be run.

    Returns:
    -------
    bool
        True if the script runs successfully, False otherwise.
    """
    subprocess.run(
        [f"{sys.executable}", str(script_path)],
        check=True,
        cwd=str(Path(script_path).resolve().parent.parent),
    )


def get_json_file_names(directory: Union[str, Path]) -> List[str]:
    """Get a list of all JSON files in a directory.

    Parameters
    ----------
    directory : Union[str, Path]
        Path to the directory to be searched.

    Returns:
    -------
    List[str]
        List of JSON file names without the '.json' extension.

    Notes:
    -----
    This function does not recursively search directories.
    """
    file_names: List[str] = [
        f[:-5] for f in os.listdir(directory) if f.endswith(".json")
    ]
    return file_names
