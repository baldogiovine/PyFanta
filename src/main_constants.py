"""Module to define constants to use in main.py."""


class MainConstants:
    """Class to define constants to use in main.py."""

    BASE_URL: str = "http://127.0.0.1:8000"

    # get_players_link endpoint
    year: str = "2023-24"
    get_players_link_endpoint: str = f"{BASE_URL}/players-links/{year}"
