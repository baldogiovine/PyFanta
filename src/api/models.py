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


class MatchesStats(BaseModel):
    """Data validation model for a single match."""

    name: str
    game_day: List[int]
    grade: List[Union[float, None]]
    fanta_grade: List[Union[float, None]]
    bonus: List[Union[float, None]]
    malus: List[Union[float, None]]
    home_team: List[str]
    guest_team: List[str]
    home_team_score: List[int]
    guest_team_score: List[int]
    subsitution_in: List[Union[float, None]]
    subsitution_out: List[Union[float, None]]


class MatchesStatsResponse(BaseModel):
    """Data validation model for all the matches."""

    data: Union[MatchesStats, List[MatchesStats]]
