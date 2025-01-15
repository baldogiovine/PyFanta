"""Module to design a Strealit page to check team's stats."""

import json
from typing import Dict, List

import streamlit as st

from frontend.streamlit_helpers import (
    download_json_in_server,
    get_default_options,
    get_json_file_names,
)

st.set_page_config(
    page_title="Check team's stats",
    page_icon="⚽",
    layout="wide",
)

# Session state initialization
if "visibility" not in st.session_state:
    st.session_state.visibility = "visible"
    st.session_state.disabled = False
if "team_name" not in st.session_state:
    st.session_state.team_name = ""
if "loaded_team" not in st.session_state:
    st.session_state.loaded_team = {}

joined_df = st.session_state.joined_df


st.markdown("# Check your team's stats")


st.divider()

# Load team
st.title("Load team")
saved_teams: List[str] = get_json_file_names(directory="data/my_teams")
team_name = st.selectbox(
    label="If any team has been saved, you can load it here:",
    options=saved_teams,
    index=0 if saved_teams else None,  # Default to the first team if available
    placeholder="Select team",
)
if team_name:
    with open(f"data/my_teams/{team_name}.json", "r") as file:
        st.session_state.loaded_team = json.load(file)

st.divider()


# Attackers
st.title("Attackers")
attackers_options: List[str] = st.multiselect(
    label="Choose your team's attackers:",
    options=joined_df.query("role == 'Attaccante'")["name"].unique(),
    default=get_default_options("attackers"),
)
st.line_chart(
    data=joined_df.query(f"name in {attackers_options}"),
    x="game_day",
    y="fanta_grade",
    color="name",
)

# Midfielders
st.title("Midfielders")
midfielders_options: List[str] = st.multiselect(
    label="Choose your team's midfielders:",
    options=joined_df.query("role == 'Centrocampista'")["name"].unique(),
    default=get_default_options("midfilders"),
)
st.line_chart(
    data=joined_df.query(f"name in {midfielders_options}"),
    x="game_day",
    y="fanta_grade",
    color="name",
)

# Defenders
st.title("Defenders")
defenders_options: List[str] = st.multiselect(
    label="Choose your team's defenders:",
    options=joined_df.query("role == 'Difensore'")["name"].unique(),
    default=get_default_options("defenders"),
)
st.line_chart(
    data=joined_df.query(f"name in {defenders_options}"),
    x="game_day",
    y="fanta_grade",
    color="name",
)

# Goalkeepers
st.title("Goalkeepers")
goalkeepers_options: List[str] = st.multiselect(
    label="Choose your team's goalkeepers:",
    options=joined_df.query("role == 'Portiere'")["name"].unique(),
    default=get_default_options("goalkeepers"),
)
st.line_chart(
    data=joined_df.query(f"name in {goalkeepers_options}"),
    x="game_day",
    y="fanta_grade",
    color="name",
)

st.divider()

# Save team
st.title("Save team")
st.text("Do you want to save this team so that next time it's automatically loaded?")
my_team: Dict[str, List[str]] = {
    "goalkeepers": goalkeepers_options,
    "defenders": defenders_options,
    "midfilders": midfielders_options,
    "attackers": attackers_options,
}
st.json(my_team)
team_name = st.text_input(
    label="Write your team's name here:👇",
    value=st.session_state.team_name,
    label_visibility=st.session_state.visibility,
    disabled=st.session_state.disabled,
    placeholder="My amazing team",
)
st.session_state.team_name = team_name
if st.button(label="📥 Save this team!⚽"):
    if st.session_state.team_name != "":
        assert st.session_state.team_name is not None
        download_json_in_server(data=my_team, team_name=st.session_state.team_name)
        st.success("Team successfully saved!")
    else:
        st.error("Please provide a team name before saving.")
