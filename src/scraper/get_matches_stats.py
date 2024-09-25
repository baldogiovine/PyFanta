"""Module to get players historical stats."""

import asyncio
from functools import wraps
from typing import Any, Awaitable, Callable, List, Tuple, TypeVar, Union

import aiohttp
from bs4 import BeautifulSoup
from bs4.element import Tag

from src.scraper import utils
from src.scraper.exceptions import FetchError, PageStructureError


class GetMatchesStats:
    """Docstring."""

    def __init__(self, url: str):  # noqa: D107
        self.__url: str = url
        self.__soup: Union[BeautifulSoup, None] = None
        self.__game_day: Union[List[int], None] = None
        self.__grade: Union[List[float], None] = None
        self.__fanta_grade: Union[List[float], None] = None
        self.__bonus: Union[List[float], None] = None
        self.__malus: Union[List[float], None] = None
        self.__home_team: Union[List[str], None] = None
        self.__guest_team: Union[List[str], None] = None
        self.__home_team_score: Union[List[int], None] = None
        self.__guest_team_score: Union[List[int], None] = None
        self.__sub_in: Union[List[float], None] = None
        self.__sub_out: Union[List[float], None] = None

    async def __fetch_page(self) -> None:
        """Asynchronously fetch the page content and parse it with BeautifulSoup."""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.__url, timeout=5) as response:
                    response.raise_for_status()
                    content: bytes = await response.read()
                    self.__soup = BeautifulSoup(content, "lxml")
        except aiohttp.ClientError as e:
            raise FetchError(f"Error fetching URL {self.__url}: {e}") from e
        except asyncio.TimeoutError as te:
            raise FetchError(f"Request to {self.__url} timed out.") from te

    F = TypeVar("F", bound=Callable[..., Awaitable[Any]])

    @staticmethod
    def __check_for_soup(func: F) -> F:
        @wraps(func)
        async def wrapper(self, *args, **kwargs) -> Any:  # type: ignore
            if not self.__soup:
                await self.__fetch_page()
            try:
                return await func(self, *args, **kwargs)
            except AttributeError as e:
                raise PageStructureError(
                    "Unexpected page structure while extracting data."
                ) from e

        return wrapper  # type: ignore

    def __get_game_day(self) -> List[int]:
        """Gets game days.

        Returns:
        -------
        List[int]
            List of game days.
        """
        self.__game_day = list(range(1, 39))

        return self.__game_day

    @__check_for_soup
    async def __get_grade(self) -> list[float]:
        """Gets the real grade obtained by a player.

        Returns:
        -------
        list[float]
            List of grades.
        """
        grades: List[float] = []
        assert isinstance(self.__soup, BeautifulSoup)
        for span in self.__soup.find_all("span", class_="grade"):
            grade: float = utils.str_to_float(str_to_replace=span.get("data-value"))
            assert isinstance(grade, float)
            grades.append(grade)
        self.__grade = grades

        return self.__grade

    @__check_for_soup
    async def __get_fanta_grade(self) -> list[float]:
        """Gets the fanta grade obtained by a player.

        Fanta grade is calculated based on the real grade summed with bonuses and
        maluses.

        Returns:
        -------
        list[float]
            List of grades.
        """
        fanta_grades: List[float] = []
        assert isinstance(self.__soup, BeautifulSoup)
        for span in self.__soup.find_all("span", class_="fanta-grade"):
            fanta_grade: float = utils.str_to_float(
                str_to_replace=span.get("data-value")
            )
            assert isinstance(fanta_grade, float)
            fanta_grades.append(fanta_grade)
        self.__fanta_grade = fanta_grades

        return self.__fanta_grade

    @__check_for_soup
    async def __get_bonus(self) -> List[float]:
        """Gets the (eventual) bonus obtained by a player.

        Returns:
        -------
        list[float]
            List of grades.
        """
        bonus: List[float] = []
        assert isinstance(self.__soup, BeautifulSoup)
        x_axis_list: List[Tag] = self.__soup.find_all("div", class_="x-axis")
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
            assert isinstance(one_bonus, float)
            bonus.append(one_bonus)
        self.__bonus = bonus

        return self.__bonus

    @__check_for_soup
    async def __get_malus(self) -> List[float]:
        """Gets the (eventual) malus obtained by a player.

        Returns:
        -------
        list[float]
            List of grades.
        """
        malus: List[float] = []
        assert isinstance(self.__soup, BeautifulSoup)
        x_axis_list: List[Tag] = self.__soup.find_all("div", class_="x-axis")
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
            assert isinstance(one_malus, float)
            malus.append(one_malus)
        self.__malus = malus

        return self.__malus

    @__check_for_soup
    async def __get_home_team(self) -> List[str]:
        """Gets the name of the hosting team.

        Returns:
        -------
        List[str]
            List of guest teams.
        """
        home_teams: List[str] = []
        assert isinstance(self.__soup, BeautifulSoup)
        for span in self.__soup.find_all("span", class_="team-home")[
            :-2
        ]:  # [:-2] removes two inexisting matches
            assert isinstance(span, Tag)
            home_team: str = span.text.strip()
            assert isinstance(home_team, str)
            home_teams.append(home_team)
        self.__home_team = home_teams

        return self.__home_team

    @__check_for_soup
    async def __get_guest_team(self) -> List[str]:
        """Gets the name of the guest team.

        Returns:
        -------
        List[str]
            List of guest teams.
        """
        guest_teams: List[str] = []
        assert isinstance(self.__soup, BeautifulSoup)
        for span in self.__soup.find_all("span", class_="team-home")[
            :-2
        ]:  # [:-2] removes two inexisting matches
            assert isinstance(span, Tag)
            guest_team: str = span.text.strip()
            assert isinstance(guest_team, str)
            guest_teams.append(guest_team)
        self.__guest_team = guest_teams

        return self.__guest_team

    @__check_for_soup
    async def __get_match_score(self) -> Tuple[List[int], List[int]]:
        """Gets matches' scores.

        Returns:
        -------
        Tuple[List[int], List[int]]

            1. List of match scores of the home team.
            2. List of match scores of the guest team.
        """
        home_team_scores: List[int] = []
        guest_team_scores: List[int] = []
        assert isinstance(self.__soup, BeautifulSoup)
        for span in self.__soup.find_all("span", class_="match-score")[:-2]:
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
        self.__home_team_score = home_team_scores
        self.__guest_team_score = guest_team_scores

        return self.__home_team_score, self.__guest_team_score

    @__check_for_soup
    async def __get_minute_in(self) -> List[float]:
        """Gets minute a player entered the field as a substitution.

        If `np.nan` it can mean that the player started as a starting player or that
        he didn' t play at all. But looking if a fantagrade is available will tell you
        if the player played or not.

        Returns:
        -------
        List[int]
            List of minutues a player entered the field as a substitution.
        """
        subs_in: List[float] = []
        assert isinstance(self.__soup, BeautifulSoup)
        for span in self.__soup.find_all("span", class_="sub-in"):
            sub_in: float = utils.empty_to_nan(value=span.get("data-minute"))
            assert isinstance(sub_in, float)
            subs_in.append(sub_in)
        self.__sub_in = subs_in

        return self.__sub_in

    @__check_for_soup
    async def __get_minute_out(self) -> List[float]:
        """Gets minute a player exited the field as a substitution.

        If `np.nan` it can mean that a player never exited the field or that
        he didn' t play at all. But looking if a fantagrade is available will tell you
        if the player played or not.

        Returns:
        -------
        List[int]
            List of minutues a player exited the field as a substitution.
        """
        subs_out: List[float] = []
        assert isinstance(self.__soup, BeautifulSoup)
        for span in self.__soup.find_all("span", class_="sub-in"):
            sub_out: float = utils.empty_to_nan(value=span.get("data-minute"))
            assert isinstance(sub_out, float)
            subs_out.append(sub_out)
        self.__sub_out = subs_out

        return self.__sub_out
