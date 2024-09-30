"""Module to organize Pydantic data validation models for FastAPI endpoints."""

from typing import List

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
    grade: List[float]
    fanta_grade: List[float]
    bonus: List[float]
    malus: List[float]
    home_team: List[str]
    guest_team: List[str]
    home_team_score: List[int]
    guest_team_score: List[int]
    subsitution_in: List[float]
    subsitution_out: List[float]


class MatchesStatsResponse(BaseModel):
    """Data validation model for all the matches."""

    data: List[MatchesStats]
