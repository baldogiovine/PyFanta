"""Module to fetch data regarding Serie A players"""

import uuid
from dataclasses import dataclass, field

import pandas as pd
import requests
from bs4 import BeautifulSoup

from src.utils import utils


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


@dataclass
class GetPlayersAttributes:
    link: str

    def __post_init__(self):
        self.html = requests.get(self.link, timeout=5)
        self.soup = BeautifulSoup(self.html.content, "lxml")
        self.avg_grade = self.get_avg_grade()
        self.avg_fanta_grade = self.get_avg_fanta_grade()

    def get_avg_grade(self) -> float:
        value = self.soup.find("span", class_="badge badge-primary avg").text
        return utils.str_to_float(value)

    def get_avg_fanta_grade(self) -> float:
        value = self.soup.find("span", class_="badge badge-info avg").text
        return utils.str_to_float(value)
