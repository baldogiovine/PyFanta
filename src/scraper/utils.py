"""Module to define some general utility functions."""

from functools import wraps
from typing import Any, Awaitable, Callable, TypeVar, Union

from src.scraper.exceptions import PageStructureError


def str_to_float(str_to_replace: str) -> Union[float, None]:
    """Converts a string with a comma as the decimal separator to a float."""
    if str_to_replace is None or str_to_replace == "":
        return None
    else:
        return float(str_to_replace.replace(",", "."))


def safe_zero_division(
    numerator: Union[int, float],
    denominator: Union[int, float],
) -> Union[float, None]:
    """Safely divides two numbers and handles division by zero.

    Parameters
    ----------
    numerator : Union[int, float]
        The numerator of the division.
    denominator : Union[int, float]
        The denominator of the division.

    Returns:
    -------
    Optional[float]
        The result of the division, or None if division by zero occurs.
    """
    try:
        result = numerator / denominator
        result = round(result, 2)
        assert isinstance(result, float)
    except ZeroDivisionError:
        result = None
    return result


def empty_to_none(value: str) -> Union[float, None]:
    """Transforms empty strings to `None`, therefore to a float."""
    if value is None or value == "":
        return None
    else:
        return float(value)


F = TypeVar("F", bound=Callable[..., Awaitable[Any]])


def check_for_soup(func: F) -> F:
    """Decorator that ensures the BeautifulSoup object is initialized before
    executing the decorated method.

    Parameters
    ----------
    func : Callable[..., Awaitable[Any]]
        The asynchronous method to be decorated.

    Returns:
    -------
    Callable[..., Awaitable[Any]]
        The wrapped asynchronous method with pre-execution checks.
    """  # noqa: D205

    @wraps(func)
    async def wrapper(self, *args, **kwargs) -> Any:  # type: ignore
        if not self.soup:
            await self.fetch_page()
        try:
            return await func(self, *args, **kwargs)
        except AttributeError as e:
            raise PageStructureError(
                "Unexpected page structure while extracting data."
            ) from e

    return wrapper  # type: ignore
