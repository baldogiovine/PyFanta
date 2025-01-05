"""Module to define a router to get matches stats."""

from typing import no_type_check

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

    name = scraper.name
    game_days = scraper.game_day
    grades = scraper.grade
    fanta_grades = scraper.fanta_grade
    bonuses = scraper.bonus
    maluses = scraper.malus
    home_teams = scraper.home_team
    guest_teams = scraper.guest_team
    home_team_scores = scraper.home_team_score
    guest_team_scores = scraper.guest_team_score
    subs_in = scraper.sub_in
    subs_out = scraper.sub_out

    rows = []
    for i in range(len(game_days)):
        row = {
            "name": name,
            "game_day": game_days[i],
            "grade": grades[i],
            "fanta_grade": fanta_grades[i],
            "bonus": bonuses[i],
            "malus": maluses[i],
            "home_team": home_teams[i],
            "guest_team": guest_teams[i],
            "home_team_score": home_team_scores[i],
            "guest_team_score": guest_team_scores[i],
            "subsitution_in": subs_in[i],
            "subsitution_out": subs_out[i],
        }
        rows.append(row)

    return MatchesStatsResponse(data=rows)
