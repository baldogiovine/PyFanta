"""Module to get players links. Links are necessary to scrape players data"""

import os
import uuid
from dataclasses import dataclass, field

import pandas as pd
import requests
from bs4 import BeautifulSoup


@dataclass
class GetPlayersLinks:
    """A class to scrape and manage player links from a specified year.

    This class is designed to fetch player links from the Leghe Fantacalcio website
    for a specified year. It performs HTTP requests to get the HTML content,
    parses the content to extract player names and their links, and stores
    this information in a pandas DataFrame. The class also provides functionality
    to add unique identifiers to each player and save the DataFrame as a CSV file.

    Attributes
    ----------
    year : str
        The year for which player links are to be fetched. e.g., "2023-24", "2022-23".

    Other Attributes
    ----------------
    url : str
        The constructed URL based on the specified year.
    soup : BeautifulSoup
        The BeautifulSoup object used to parse the HTML content.
    df : pd.DataFrame
        DataFrame to store player names and links.
    """

    year: str
    url: str = field(init=False)
    soup: BeautifulSoup = field(init=False)
    df: pd.DataFrame = field(
        init=False, default_factory=lambda: pd.DataFrame(columns=["name", "link"])
    )

    def __post_init__(self):
        self.url = self.get_full_url()
        response = requests.get(self.url, timeout=5)
        self.check_status_code(response)
        self.soup = BeautifulSoup(response.content, "lxml")

    def get_full_url(self) -> str:
        """Construct the full URL for fetching player links."""
        base_link = "https://www.fantacalcio.it/quotazioni-fantacalcio"
        return f"{base_link}/{self.year}/"

    def check_status_code(self, response: requests.Response) -> None:
        """Check the status code of the response."""
        if response.status_code != 200:
            raise ValueError(f"Request failed with status code {response.status_code}")

    def get_links(self) -> "GetPlayersLinks":
        """Extract player links from the webpage."""
        soup_link = (
            self.soup.find("div", class_="container")
            .find("div", class_="table-overflow")
            .find("table")
            .find_all("a", class_="player-name player-link")
        )

        player_data = [
            {
                "name": one_soup.get_text(separator="\n", strip=True),
                "link": one_soup.get("href"),
            }
            for one_soup in soup_link
        ]

        self.df = pd.DataFrame(player_data)
        return self

    def add_ids(self) -> "GetPlayersLinks":
        """Add unique IDs to each player link."""
        self.df["player_id"] = [str(uuid.uuid4()) for _ in range(len(self.df))]
        return self

    def save_csv(self) -> None:
        """Save the DataFrame to a CSV file."""
        os.makedirs("data", exist_ok=True)
        self.df.to_csv(f"data/players_links_{self.year}.csv", index=False)

    def get_dataframe(self) -> pd.DataFrame:
        """Return the DataFrame containing player links and IDs."""
        return self.df
