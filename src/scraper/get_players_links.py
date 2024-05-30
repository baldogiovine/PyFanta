"""Module to get players links. Links are necessary to scrape players data"""

import uuid
from dataclasses import dataclass, field

import pandas as pd
import requests
from bs4 import BeautifulSoup


@dataclass
class GetPlayersLinks:
    year: int
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
        base_link = "https://www.fantacalcio.it/quotazioni-fantacalcio"
        return f"{base_link}/{self.year}/"

    def check_status_code(self, response) -> None:
        if response.status_code != 200:
            raise ValueError("Requests status code different from 200")

    def get_links(self) -> "GetPlayersLinks":
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
        self.df["player_id"] = [str(uuid.uuid4()) for _ in range(len(self.df))]
        return self

    def save_csv(self) -> None:
        self.df.to_csv(f"data/players_links_{self.year}.csv", index=False)

    def get_dataframe(self) -> pd.DataFrame:
        return self.df
