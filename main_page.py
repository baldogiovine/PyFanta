"""Main streamlit app module."""

import streamlit as st
from pandas import DataFrame

from frontend.streamlit_helpers import (
    download_data_from_fastapi_api,
    load_matches_dataframe,
    load_players_dataframe,
)

st.set_page_config(
    page_title="PyFanta",
    page_icon="⚽",
    layout="wide",
)

st.write("# Welcome to PyFanta! 👋")

st.divider()

st.sidebar.success("Select a page above.")


# Download data
st.title("Download data")
if st.button(label="Download data"):
    download_data_from_fastapi_api()

# Show data
matches_stats_df: DataFrame = load_matches_dataframe(
    path_to_json="data/matches_data_2024-25.json"
)
outfield_players_df: DataFrame = load_players_dataframe(
    path_to_json="data/outfiled_players_summary_stats_data_2024-25.json"
)
goalkeepers_df: DataFrame = load_players_dataframe(
    path_to_json="data/goalkeepers_summary_stats_data_2024-25.json"
)

joined_df = (
    matches_stats_df.set_index("name")
    .combine_first(outfield_players_df.set_index("name"))
    .combine_first(goalkeepers_df.set_index("name"))
    .reset_index()
)
st.session_state.joined_df = joined_df

st.dataframe(data=joined_df)
