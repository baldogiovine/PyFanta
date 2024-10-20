"""Module to get players historical stats."""

import asyncio
from typing import List, Tuple, Union

import aiohttp
from bs4 import BeautifulSoup
from bs4.element import Tag

from src.api.models import PlayerLink
from src.scraper import utils
from src.scraper.exceptions import FetchError, PageStructureError
from src.scraper.utils import check_for_soup


class GetMatchesStats:
    """Class to get players' match stats."""

    def __init__(self, player_link: PlayerLink):  # noqa: D107
        self.name: str = str(player_link.name)
        self.url: str = str(player_link.link)
        self.soup: Union[BeautifulSoup, None] = None
        self.game_day: Union[List[int], None] = None
        self.grade: Union[List[Union[float, None]], None] = None
        self.fanta_grade: Union[List[Union[float, None]], None] = None
        self.bonus: Union[List[Union[float, None]], None] = None
        self.malus: Union[List[Union[float, None]], None] = None
        self.home_team: Union[List[str], None] = None
        self.guest_team: Union[List[str], None] = None
        self.home_team_score: Union[List[int], None] = None
        self.guest_team_score: Union[List[int], None] = None
        self.sub_in: Union[List[Union[float, None]], None] = None
        self.sub_out: Union[List[Union[float, None]], None] = None

    async def fetch_page(self) -> None:
        """Asynchronously fetch the page content and parse it with BeautifulSoup."""
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

    def get_game_day(self) -> List[int]:
        """Gets game days.

        Returns:
        -------
        List[int]
            List of game days.
        """
        self.game_day = list(range(1, 39))

        return self.game_day

    @check_for_soup
    async def get_grade(self) -> list[Union[float, None]]:
        """Gets the real grade obtained by a player.

        Returns:
        -------
        list[float]
            List of grades.
        """
        grades: List[Union[float, None]] = []
        assert isinstance(self.soup, BeautifulSoup)
        for span in self.soup.find_all("span", class_="grade"):
            grade: Union[float, None] = utils.str_to_float(
                str_to_replace=span.get("data-value")
            )
            assert isinstance(grade, float) or grade is None
            grades.append(grade)
        self.grade = grades

        return self.grade

    @check_for_soup
    async def get_fanta_grade(self) -> list[Union[float, None]]:
        """Gets the fanta grade obtained by a player.

        Fanta grade is calculated based on the real grade summed with bonuses and
        maluses.

        Returns:
        -------
        list[float]
            List of grades.
        """
        fanta_grades: List[Union[float, None]] = []
        assert isinstance(self.soup, BeautifulSoup)
        for span in self.soup.find_all("span", class_="fanta-grade"):
            fanta_grade: Union[float, None] = utils.str_to_float(
                str_to_replace=span.get("data-value")
            )
            assert isinstance(fanta_grade, float) or fanta_grade is None
            fanta_grades.append(fanta_grade)
        self.fanta_grade = fanta_grades

        return self.fanta_grade

    @check_for_soup
    async def get_bonus(self) -> List[Union[float, None]]:
        """Gets the (eventual) bonus obtained by a player.

        Returns:
        -------
        list[float]
            List of grades.
        """
        bonus: List[Union[float, None]] = []
        assert isinstance(self.soup, BeautifulSoup)
        x_axis_list: List[Tag] = self.soup.find_all("div", class_="x-axis")
        if len(x_axis_list) > 1:
            x_axis: Tag = x_axis_list[1]
            if not isinstance(x_axis, Tag):
                raise PageStructureError("Expected a Tag object for x_axis.")
        else:
            raise PageStructureError(
                """Expected at least two 'div' elements with class 'x-axis',
                but found fewer."""
            )
        for span in x_axis.find_all("span"):
            one_bonus = utils.str_to_float(
                str_to_replace=span.get("data-primary-value")
            )
            assert isinstance(one_bonus, float) or one_bonus is None
            bonus.append(one_bonus)
        self.bonus = bonus

        return self.bonus

    @check_for_soup
    async def get_malus(self) -> List[Union[float, None]]:
        """Gets the (eventual) malus obtained by a player.

        Returns:
        -------
        list[float]
            List of grades.
        """
        malus: List[Union[float, None]] = []
        assert isinstance(self.soup, BeautifulSoup)
        x_axis_list: List[Tag] = self.soup.find_all("div", class_="x-axis")
        if len(x_axis_list) > 1:
            x_axis: Tag = x_axis_list[1]
            if not isinstance(x_axis, Tag):
                raise PageStructureError("Expected a Tag object for x_axis.")
        else:
            raise PageStructureError(
                """Expected at least two 'div' elements with class 'x-axis',
                but found fewer."""
            )
        for span in x_axis.find_all("span"):
            one_malus = utils.str_to_float(
                str_to_replace=span.get("data-secondary-value")
            )
            assert isinstance(one_malus, float) or one_malus is None
            malus.append(one_malus)
        self.malus = malus

        return self.malus

    @check_for_soup
    async def get_home_team(self) -> List[str]:
        """Gets the name of the hosting team.

        Returns:
        -------
        List[str]
            List of guest teams.
        """
        home_teams: List[str] = []
        assert isinstance(self.soup, BeautifulSoup)
        for span in self.soup.find_all("span", class_="team-home")[
            :-2
        ]:  # [:-2] removes two inexisting matches
            assert isinstance(span, Tag)
            home_team: str = span.text.strip()
            assert isinstance(home_team, str)
            home_teams.append(home_team)
        self.home_team = home_teams

        return self.home_team

    @check_for_soup
    async def get_guest_team(self) -> List[str]:
        """Gets the name of the guest team.

        Returns:
        -------
        List[str]
            List of guest teams.
        """
        guest_teams: List[str] = []
        assert isinstance(self.soup, BeautifulSoup)
        for span in self.soup.find_all("span", class_="team-home")[
            :-2
        ]:  # [:-2] removes two inexisting matches
            assert isinstance(span, Tag)
            guest_team: str = span.text.strip()
            assert isinstance(guest_team, str)
            guest_teams.append(guest_team)
        self.guest_team = guest_teams

        return self.guest_team

    @check_for_soup
    async def get_match_score(self) -> Tuple[List[int], List[int]]:
        """Gets matches' scores.

        Returns:
        -------
        Tuple[List[int], List[int]]

            1. List of match scores of the home team.
            2. List of match scores of the guest team.
        """
        home_team_scores: List[int] = []
        guest_team_scores: List[int] = []
        assert isinstance(self.soup, BeautifulSoup)
        for span in self.soup.find_all("span", class_="match-score")[:-2]:
            assert isinstance(span, Tag)
            match_score: str = span.text.strip()
            assert isinstance(match_score, str)
            home_team_score_str, guest_team_score_str = match_score.split("-")
            home_team_score = int(home_team_score_str)
            guest_team_score = int(guest_team_score_str)
            assert isinstance(home_team_score, int) and isinstance(
                guest_team_score, int
            )
            home_team_scores.append(home_team_score)
            guest_team_scores.append(guest_team_score)
        self.home_team_score = home_team_scores
        self.guest_team_score = guest_team_scores

        return self.home_team_score, self.guest_team_score

    @check_for_soup
    async def get_minute_in(self) -> List[Union[float, None]]:
        """Gets minute a player entered the field as a substitution.

        If `np.nan` it can mean that the player started as a starting player or that
        he didn' t play at all. But looking if a fantagrade is available will tell you
        if the player played or not.

        Returns:
        -------
        List[int]
            List of minutues a player entered the field as a substitution.
        """
        subs_in: List[Union[float, None]] = []
        assert isinstance(self.soup, BeautifulSoup)
        for span in self.soup.find_all("span", class_="sub-in"):
            sub_in: Union[float, None] = utils.empty_to_none(
                value=span.get("data-minute")
            )
            assert isinstance(sub_in, float) or sub_in is None
            subs_in.append(sub_in)
        self.sub_in = subs_in

        return self.sub_in

    @check_for_soup
    async def get_minute_out(self) -> List[Union[float, None]]:
        """Gets minute a player exited the field as a substitution.

        If `np.nan` it can mean that a player never exited the field or that
        he didn' t play at all. But looking if a fantagrade is available will tell you
        if the player played or not.

        Returns:
        -------
        List[int]
            List of minutues a player exited the field as a substitution.
        """
        subs_out: List[Union[float, None]] = []
        assert isinstance(self.soup, BeautifulSoup)
        for span in self.soup.find_all("span", class_="sub-in"):
            sub_out: Union[float, None] = utils.empty_to_none(
                value=span.get("data-minute")
            )
            assert isinstance(sub_out, float) or sub_out is None
            subs_out.append(sub_out)
        self.sub_out = subs_out

        return self.sub_out
