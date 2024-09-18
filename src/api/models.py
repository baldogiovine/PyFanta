"""Module to organize Pydantic data validation models for FastAPI endpoints."""

from typing import List

from pydantic import BaseModel


class PlayerLink(BaseModel):
    """Data validation model for a single player."""

    name: str
    link: str


class PlayersLinksResponse(BaseModel):
    """Data validation model for all the players."""

    data: List[PlayerLink]
