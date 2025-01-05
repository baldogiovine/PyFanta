"""Module to organize Pydantic data validation models for FastAPI endpoints."""

from typing import List, Union

from pydantic import BaseModel


class PlayerLink(BaseModel):
    """Data validation model for a single player links."""

    name: str
    link: str


class PlayersLinksResponse(BaseModel):
    """Data validation model for all the players links."""

    data: List[PlayerLink]


class SingleMatch(BaseModel):
    """Data validation model for a single player-game-day observation."""

    name: str
    game_day: int
    grade: Union[float, None]
    fanta_grade: Union[float, None]
    bonus: Union[float, None]
    malus: Union[float, None]
    home_team: str
    guest_team: str
    home_team_score: int
    guest_team_score: int
    subsitution_in: Union[float, None]
    subsitution_out: Union[float, None]


class MatchesStatsResponse(BaseModel):
    """Data validation model for a list of player-game-day observations."""

    data: Union[SingleMatch, List[SingleMatch]]


class BasePlayerSummaryStats(BaseModel):
    """Data validation model for a single player summary stats in a season.

    This model takes in accounts only the common stats between outfield players and
    goalkeepers.
    """

    name: str
    role: str
    mantra_role: str
    team: str
    description: str
    avg_grade: Union[float, None]
    avg_fanta_grade: Union[float, None]
    median_grade: Union[float, None]
    median_fanta_grade: Union[float, None]


class OutfieldPlayerSummaryStats(BasePlayerSummaryStats):
    """Data validation model for a single outfiled player summary stats in a season.

    Outfield players are:
    - attackers
    - midfilders
    - defenders
    """

    graded_matches: int
    goals: int
    assists: int
    home_game_goals: int
    away_game_goals: int
    penalties_scored: int
    penalties_shot: int
    penalties_ratio: Union[float, None]
    autogoals: int
    yellow_cards: int
    red_cards: int


class OutfieldPlayerSummaryStatsResponse(BaseModel):
    """Data validation model for all the outfield players.

    Outfield players are:
    - attackers
    - midfilders
    - defenders
    """

    data: Union[OutfieldPlayerSummaryStats, List[OutfieldPlayerSummaryStats]]


class GoalkeeperSummaryStats(BasePlayerSummaryStats):
    """Data validation model for a single goalkeeper summary stats in a season."""

    graded_matches: int
    goals_conceded: int
    assists: int
    home_game_goals_conceded: int
    away_game_goals_conceded: int
    penalties_saved: int
    autogoals: int
    yellow_cards: int
    red_cards: int


class GoalkeeperSummaryStatsResponse(BaseModel):
    """Data validation model for all the goalkeepers."""

    data: Union[GoalkeeperSummaryStats, List[GoalkeeperSummaryStats]]
