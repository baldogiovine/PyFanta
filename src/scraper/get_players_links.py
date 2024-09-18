"""Module to get players links. Links are necessary to scrape players data."""

import asyncio
from typing import Dict, List, Union

import aiohttp
from bs4 import BeautifulSoup
from bs4.element import Tag

from src.scraper.constants import PlayerLinksConstants
from src.scraper.exceptions import FetchError, PageStructureError


class GetPlayersLinks:
    """An asynchronous class to scrape player names and links from a specified year.

    Attributes:
    ----------
    year : str
        The year for which player links are to be fetched, e.g., "2023-24", "2022-23".
    """

    def __init__(self, year: str):  # noqa: D107
        self.year: str = year
        self.__url: str = self.__construct_url()
        self.__soup: Union[BeautifulSoup, None] = None

    def __construct_url(self) -> str:
        """Construct the full URL for fetching player links."""
        return f"{PlayerLinksConstants.fantacalcio_link}/{self.year}/"

    async def __fetch_page(self) -> None:
        """Asynchronously fetch the page content and parse it with BeautifulSoup."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.__url, timeout=5) as response:
                    response.raise_for_status()
                    content: bytes = await response.read()
                    self.__soup = BeautifulSoup(content, "lxml")
        except aiohttp.ClientError as e:
            raise FetchError(f"Error fetching URL {self.__url}: {e}") from e
        except asyncio.TimeoutError as te:
            raise FetchError(f"Request to {self.__url} timed out.") from te

    async def get_links(self) -> List[Dict[str, str]]:
        """Asynchronously extract player links from the webpage.

        Returns:
        -------
        List[Dict[str, str]]
            List of dictionaries containing players' names and links.
        """
        if not self.__soup:
            await self.__fetch_page()
        assert isinstance(self.__soup, BeautifulSoup)
        try:
            container: Union[Tag, None] = self.__soup.find("div", class_="container")
            assert isinstance(container, Tag)
            table_overflow: Union[Tag, None] = container.find(
                "div", class_="table-overflow"
            )
            assert isinstance(table_overflow, Tag)
            table: Union[Tag, None] = table_overflow.find("table")
            assert isinstance(table, Tag)
            links: List[Tag] = table.find_all("a", class_="player-name player-link")
            assert isinstance(links, List)

            data: List[Dict[str, str]] = [
                {
                    "name": link.get_text(separator="\n", strip=True),
                    "link": link.get("href"),
                }
                for link in links
            ]
            return data
        except AttributeError as e:
            raise PageStructureError(
                "Unexpected page structure while extracting player links"
            ) from e
