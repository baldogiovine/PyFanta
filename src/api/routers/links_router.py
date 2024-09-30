"""Module to define a router to get players links."""

from typing import Dict, List, no_type_check

from fastapi import APIRouter

from src.api.models import PlayersLinksResponse
from src.scraper.get_players_links import GetPlayersLinks

router = APIRouter()


@router.get(
    "/v1/players-links/{year}",
    response_model=PlayersLinksResponse,
    summary="Get players' names and links for a specified year",
    tags=["Links"],
)
@no_type_check
async def get_players_links(year: str) -> PlayersLinksResponse:
    """Endpoint to get players' names and links for a specified year.

    Parameters
    ----------
    year : str
        The year for which player links are to be fetched, e.g., "2023-24", "2022-23".

    Returns:
    -------
    PlayersLinksResponse
        Players' names and links for a the `year` season.
    """
    scraper = GetPlayersLinks(year=year)
    data: List[Dict[str, str]] = await scraper.get_links()
    return PlayersLinksResponse(data=data)
