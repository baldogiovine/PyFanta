"""Module to define front-end actions related to the matches_stats dataframe."""

import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Union

import pandas as pd
import streamlit as st
from pandas import DataFrame


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
    """Run a Python script using the subprocess module.

    Parameters
    ----------
    script_path : str or Path
        Path to the script to be run.

    Raises:
    ------
    subprocess.CalledProcessError
        If the script returns a non-zero exit code.

    Notes:
    -----
    This function does not capture the output of the script. If you want to capture
    the output, use the `subprocess.run` function directly.
    """
    # TODO: make it show output (tqdm) in streamlit
    try:
        module_path = str(script_path).replace("/", ".").replace(".py", "")
        subprocess.run(
            [sys.executable, "-m", module_path],
            check=True,
            cwd=str(Path(script_path).resolve().parent.parent),
        )
    except subprocess.CalledProcessError as e:
        st.error(f"Error running script: {script_path}\n{e}")
        raise


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


def get_default_options(role: str) -> List[str]:
    """Retrieve default options for a specified role from a loaded team.

    Parameters
    ----------
    role : str
        The role for which to retrieve default options (e.g., "attackers", "defenders").

    Returns:
    -------
    List[str]
        A list of default options (player names) for the given role if available,
        otherwise an empty list.
    """
    if st.session_state.loaded_team and role in st.session_state.loaded_team:
        assert isinstance(st.session_state.loaded_team[role], List)
        return st.session_state.loaded_team[role]  # type: ignore
    return []


def start_fastapi_server() -> subprocess.Popen[bytes]:
    """Start the FastAPI server as a subprocess."""
    try:
        process = subprocess.Popen(
            ["uvicorn", "src.api.main:app", "--host", "127.0.0.1", "--port", "8000"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        time.sleep(7)
        return process
    except Exception as e:
        st.error(f"Failed to start FastAPI server: {e}")
        raise


def stop_fastapi_server(process: subprocess.Popen[bytes]) -> None:
    """Terminate the FastAPI server subprocess."""
    try:
        process.terminate()
        process.wait()
    except Exception as e:
        st.error(f"Failed to stop FastAPI server: {e}")
        raise


def download_data_from_fastapi_api() -> None:
    """Download data from the FastAPI API.

    This function starts the FastAPI server and downloads all available data using the
    `src/download_data.py` script. The function will handle any exceptions that occur
    during the execution of the script and will stop the FastAPI server after the script
    has finished or an exception has occurred.
    """
    fastapi_process = None
    try:
        st.info("Starting FastAPI server...")
        fastapi_process = start_fastapi_server()
        st.success("FastAPI server started successfully!")

        st.info("Downloading data...")
        run_python_script(script_path="src/download_data.py")
        st.success("Data downloaded successfully!")
    except Exception as e:
        st.error(f"An error occurred: {e}")
    finally:
        if fastapi_process:
            st.info("Stopping FastAPI server...")
            stop_fastapi_server(fastapi_process)
            st.success("FastAPI server stopped successfully!")
