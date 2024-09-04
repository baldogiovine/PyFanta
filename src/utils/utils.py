"""Module to define some general utility functions"""

from typing import Union

import numpy as np


def str_to_float(str_to_replace: str) -> float:
    """Converts a string with a comma as the decimal separator to a float."""
    if str_to_replace == "":
        return np.nan
    else:
        return float(str_to_replace.replace(",", "."))


def safe_zero_division(
    numerator: Union[int, float],
    denominator: Union[int, float],
) -> float:
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
        result = np.nan
    return result


def empty_to_nan(value: str) -> float:
    if value == "":
        value = np.nan
    else:
        pass
    return float(value)
