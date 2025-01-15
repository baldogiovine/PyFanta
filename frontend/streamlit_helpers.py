"""Module to define front-end actions related to the matches_stats dataframe."""

import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Union

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
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


def make_radar_plot(
    data: pd.DataFrame,
    players: list[str],
    categories: List[str],
) -> None:
    """Make a radar plot comparing the given players.

    Parameters
    ----------
    data : pd.DataFrame
        DataFrame containing the data to be plotted.
    players : list[str]
        List of player names to be compared.
    categories : List[str]
        List of categories to be plotted.

    Returns:
    -------
    None
    """
    fig = go.Figure()
    max_values: List[int] = []

    for player in players:
        player_data: List[float] = (
            data.query(f"name == '{player}'")[categories].iloc[0].tolist()
        )
        max_value: int = int(round(max(player_data), 0)) + 1
        max_values.append(max_value)

        add_radar_plot_trace(
            fig=fig,
            player_data=player_data,
            categories=categories,
            player=player,
        )

    size: int = max(max_values)

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, size],
                tickfont=dict(
                    color="black",
                    size=12,
                ),
            )
        ),
        showlegend=True,
    )

    st.plotly_chart(fig)


# FIXME: fix "'" problem, with names like "n'Dicka"
def add_radar_plot_trace(
    fig: go.Figure,
    player_data: List[float],
    categories: List[str],
    player: str,
) -> go.Figure:
    """Add a radar plot trace for a player to the given figure.

    Parameters
    ----------
    fig : go.Figure
        The figure to which the radar plot trace will be added.
    player_data : List[float]
        A list of data points representing the player's statistics.
    categories : List[str]
        A list of category names corresponding to the player's data points.
    player : str
        The name of the player being plotted.

    Returns:
    -------
    go.Figure
        The figure with the added radar plot trace for the player.
    """
    fig.add_trace(
        go.Scatterpolar(
            r=player_data,
            theta=categories,
            fill="toself",
            name=player,
        )
    )


def make_donut_plot(
    data: pd.DataFrame,
    player: str,
    categories: List[str],
) -> go.Figure:
    """Make a donut plot comparing the given categories for the given player.

    Parameters
    ----------
    data : pd.DataFrame
        DataFrame containing the data to be plotted.
    player : str
        Name of the player to be compared.
    categories : List[str]
        List of categories to be plotted.

    Returns:
    -------
    go.Figure
        The created figure with the donut plot.
    """
    values = data.query(f"name == '{player}'")[categories].iloc[0].tolist()

    fig = go.Figure(
        data=[
            go.Pie(
                labels=categories,
                values=values,
                hole=0.3,
            )
        ]
    )
    fig.update_traces(
        textposition="inside",
        textinfo="percent+label",
    )

    st.plotly_chart(fig)


def make_gauge_plot(
    current_value: Union[int, float],
    max_value: Union[int, float],
    title: str,
) -> go.Figure:
    """Make a gauge plot to compare the given current value with the given max value.

    Parameters
    ----------
    current_value : Union[int, float]
        The current value to be compared.
    max_value : Union[int, float]
        The maximum value to be compared.
    title : str
        The title of the plot.

    Returns:
    -------
    go.Figure
        The created figure with the gauge plot.
    """
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=current_value,
            gauge={
                "axis": {"range": [0, max_value]},
            },
            domain={"x": [0, 1], "y": [0, 1]},
            title={"text": title},
        )
    )

    st.plotly_chart(fig)


def make_bar_plot(
    data: pd.DataFrame,
    player: str,
    x: Union[str, None] = None,
    y: Union[str, None] = None,
) -> go.Figure:
    """Make a bar plot to compare the given player with the given data.

    Parameters
    ----------
    data : pd.DataFrame
        DataFrame containing the data to be plotted.
    player : str
        Player to be plotted.
    x : Union[str, None]
        The column to be used as the x-axis. If None, the index of data is used.
    y : Union[str, None]
        The column to be used as the y-axis. If None, all columns of data are used.

    Returns:
    -------
    go.Figure
        The created figure with the bar plot.
    """
    fig = px.bar(data.query(f"name == '{player}'"), x=x, y=y)

    st.plotly_chart(fig)
