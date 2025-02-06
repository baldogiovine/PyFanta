"""Module to test beautiful_soup_base_scraping_class module."""

import asyncio

import pytest
from aioresponses import aioresponses

from src.scraper.beautiful_soup_base_scraping_class import BeautifulSoupBaseScraper
from src.scraper.exceptions import FetchError


@pytest.fixture(scope="module")  # type: ignore
def url() -> str:
    """Pytest fixture that returns a mocked url to be used in tests."""
    return "https://mocked_url.com"


@pytest.fixture(scope="module")  # type: ignore
def scraper() -> BeautifulSoupBaseScraper:
    """Pytest fixture to create a BeautifulSoupBaseScraper object for testing."""
    return BeautifulSoupBaseScraper()


@pytest.mark.asyncio  # type: ignore
async def test_fetch_page_success(
    url: str,
    scraper: BeautifulSoupBaseScraper,
) -> None:
    """Test that fetch_page successfully fetches and parses content."""
    mocked_html = "<html><body><h1>Hello, World!</h1></body></html>"

    with aioresponses() as mocked:
        mocked.get(url, status=200, body=mocked_html)

        await scraper.fetch_page(url)

        assert scraper.soup is not None
        assert scraper.soup.h1.text == "Hello, World!"


@pytest.mark.asyncio  # type: ignore
async def test_fetch_page_client_error(
    url: str,
    scraper: BeautifulSoupBaseScraper,
) -> None:
    """Test that fetch_page raises FetchError on client errors."""
    with aioresponses() as mocked:
        mocked.get(url, status=404)

        with pytest.raises(FetchError, match="Error fetching URL"):
            await scraper.fetch_page(url)


@pytest.mark.asyncio  # type: ignore
async def test_fetch_page_timeout_error(
    url: str,
    scraper: BeautifulSoupBaseScraper,
) -> None:
    """Test that fetch_page raises FetchError on timeout."""
    with aioresponses() as mocked:
        mocked.get(url, exception=asyncio.TimeoutError)  # Simulate a timeout

        with pytest.raises(FetchError, match="timed out"):
            await scraper.fetch_page(url)


def test_fetch_page_invalid_url(scraper: BeautifulSoupBaseScraper) -> None:
    """Test that fetch_page raises AssertionError for non-string URLs."""
    # Using pytest.raises for assertion failure
    with pytest.raises(AssertionError):
        asyncio.run(scraper.fetch_page(12345))  # type: ignore
