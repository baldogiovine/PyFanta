"""Moudule to test get_matches_stats module."""

from typing import List, Union

import pytest
from bs4 import BeautifulSoup

from src.api.models import PlayerLink
from src.scraper.get_matches_stats import GetMatchesStats

PULISIC_PLAYER_LINK: dict[str, str] = {
    "name": "Pulisic",
    "link": "https://www.fantacalcio.it/serie-a/squadre/milan/pulisic/2423/2024-25",
}


@pytest.fixture(scope="module")  # type: ignore
def player_link() -> PlayerLink:
    """Fixture to create a PlayerLink object for testing."""
    return PlayerLink(
        name=PULISIC_PLAYER_LINK["name"],
        link=PULISIC_PLAYER_LINK["link"],
    )


@pytest.fixture(scope="function")  # type: ignore
def scraper(player_link: PlayerLink) -> GetMatchesStats:
    """Fixture to create a GetMatchesStats object for testing."""
    return GetMatchesStats(player_link=player_link)


def test_get_matches_stats_init(scraper: GetMatchesStats) -> None:
    """Test initialization of GetMatchesStats."""
    assert scraper.name == PULISIC_PLAYER_LINK.get("name")
    assert scraper.url == PULISIC_PLAYER_LINK.get("link")
    assert scraper.soup is None


def test_get_game_day(scraper: GetMatchesStats) -> None:
    """Test get_game_day method."""
    result = scraper.get_game_day()
    assert result == list(range(1, 39))
    assert scraper.game_day == list(range(1, 39))


@pytest.mark.asyncio  # type: ignore
async def test_get_grade(scraper: GetMatchesStats) -> None:
    """Test get_grade method."""
    mocked_html = """
    <html>
        <span class="grade" data-value="7.5"></span>
        <span class="grade" data-value="6.0"></span>
        <span class="grade" data-value=""></span>
    </html>
    """
    scraper.soup = BeautifulSoup(mocked_html, "lxml")

    result: List[Union[float, None]] = await scraper.get_grade()
    assert result == [7.5, 6.0, None]
    assert scraper.grade == [7.5, 6.0, None]


@pytest.mark.asyncio  # type: ignore
async def test_get_fanta_grade(scraper: GetMatchesStats) -> None:
    """Test get_fanta_grade method."""
    mocked_html = """
    <html>
        <span class="fanta-grade" data-value="11.5"></span>
        <span class="fanta-grade" data-value="3.0"></span>
        <span class="fanta-grade" data-value=""></span>
    </html>
    """
    scraper.soup = BeautifulSoup(mocked_html, "lxml")

    result: List[Union[float, None]] = await scraper.get_fanta_grade()
    assert result == [11.5, 3.0, None]
    assert scraper.fanta_grade == [11.5, 3.0, None]


@pytest.mark.asyncio  # type: ignore
async def test_get_match_score(scraper: GetMatchesStats) -> None:
    """Test get_match_score method."""
    mocked_html = """
    <html>
        <span class="match-score">3-2</span>
        <span class="match-score">1-1</span>
        <span class="match-score">0-0</span>
    </html>
    """
    scraper.soup = BeautifulSoup(mocked_html, "lxml")

    home_scores, guest_scores = await scraper.get_match_score()
    assert home_scores == [3, 1, 0]
    assert guest_scores == [2, 1, 0]


# TODO: test get_bonus and get_mauls
@pytest.mark.asyncio  # type: ignore
async def test_get_bonus(scraper: GetMatchesStats) -> None:
    """Test."""
    pass


@pytest.mark.asyncio  # type: ignore
async def test_get_home_team(scraper: GetMatchesStats) -> None:
    """Test."""
    mocked_html = """
    <html>
        <span class="team-home">Rom</span>
        <span class="team-home">Mil</span>
        <span class="team-home">Cag</span>
        <span class="team-home">fake_match_to_remove</span>
        <span class="team-home">fake_match_to_remove</span>
    </html>
    """
    scraper.soup = BeautifulSoup(mocked_html, "lxml")

    home_team = await scraper.get_home_team()
    assert home_team == [
        "Rom",
        "Mil",
        "Cag",
    ]


def test_post_game_day_fix(scraper: GetMatchesStats) -> None:
    """Test that game_day is correctly adapted to the number of elements fetched from
    the other methods."""  # noqa: D205, D209
    scraper.game_day = list(range(1, 40))
    scraper.grade = [6.5, 7.0, None]
    scraper.post_game_day_fix()

    assert scraper.game_day == [1, 2, 3]
