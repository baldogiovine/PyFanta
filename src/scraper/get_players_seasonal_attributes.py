"""Module to fetch seasonal attributes of Serie A players"""

from dataclasses import dataclass, field
from typing import NamedTuple

import requests
from bs4 import BeautifulSoup

from src.utils import utils


class SeasonalStats(NamedTuple):
    """
    Represents seasonal statistics for a player.

    Attributes
    ----------
    played_matches : int
        The number of matches played by the player.
    goals : int
        The number of goals scored by the player.
    assists : int
        The number of assists made by the player.
    """

    played_matches: int
    goals: int
    assists: int


class OtherSeasonalStats(NamedTuple):
    """
    Represents additional seasonal statistics for a player.

    Attributes
    ----------
    goals_home_game : int
        The number of goals scored by the player in home games.
    goals_away_games : int
        The number of goals scored by the player in away games.
    penalties_scored : int
        The number of penalties scored by the player.
    penalties_shot : int
        The number of penalties taken by the player.
    penalties_ratio : float
        The ratio of penalties scored to penalties taken by the player.
    autogoals : int
        The number of own goals scored by the player.
    yellow_cards : int
        The number of yellow cards received by the player.
    red_cards : int
        The number of red cards received by the player.
    """

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
    """Class to scrape and manage Serie A player seasonal attributes from a given link.

    With seasonal attributes we indicate a player summary statics.
    No information about a specific match is provided, but are provided instead statics
    capable of summarazing a player season up to now.

    Attributes
    ----------
    link : str
        The URL link to the player's statistics page.

    Other Attributes
    ----------------
    soup : BeautifulSoup
        The BeautifulSoup object used to parse the HTML content.
    avg_grade : float
        The average grade of the player.
    avg_fanta_grade : float
        The average fantasy grade of the player.
    role : str
        The player's role.
    role_mantra : str
        The player's mantra role.
    played_matches : int
        The number of matches played by the player.
    goals : int
        The number of goals scored by the player.
    assists : int
        The number of assists made by the player.
    goals_home_game : int
        The number of goals scored by the player in home games.
    goals_away_games : int
        The number of goals scored by the player in away games.
    penalties_scored : int
        The number of penalties scored by the player.
    penalties_shot : int
        The number of penalties taken by the player.
    penalties_ratio : float
        The ratio of penalties scored to penalties taken by the player.
    autogoals : int
        The number of own goals scored by the player.
    yellow_cards : int
        The number of yellow cards received by the player.
    red_cards : int
        The number of red cards received by the player.
    team : str
        The team the player belongs to.
    description : str
        A description of the player.
    fanta_description : str
        A fantasy description of the player.
    """

    link: str
    soup: BeautifulSoup = field(init=False)
    avg_grade: float = field(init=False)
    avg_fanta_grade: float = field(init=False)
    role: str = field(init=False)
    role_mantra: str = field(init=False)
    played_matches: int = field(init=False)
    goals: int = field(init=False)
    assists: int = field(init=False)
    goals_home_game: int = field(init=False)
    goals_away_games: int = field(init=False)
    penalties_scored: int = field(init=False)
    penalties_shot: int = field(init=False)
    penalties_ratio: float = field(init=False)
    autogoals: int = field(init=False)
    yellow_cards: int = field(init=False)
    red_cards: int = field(init=False)
    team: str = field(init=False)
    description: str = field(init=False)
    fanta_description: str = field(init=False)

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

    def check_status_code(self, response: requests.Response) -> None:
        """Check the status code of the HTTP response."""
        if response.status_code != 200:
            raise ValueError("Requests status code different from 200")

    def get_avg_grade(self) -> float:
        """Get the average grade of the player."""
        value = self.soup.find("span", class_="badge badge-primary avg").text
        return utils.str_to_float(value)

    def get_avg_fanta_grade(self) -> float:
        """Get the average fantasy grade of the player."""
        value = self.soup.find("span", class_="badge badge-info avg").text
        return utils.str_to_float(value)

    def get_role(self) -> str:
        """Get the role of the player."""
        return self.soup.find("span", class_="role").get("title")

    def get_role_mantra(self) -> str:
        """Get the mantra role of the player."""
        return self.soup.find("span", class_="role role-mantra").get("title")

    def get_seasonal_stats(self) -> SeasonalStats:
        """Get seasonal stats of the player."""
        played_matches = int(self.soup.find_all("td", class_="value")[0].text)
        goals = int(self.soup.find_all("td", class_="value")[1].text)
        assists = int(self.soup.find_all("td", class_="value")[2].text)

        return SeasonalStats(played_matches, goals, assists)

    def get_other_seasonal_stats(self) -> OtherSeasonalStats:
        """Get other seasonal stats of the player."""
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
        """Get the team of the player."""
        return (
            self.soup.find_all("a", class_="team-name team-link")[0]
            .find("meta")
            .get("content")
        )

    def get_description(self) -> str:
        """Get the description of the player."""
        return self.soup.find("div", class_="description").text.strip()

    def get_fanta_description(self) -> str:
        """Get the fantasy description of the player."""
        text = self.soup.find("div", class_="card tipography").text.strip()
        return text[text.find("\n") + 1 :].strip()
