"""Module to define a router to get players stats."""

from typing import Dict, List, Union, no_type_check

from fastapi import APIRouter, HTTPException

from src.api.models import (
    GoalkeeperSummaryStatsResponse,
    OutfieldPlayerSummaryStatsResponse,
    PlayerLink,
)
from src.scraper.get_players_stats import (
    GetGoalkeeperSummaryStats,
    GetOufieldPlayerSummaryStats,
)

router = APIRouter()


@router.post(
    "/v1/player-summary-stats/outfield",
    response_model=OutfieldPlayerSummaryStatsResponse,
    summary="""Get outfiled player's summary stats for a season.

    Outfield players are:
    - attackers
    - midfilders
    - defenders
    """,
    tags=["Players"],
)
@no_type_check
async def get_outfield_player_summary_stats(
    player_link: PlayerLink,
) -> OutfieldPlayerSummaryStatsResponse:
    """Endpoint to get an outfield player's summary stats in a season.

    Outfield players are:
    - attackers
    - midfilders
    - defenders

    Parameters
    ----------
    player_link: PlayerLink
        Input object containing the player's name and link.

    Returns:
    -------
    OutfieldPlayerSummaryStatsResponse
        The outfield player's summary stats in a season.
    """
    scraper = GetOufieldPlayerSummaryStats(player_link=player_link)

    await scraper.scrape_all()

    if scraper.role.lower() == "goalkeeper":
        raise HTTPException(
            status_code=400,
            detail="The player is a goalkeeper. Use the goalkeepers endpoint.",
        )

    data: Dict[str, List[Union[int, float, str, None]]] = {
        "name": scraper.name,
        "avg_grade": scraper.avg_grade,
        "avg_fanta_grade": scraper.avg_fanta_grade,
        "median_grade": scraper.median_grade,
        "median_fanta_grade": scraper.median_fanta_grade,
        "role": scraper.role,
        "mantra_role": scraper.mantra_role,
        "graded_matches": scraper.graded_matches,
        "goals": scraper.goals,
        "assists": scraper.assists,
        "home_game_goals": scraper.home_game_goals,
        "away_game_goals": scraper.away_game_goals,
        "penalties_scored": scraper.penalties_scored,
        "penalties_shot": scraper.penalties_shot,
        "penalties_ratio": scraper.penalties_ratio,
        "autogoals": scraper.autogoals,
        "yellow_cards": scraper.yellow_cards,
        "red_cards": scraper.red_cards,
        "team": scraper.team,
        "description": scraper.description,
    }

    return OutfieldPlayerSummaryStatsResponse(data=data)


@router.post(
    "/v1/player-summary-stats/goalkeper",
    response_model=GoalkeeperSummaryStatsResponse,
    summary="Get goalkeeper's summary stats for a season.",
    tags=["Players"],
)
@no_type_check
async def get_goalkeeper_summary_stats(
    player_link: PlayerLink,
) -> GoalkeeperSummaryStatsResponse:
    """Endpoint to get an goalkeeper's summary stats in a season.

    Parameters
    ----------
    player_link: PlayerLink
        Input object containing the player's name and link.

    Returns:
    -------
    GoalkeeperSummaryStatsResponse
        The goalkeepr's summary stats in a season.
    """
    scraper = GetGoalkeeperSummaryStats(player_link=player_link)

    await scraper.scrape_all()

    if scraper.role.lower() != "portiere":
        raise HTTPException(
            status_code=400,
            detail="""The player is an outfield player.
            Use the outfield player endpoint.""",
        )

    data: Dict[str, List[Union[int, float, str, None]]] = {
        "name": scraper.name,
        "avg_grade": scraper.avg_grade,
        "avg_fanta_grade": scraper.avg_fanta_grade,
        "median_grade": scraper.median_grade,
        "median_fanta_grade": scraper.median_fanta_grade,
        "role": scraper.role,
        "mantra_role": scraper.mantra_role,
        "graded_matches": scraper.graded_matches,
        "goals_conceded": scraper.goals_conceded,
        "assists": scraper.assists,
        "home_game_goals_conceded": scraper.home_game_goals_conceded,
        "away_game_goals_conceded": scraper.away_game_goals_conceded,
        "penalties_saved": scraper.penalties_saved,
        "autogoals": scraper.autogoals,
        "yellow_cards": scraper.yellow_cards,
        "red_cards": scraper.red_cards,
        "team": scraper.team,
        "description": scraper.description,
    }

    return GoalkeeperSummaryStatsResponse(data=data)
