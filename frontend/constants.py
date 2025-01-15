"""Module to define constants."""

from typing import List


class PlotsConstants:
    """Class to store constants to use in frontend plots."""

    player_general_stats_constants: List[str] = [
        "avg_grade",
        "avg_fanta_grade",
        "median_grade",
        "median_fanta_grade",
    ]

    goals_constants: List[str] = [
        "home_game_goals",
        "away_game_goals",
    ]

    # other_constants: List[str] = [
    #     "goals",
    #     "assists",
    #     "yellow_cards",
    #     "red_cards",
    #     "autogoals",
    #     "penalties_scored",
    # ]
