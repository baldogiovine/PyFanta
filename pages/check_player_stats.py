"""Module to design a Strealit page to check players' stats."""

from typing import List, Union

import streamlit as st

from frontend.constants import PlotsConstants
from frontend.streamlit_helpers import make_donut_plot, make_gauge_plot, make_radar_plot

st.set_page_config(
    page_title="Check players' stats",
    page_icon="⚽",
    layout="wide",
)

joined_df = st.session_state.joined_df

st.markdown("# Check your players' stats")

st.divider()

st.title("Choose a player")

players: Union[List[str], None] = st.multiselect(
    label="Choose one or more players:",
    options=joined_df["name"].unique(),
    placeholder="Select player/s",
)

if players:
    assert isinstance(players, List)

    # Grades radar plot
    st.markdown("## Average grades analysis")
    make_radar_plot(
        data=joined_df,
        players=players,
        categories=PlotsConstants.player_general_stats_constants,
    )

    st.divider()

    st.markdown("## Goals analysis")
    for player in players:
        # Goals donut plot
        st.markdown(f"### {player}")
        make_donut_plot(
            data=joined_df,
            player=player,
            categories=PlotsConstants.goals_constants,
        )

        # Penalties gauge plot
        st.markdown("### Penalties analysis")
        make_gauge_plot(
            current_value=joined_df.query(f"name == '{player}'")[
                "penalties_scored"
            ].iloc[0],
            max_value=joined_df.query(f"name == '{player}'")["penalties_shot"].iloc[0],
            title="Scored penalties",
        )

        st.divider()
