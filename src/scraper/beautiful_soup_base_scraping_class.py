"""Module to define an abstract scraping class for scraping classes based on
BeautifulSoup.
"""  # noqa: D205

import asyncio
from typing import Union

import aiohttp
from bs4 import BeautifulSoup

from src.scraper.exceptions import FetchError


class BeautifulSoupBaseScraper:
    """Base class to define a scraping class based on BeautifulSoup."""

    def __init__(self) -> None:  # noqa: D107 # type: ignore
        self.soup: Union[BeautifulSoup, None] = None

    async def fetch_page(self, url: str) -> None:
        """Asynchronously fetches the page content and parse it with BeautifulSoup."""
        try:
            async with aiohttp.ClientSession() as session:
                assert isinstance(url, str)
                async with session.get(url, timeout=15) as response:
                    response.raise_for_status()
                    content: bytes = await response.read()
                    self.soup = BeautifulSoup(content, "lxml")
        except aiohttp.ClientError as e:
            raise FetchError(f"Error fetching URL {url}: {e}") from e
        except asyncio.TimeoutError as te:
            raise FetchError(f"Request to {url} timed out.") from te
