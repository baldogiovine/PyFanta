"""Module to define some general utility functions"""

from typing import Optional, Union


def str_to_float(str_to_replace: str) -> float:
    """Converts a string with a comma as the decimal separator to a float."""
    return float(str_to_replace.replace(",", "."))


def safe_zero_division(
    numerator: Union[int, float],
    denominator: Union[int, float],
) -> Optional[float]:
    """Safely divides two numbers and handles division by zero.

    Parameters
    ----------
    numerator : Union[int, float]
        The numerator of the division.
    denominator : Union[int, float]
        The denominator of the division.

    Returns
    -------
    Optional[float]
        The result of the division, or None if division by zero occurs.
    """
    try:
        result = numerator / denominator
        result = round(result, 2)
    except ZeroDivisionError:
        result = None
    return result
