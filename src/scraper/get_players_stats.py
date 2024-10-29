"""Module to get players' stats."""

import asyncio
from typing import NamedTuple, Union

import aiohttp
from bs4 import BeautifulSoup
from bs4.element import ResultSet, Tag

from src.api.models import PlayerLink
from src.scraper import utils
from src.scraper.exceptions import FetchError
from src.scraper.utils import check_for_soup


class GradedMatchesGoalsAssistsTuple(NamedTuple):
    """NamedTuple.

    Where:
    - [0] = graded_matches: int
    - [1] = goals: int
    - [2] = assists: int
    """

    graded_matches: int
    goals: int
    assists: int


class GoalsInfoPenaltiesInfoCardsInfoTuple(NamedTuple):
    """NamedTuple.

    Where:
    - [0] = home_game_goals: int
    - [1] = away_game_goals: int
    - [2] = penalties_scored: int
    - [3] = penalties_shot: int
    - [4] = penalties_ratio: Union[float, None]
    - [5] = autogoals: int
    - [6] = yellow_cards: int
    - [7] = red_cards: int
    """

    home_game_goals: int
    away_game_goals: int
    penalties_scored: int
    penalties_shot: int
    penalties_ratio: Union[float, None]
    autogoals: int
    yellow_cards: int
    red_cards: int


class GetPlayerSummaryStats:
    """Class to scrpae a player summary statistics in a specific seasons."""

    def __init__(self, player_link: PlayerLink):  # noqa: D107
        self.name: str = str(player_link.name)
        self.url: str = str(player_link.link)
        self.soup: Union[BeautifulSoup, None] = None
        self.avg_grade: Union[float, None] = None
        self.avg_fanta_grade: Union[float, None] = None
        self.role: Union[str, None] = None
        self.mantra_role: Union[str, None] = None
        self.graded_matches: Union[int, None] = None
        self.goals: Union[int, None] = None
        self.assists: Union[int, None] = None
        self.home_game_goals: Union[int, None] = None
        self.away_game_goals: Union[int, None] = None
        self.penalties_scored: Union[int, None] = None
        self.penalties_shot: Union[int, None] = None
        self.penalties_ratio: Union[float, None] = None
        self.autogoals: Union[int, None] = None
        self.yellow_cards: Union[int, None] = None
        self.red_cards: Union[int, None] = None
        self.team: Union[str, None] = None
        self.description: Union[str, None] = None

    async def fetch_page(self) -> None:  # FIXME: it repeated from GetMatchesStats
        """Asynchronously fetches the page content and parse it with BeautifulSoup."""
        try:
            async with aiohttp.ClientSession() as session:
                assert isinstance(self.url, str)
                async with session.get(self.url, timeout=5) as response:
                    response.raise_for_status()
                    content: bytes = await response.read()
                    self.soup = BeautifulSoup(content, "lxml")
        except aiohttp.ClientError as e:
            raise FetchError(f"Error fetching URL {self.url}: {e}") from e
        except asyncio.TimeoutError as te:
            raise FetchError(f"Request to {self.url} timed out.") from te

    @check_for_soup
    async def get_avg_grade(self) -> Union[float, None]:
        """Gets the average grade."""
        assert isinstance(self.soup, BeautifulSoup)
        span: str = self.soup.find("span", class_="badge badge-primary avg").text
        assert isinstance(span, str)
        avg_grade: Union[float, None] = utils.str_to_none(span)
        assert isinstance(avg_grade, float) or avg_grade is None
        self.avg_grade = avg_grade

        return self.avg_grade

    @check_for_soup
    async def get_avg_fanta_grade(self) -> Union[float, None]:
        """Gets the average fanta grade."""
        assert isinstance(self.soup, BeautifulSoup)
        span: str = self.soup.find("span", class_="badge badge-primary avg").text
        assert isinstance(span, str)
        avg_fanta_grade: Union[float, None] = utils.str_to_none(span)
        assert isinstance(avg_fanta_grade, float) or avg_fanta_grade is None
        self.avg_fanta_grade = avg_fanta_grade

        return self.avg_fanta_grade

    @check_for_soup
    async def get_role(self) -> str:
        """Gets the role of the player."""
        assert isinstance(self.soup, BeautifulSoup)
        span: Tag = self.soup.find("span", class_="role")
        assert isinstance(span, Tag)
        role: str = span.get("title")
        assert isinstance(role, str)
        self.role = role

        return self.role

    @check_for_soup
    async def get_mantra_role(self) -> str:
        """Gets the role of the player."""
        assert isinstance(self.soup, BeautifulSoup)
        span: Tag = self.soup.find("span", class_="role role-mantra")
        assert isinstance(span, Tag)
        mantra_role: str = span.get("title")
        assert isinstance(mantra_role, str)
        self.mantra_role = mantra_role

        return self.mantra_role

    @check_for_soup
    async def get_graded_matches_goals_assists(self) -> GradedMatchesGoalsAssistsTuple:
        """Gets graded matches, goals, and assists."""
        assert isinstance(self.soup, BeautifulSoup)
        td: ResultSet[Tag] = self.soup.find_all("td", class_="value")
        assert isinstance(td, ResultSet)

        graded_matches = int(td[0].text)
        assert isinstance(graded_matches, int)
        self.graded_matches = graded_matches

        goals = int(td[1].text)
        assert isinstance(goals, int)
        self.goals = goals

        assists = int(td[2].text)
        assert isinstance(assists, int)
        self.assists = assists

        return GradedMatchesGoalsAssistsTuple(
            self.graded_matches,
            self.goals,
            self.assists,
        )

    @check_for_soup
    async def get_goals_info_penalties_info_cards_info(
        self,
    ) -> GoalsInfoPenaltiesInfoCardsInfoTuple:
        """Gets information about goals, penalties, autogoals, and cards."""
        assert isinstance(self.soup, BeautifulSoup)
        span: ResultSet[Tag] = self.soup.find_all("span", class_="pill")
        assert isinstance(span, ResultSet)

        home_game_goals, away_game_goals = span[0].text.split("/")
        assert isinstance(home_game_goals, str)
        assert isinstance(away_game_goals, str)
        home_game_goals = int(home_game_goals)
        assert isinstance(home_game_goals, int)
        self.home_game_goals = home_game_goals
        away_game_goals = int(away_game_goals)
        assert isinstance(away_game_goals, int)
        self.away_game_goals = away_game_goals

        penalties_scored, penalties_shot = span[2].text.split("/")
        assert isinstance(penalties_scored, str)
        assert isinstance(penalties_shot, str)
        penalties_scored = int(penalties_scored)
        assert isinstance(penalties_scored, int)
        self.penalties_scored = penalties_scored
        penalties_shot = int(penalties_shot)
        assert isinstance(penalties_shot, int)
        self.penalties_shot = penalties_shot
        penalties_ratio: Union[float, None] = utils.safe_zero_division(
            numerator=penalties_scored,
            denominator=penalties_shot,
        )
        assert isinstance(penalties_ratio, float) or penalties_ratio is None
        self.penalties_ratio = penalties_ratio

        autogoals: int = int(span[4].text)
        assert isinstance(autogoals, int)
        self.autogoals = autogoals

        yellow_cards: int = int(span[1].text)
        assert isinstance(yellow_cards, int)
        self.yellow_cards = yellow_cards
        red_cards: int = int(span[3].text)
        assert isinstance(red_cards, int)
        self.red_cards = red_cards

        return GoalsInfoPenaltiesInfoCardsInfoTuple(
            home_game_goals,
            away_game_goals,
            penalties_scored,
            penalties_shot,
            penalties_ratio,
            autogoals,
            yellow_cards,
            red_cards,
        )

    @check_for_soup
    async def get_team(self) -> str:
        """Get team of the player."""
        assert isinstance(self.soup, BeautifulSoup)
        a: ResultSet[Tag] = self.soup.find_all("a", class_="team-name team-link")
        assert isinstance(a, ResultSet)
        first_tag: Tag = a[0]
        assert isinstance(first_tag, Tag)
        meta: Tag = first_tag.find("meta")
        assert isinstance(meta, Tag)
        team: str = meta.get("content")
        assert isinstance(team, str)
        self.team = team

        return self.team

    @check_for_soup
    async def get_description(self) -> str:
        """Get  description of the player."""
        assert isinstance(self.soup, BeautifulSoup)
        div: Tag = self.soup.find("div", class_="description")
        assert isinstance(div, Tag)
        description: str = div.text.strip()
        assert isinstance(description, str)
        self.description = description

        return self.description
