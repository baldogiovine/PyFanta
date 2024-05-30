"""Module to fetch seasonal attributes of Serie A players"""

from dataclasses import dataclass
from typing import NamedTuple

import requests
from bs4 import BeautifulSoup

from src.utils import utils


class SeasonalStats(NamedTuple):
    played_matches: int
    goals: int
    assists: int


class OtherSeasonalStats(NamedTuple):
    goals_home_game: int
    goals_away_games: int
    penalties_scored: int
    penalties_shot: int
    penalties_ratio: float
    autogoals: int
    yellow_cards: int
    red_cards: int


@dataclass
class GetPlayersAttributes:
    link: str

    def __post_init__(self):
        response = requests.get(self.link, timeout=5)
        self.check_status_code(response)
        self.soup = BeautifulSoup(response.content, "lxml")
        self.avg_grade = self.get_avg_grade()
        self.avg_fanta_grade = self.get_avg_fanta_grade()
        self.role = self.get_role()
        self.role_mantra = self.get_role_mantra()
        self.played_matches, self.goals, self.assists = self.get_seasonal_stats()
        (
            self.goals_home_game,
            self.goals_away_games,
            self.penalties_scored,
            self.penalties_shot,
            self.penalties_ratio,
            self.autogoals,
            self.yellow_cards,
            self.red_cards,
        ) = self.get_other_seasonal_stats()
        self.team = self.get_team()
        self.description = self.get_description()
        self.fanta_description = self.get_fanta_description()

    def check_status_code(self, response) -> None:
        if response.status_code != 200:
            raise ValueError("Requests status code different from 200")

    def get_avg_grade(self) -> float:
        value = self.soup.find("span", class_="badge badge-primary avg").text
        return utils.str_to_float(value)

    def get_avg_fanta_grade(self) -> float:
        value = self.soup.find("span", class_="badge badge-info avg").text
        return utils.str_to_float(value)

    def get_role(self) -> str:
        return self.soup.find("span", class_="role").get("title")

    def get_role_mantra(self) -> str:
        return self.soup.find("span", class_="role role-mantra").get("title")

    def get_seasonal_stats(self) -> SeasonalStats:
        played_matches = int(self.soup.find_all("td", class_="value")[0].text)
        goals = int(self.soup.find_all("td", class_="value")[1].text)
        assists = int(self.soup.find_all("td", class_="value")[2].text)

        return SeasonalStats(played_matches, goals, assists)

    def get_other_seasonal_stats(self) -> OtherSeasonalStats:
        goals_home_game, goals_away_games = self.soup.find_all("span", class_="pill")[
            0
        ].text.split("/")
        goals_home_game = int(goals_home_game)
        goals_away_games = int(goals_away_games)

        penalties_scored, penalties_shot = self.soup.find_all("span", class_="pill")[
            2
        ].text.split("/")
        penalties_scored = int(penalties_scored)
        penalties_shot = int(penalties_shot)
        penalties_ratio = utils.safe_zero_division(
            numerator=penalties_scored,
            denominator=penalties_shot,
        )

        autogoals = int(self.soup.find_all("span", class_="pill")[4].text)

        yellow_cards = int(self.soup.find_all("span", class_="pill")[1].text)
        red_cards = int(self.soup.find_all("span", class_="pill")[3].text)

        return OtherSeasonalStats(
            goals_home_game,
            goals_away_games,
            penalties_scored,
            penalties_shot,
            penalties_ratio,
            autogoals,
            yellow_cards,
            red_cards,
        )

    def get_team(self) -> str:
        return (
            self.soup.find_all("a", class_="team-name team-link")[0]
            .find("meta")
            .get("content")
        )

    def get_description(self) -> str:
        return self.soup.find("div", class_="description").text.strip()

    def get_fanta_description(self) -> str:
        text = self.soup.find("div", class_="card tipography").text.strip()
        return text[text.find("\n") + 1 :].strip()
