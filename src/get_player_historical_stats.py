"""Module to get players historical stats."""

from dataclasses import dataclass, field
from typing import List

import requests
from bs4 import BeautifulSoup

from src.utils import utils


@dataclass
class GetPlayersHistoricalStats:
    player_link: str
    year: int
    soup: BeautifulSoup = field(init=False)
    game_day: List[int] = field(init=False, default_factory=list)
    grade: List[float] = field(init=False, default_factory=list)
    fanta_grade: List[float] = field(init=False, default_factory=list)
    bonus: List[float] = field(init=False, default_factory=list)
    malus: List[float] = field(init=False, default_factory=list)
    home_team: List[str] = field(init=False, default_factory=list)
    match_score: List[str] = field(init=False, default_factory=list)
    away_team: List[str] = field(init=False, default_factory=list)
    minute_in: List[float] = field(init=False, default_factory=list)
    minute_out: List[float] = field(init=False, default_factory=list)

    def __post_init__(self):
        self.url = self.get_full_url()
        response = requests.get(self.url, timeout=5)
        self.check_status_code(response)
        self.soup = BeautifulSoup(response.content, "lxml")
        self.game_day = self.get_game_day()
        self.grade = self.get_grade()
        self.fanta_grade = self.get_fanta_grade()
        self.bonus = self.get_bonus()
        self.malus = self.get_malus()
        self.home_team = self.get_home_team()
        self.match_score = self.get_match_score()
        self.away_team = self.get_away_team()
        self.minute_in = self.get_minute_in()
        self.minute_out = self.get_minute_out()

    def get_full_url(self) -> str:
        return f"{self.player_link}/{self.year}/"

    def check_status_code(self, response: requests.Response) -> None:
        if response.status_code != 200:
            raise ValueError("Requests status code different from 200")

    def get_game_day(self) -> List[int]:
        return list(range(1, 39))

    def get_grade(self) -> list[float]:
        return [
            utils.str_to_float(span.get("data-value"))
            for span in self.soup.find_all("span", class_="grade")
        ]

    def get_fanta_grade(self) -> List[float]:
        return [
            utils.str_to_float(span.get("data-value"))
            for span in self.soup.find_all("span", class_="fanta-grade")
        ]

    def get_bonus(self) -> List[float]:
        return [
            utils.str_to_float(span.get("data-primary-value"))
            for span in self.soup.find_all("div", class_="x-axis")[1].find_all("span")
        ]

    def get_malus(self) -> List[float]:
        return [
            utils.str_to_float(span.get("data-secondary-value"))
            for span in self.soup.find_all("div", class_="x-axis")[1].find_all("span")
        ]

    def get_home_team(self) -> List[str]:
        return [
            span.text.strip() for span in self.soup.find_all("span", class_="team-home")
        ][:-2]  # [:-2] removes two inexisting matches

    def get_match_score(self) -> List[str]:
        return [
            span.text.strip()
            for span in self.soup.find_all("span", class_="match-score")
        ]

    def get_away_team(self) -> List[str]:
        return [
            span.text.strip() for span in self.soup.find_all("span", class_="team-away")
        ][:-2]  # [:-2] removes two inexisting matches

    def get_minute_in(self) -> List[float]:
        return [
            utils.empty_to_nan(span.get("data-minute"))
            for span in self.soup.find_all("span", class_="sub-in")
        ]

    def get_minute_out(self) -> List[float]:
        return [
            utils.empty_to_nan(span.get("data-minute"))
            for span in self.soup.find_all("span", class_="sub-out")
        ]
