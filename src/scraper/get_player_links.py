"""Module to get players links. Links are necessary to scrape players data."""

from dataclasses import dataclass, field
from typing import Dict, List

import requests
from bs4 import BeautifulSoup

from src.scraper.constants import CommonConstants, PlayerLinksConstants


@dataclass
class GetPlayersLinks:
    """A class to scrape and manage player links from a specified year.

    This class is designed to fetch player links from the Leghe Fantacalcio website
    for a specified year. It performs HTTP requests to get the HTML content,
    parses the content to extract player names and their links, and stores
    this information in a pandas DataFrame. The class also provides functionality
    to add unique identifiers to each player and save the DataFrame as a CSV file.

    Attributes:
    ----------
    year : str
        The year for which player links are to be fetched. e.g., "2023-24", "2022-23".

    Other Attributes
    ----------------
    url : str
        The constructed URL based on the specified year.
    soup : BeautifulSoup
        The BeautifulSoup object used to parse the HTML content.
    data : List[Dict[str, str]]
        List of dictionaries containing player name and link.
    """

    year: str
    url: str = field(init=False)
    soup: BeautifulSoup = field(init=False)
    data: List[Dict[str, str]] = field(init=False, default_factory=list)

    def __post_init__(self):  # noqa: D105
        self.url = self.get_full_url()
        response = requests.get(self.url, timeout=5)
        self.check_status_code(response)
        self.soup = BeautifulSoup(response.content, "lxml")

    def get_full_url(self) -> str:
        """Construct the full URL for fetching player links."""
        return f"{PlayerLinksConstants.fantacalcio_link}/{self.year}/"

    def check_status_code(self, response: requests.Response) -> None:
        """Check the status code of the response."""
        if response.status_code != CommonConstants.status_code_ok:
            raise ValueError(f"Request failed with status code {response.status_code}")

    def get_links(self) -> "GetPlayersLinks":
        """Extract player links from the webpage."""
        soup_link = (
            self.soup.find("div", class_="container")
            .find("div", class_="table-overflow")
            .find("table")
            .find_all("a", class_="player-name player-link")
        )

        self.data = [
            {
                "name": one_soup.get_text(separator="\n", strip=True),
                "link": one_soup.get("href"),
            }
            for one_soup in soup_link
        ]
        return self
