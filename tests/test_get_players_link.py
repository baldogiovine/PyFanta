"""Module to test get_players_links module."""

from unittest.mock import patch

import pytest
from aioresponses import aioresponses

from src.scraper.get_players_links import GetPlayersLinks


@pytest.fixture  # type: ignore
def year() -> str:
    """Pytest fixture to pass "year" parameter to GetPlayersLinks class."""
    return "2024-25"


@pytest.fixture  # type: ignore
def url(year: str) -> str:
    """Pytest fixture to construct the URL for fetching player links.

    Parameters
    ----------
    year : str
        The year for which player links are to be fetched.

    Returns:
    -------
    str
        The constructed URL for the specified year.
    """
    scraper = GetPlayersLinks(year)
    return scraper._construct_url()


@pytest.mark.parametrize(  # type: ignore
    "year, expected_url",
    [
        ("2024-25", "https://mocked_link/2024-25/"),
        ("2023-24", "https://mocked_link/2023-24/"),
        ("2022-23", "https://mocked_link/2022-23/"),
    ],
)
def test_construct_url(year: str, expected_url: str) -> None:
    """Test URL construction directly with a patched constant."""
    with patch(
        "src.scraper.constants.PlayerLinksConstants.fantacalcio_link",
        "https://mocked_link",
    ):
        scraper = GetPlayersLinks(year=year)
        assert scraper._construct_url() == expected_url


@pytest.mark.asyncio  # type: ignore
async def test_get_links_success(year: str, url: str) -> None:
    """Test that get_links successfully extracts player names and links."""
    mocked_html = """
    <div class="container">
        <div class="table-overflow">
            <table>
                <tr class="player-row">
                    <th class="player-name">
                        <a class="player-name player-link" href="https://www.fantacalcio.it/serie-a/squadre/atalanta/lookman/4730">
                        <span>Lookman</span>
                        <a class="player-name player-link" href="https://www.fantacalcio.it/serie-a/squadre/milan/pulisic/2423">
                            <span>Pulisic</span>
                        </a>
                    </th>
                </tr>
            </table>
        </div>
    </div>
    """

    with aioresponses() as mocked:
        mocked.get(url, status=200, body=mocked_html)

        scraper = GetPlayersLinks(year)
        result = await scraper.get_links()

        number_results = 2
        assert len(result) == number_results
        assert result[0]["name"] == "Lookman"
        assert (
            result[0]["link"]
            == "https://www.fantacalcio.it/serie-a/squadre/atalanta/lookman/4730/2024-25"
        )
        assert result[1]["name"] == "Pulisic"
        assert (
            result[1]["link"]
            == "https://www.fantacalcio.it/serie-a/squadre/milan/pulisic/2423/2024-25"
        )
