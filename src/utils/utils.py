"""Module to define some general utility functions"""


def str_to_float(str_to_replace: str) -> float:
    """Converts a string with a comma as the decimal separator to a float."""
    return float(str_to_replace.replace(",", "."))
