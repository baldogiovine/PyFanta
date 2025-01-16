"""Module to test get_players_links module."""

from unittest.mock import patch

import pytest

from src.scraper.get_players_links import GetPlayersLinks


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
