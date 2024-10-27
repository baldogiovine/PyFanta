"""Module to define a router to get matches stats."""

from typing import Dict, List, Union, no_type_check

from fastapi import APIRouter

from src.api.models import MatchesStatsResponse, PlayerLink
from src.scraper.get_matches_stats import GetMatchesStats

router = APIRouter()


@router.post(
    "/v1/matches-stats",
    response_model=MatchesStatsResponse,
    summary="Get player's match stats",
    tags=["Matches"],
)
@no_type_check
async def get_matches_stats(player_link: PlayerLink) -> MatchesStatsResponse:
    """Endpoint to get player's match stats.

    Parameters
    ----------
    player_link: PlayerLink
        Input object containing the player's name and link.

    Returns:
    -------
    MatchesStatsResponse
        The match stats of the player.
    """
    scraper = GetMatchesStats(player_link=player_link)

    await scraper.scrape_all()

    data: Dict[str, List[Union[int, float, str, None]]] = {
        "name": scraper.name,
        "game_day": scraper.game_day,
        "grade": scraper.grade,
        "fanta_grade": scraper.fanta_grade,
        "bonus": scraper.bonus,
        "malus": scraper.malus,
        "home_team": scraper.home_team,
        "guest_team": scraper.guest_team,
        "home_team_score": scraper.home_team_score,
        "guest_team_score": scraper.guest_team_score,
        "subsitution_in": scraper.sub_in,
        "subsitution_out": scraper.sub_out,
    }

    return MatchesStatsResponse(data=data)
