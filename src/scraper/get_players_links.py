"""Module to get players links. Links are necessary to scrape players data."""

import re
from typing import Dict, List, Union

from bs4 import BeautifulSoup
from bs4.element import NavigableString, Tag

from src.scraper.beautiful_soup_base_scraping_class import BeautifulSoupBaseScraper
from src.scraper.constants import PlayerLinksConstants
from src.scraper.exceptions import PageStructureError


class GetPlayersLinks(BeautifulSoupBaseScraper):
    """An asynchronous class to scrape player names and links from a specified year.

    Attributes:
    ----------
    year : str
        The year for which player links are to be fetched, e.g., "2023-24", "2022-23".
    """

    def __init__(self, year: str):  # noqa: D107
        if not re.match(r"^\d{4}-\d{2}$", year):
            raise ValueError("Year must be in the format YYYY-YY, e.g., 2024-25")
        self.year: str = year
        self.url: str = self._construct_url()
        self.soup: Union[BeautifulSoup, None] = None

    def _construct_url(self) -> str:
        """Constructs the URL to fetch the page content.

        Returns:
        -------
        str
            The URL to fetch the page content.
        """
        return f"{PlayerLinksConstants.fantacalcio_link}/{self.year}/"

    async def get_links(self) -> List[Dict[str, str]]:
        """Asynchronously extract player links from the webpage.

        Returns:
        -------
        List[Dict[str, str]]
            List of dictionaries containing players' names and links.
        """
        if not self.soup:
            await self.fetch_page(url=self.url)
        if not isinstance(self.soup, BeautifulSoup):
            raise PageStructureError("Soup is not a BeautifulSoup instance.")
        try:
            container: Union[Tag, NavigableString, None] = self.soup.find(
                "div", class_="container"
            )
            if not isinstance(container, Tag):
                raise PageStructureError("Missing or invalid 'container' div.")

            table_overflow: Union[Tag, NavigableString, None] = container.find(
                "div", class_="table-overflow"
            )
            if not isinstance(table_overflow, Tag):
                raise PageStructureError("Missing or invalid 'table-overflow' div.")

            table: Union[Tag, NavigableString, None] = table_overflow.find("table")
            if not isinstance(table, Tag):
                raise PageStructureError("Missing or invalid 'table' tag.")

            links: List[Tag] = table.find_all("a", class_="player-name player-link")
            if not isinstance(links, list):
                raise PageStructureError("No player links found in the table.")

            data: List[Dict[str, str]] = []
            for link in links:
                player_dict: Dict[str, str] = {
                    "name": link.get_text(separator="\n", strip=True),
                    "link": self._get_attribute_as_str(tag=link, attr_name="href"),
                }
                if not player_dict["name"] or not player_dict["link"]:
                    raise PageStructureError("Player name or link is missing.")
                if player_dict["link"][-7:] != self.year:
                    player_dict["link"] = f'{player_dict.get("link")}/{self.year}'
                data.append(player_dict)
            return data
        except AttributeError as e:
            raise PageStructureError(
                "Unexpected page structure while extracting player links."
            ) from e

    @staticmethod
    def _get_attribute_as_str(tag: Tag, attr_name: str) -> str:
        """Safely retrieve an attribute value from a BeautifulSoup Tag as a string.

        Parameters
        ----------
        tag : Tag
            The BeautifulSoup Tag object from which to retrieve the attribute.
        attr_name : str
            The name of the attribute to retrieve.

        Returns:
        -------
        str
            The attribute value as a string. If the attribute is not found or its
            value is `None`, returns an empty string.
        """
        try:
            attr_value: Union[str, List[str], None] = tag.get(attr_name)
            if isinstance(attr_value, str):
                return attr_value
            elif isinstance(attr_value, list):
                return attr_value[0] if attr_value else ""
            else:
                return ""
        except Exception as e:
            raise ValueError(
                f"Failed to get attribute '{attr_name}' from tag: {e}"
            ) from e
