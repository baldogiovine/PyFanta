"""Module to test beautiful_soup_base_scraping_class module."""

import asyncio

import pytest
from aioresponses import aioresponses

from src.scraper.beautiful_soup_base_scraping_class import BeautifulSoupBaseScraper
from src.scraper.exceptions import FetchError


@pytest.mark.asyncio  # type: ignore
async def test_fetch_page_success() -> None:
    """Test that fetch_page successfully fetches and parses content."""
    url = "https://mocked_url.com"
    mocked_html = "<html><body><h1>Hello, World!</h1></body></html>"

    scraper = BeautifulSoupBaseScraper()

    with aioresponses() as mocked:
        mocked.get(url, status=200, body=mocked_html)

        await scraper.fetch_page(url)

        assert scraper.soup is not None
        assert scraper.soup.h1.text == "Hello, World!"


@pytest.mark.asyncio  # type: ignore
async def test_fetch_page_client_error() -> None:
    """Test that fetch_page raises FetchError on client errors."""
    url = "https://mocked_url.com"

    scraper = BeautifulSoupBaseScraper()

    with aioresponses() as mocked:
        mocked.get(url, status=404)

        with pytest.raises(FetchError, match="Error fetching URL"):
            await scraper.fetch_page(url)


@pytest.mark.asyncio  # type: ignore
async def test_fetch_page_timeout_error() -> None:
    """Test that fetch_page raises FetchError on timeout."""
    url = "https://mocked_url.com"

    scraper = BeautifulSoupBaseScraper()

    with aioresponses() as mocked:
        mocked.get(url, exception=asyncio.TimeoutError)  # Simulate a timeout

        with pytest.raises(FetchError, match="timed out"):
            await scraper.fetch_page(url)


def test_fetch_page_invalid_url() -> None:
    """Test that fetch_page raises AssertionError for non-string URLs."""
    scraper = BeautifulSoupBaseScraper()

    # Using pytest.raises for assertion failure
    with pytest.raises(AssertionError):
        asyncio.run(scraper.fetch_page(12345))  # type: ignore
