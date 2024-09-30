"""Module to define a router to get matches stats."""

from typing import List, no_type_check

from fastapi import APIRouter

from src.api.models import MatchesStatsResponse, PlayerLink
from src.scraper.get_matches_stats import GetMatchesStats

router = APIRouter()


@router.post(
    "v1/matches-stats",
    response_model=MatchesStatsResponse,
    summary="Get player's match stats",
    tags=["Matches"],
)
@no_type_check
async def get_matches_stats(player_link: PlayerLink) -> MatchesStatsResponse:
    """Endpoint to get player's match stats.

    Parameters
    ----------


    Returns:
    -------
    MatchesStatsResponse
        The match stats of the player.
    """
    scraper = GetMatchesStats(player_link=player_link)

    name: str = scraper.name
    game_day: List[int] = scraper.get_game_day()
    grade: List[float] = await scraper.get_grade()
    fanta_grade: List[float] = await scraper.get_fanta_grade()
    bonus: List[float] = await scraper.get_bonus()
    malus: List[float] = await scraper.get_malus()
    home_team: List[str] = await scraper.get_home_team()
    guest_team: List[str] = await scraper.get_guest_team()
    home_team_score: List[int] = await scraper.get_match_score()[0]
    guest_team_score: List[int] = await scraper.get_match_score()[1]
    subsitution_in: List[float] = await scraper.get_minute_in()
    subsitution_out: List[float] = await scraper.get_minute_out()

    # Prepare the response data
    data = {
        "name": name,
        "game_day": game_day,
        "grade": grade,
        "fanta_grade": fanta_grade,
        "bonus": bonus,
        "malus": malus,
        "home_team": home_team,
        "guest_team": guest_team,
        "home_team_score": home_team_score,
        "guest_team_score": guest_team_score,
        "subsitution_in": subsitution_in,
        "subsitution_out": subsitution_out,
    }
    return MatchesStatsResponse(data=data)
