"""Router to get players links. Links are necessary to scrape players data."""

from typing import Dict, List, no_type_check

from src.api.main import app
from src.api.models import PlayersLinksResponse
from src.scraper.get_players_links import GetPlayersLinks


@app.get(
    "/players-links/{year}",
    response_model=PlayersLinksResponse,
)
@no_type_check
async def get_players_links(year: str) -> List[Dict[str, str]]:
    """Endpoint to get players' names and links for a specified year.

    Parameters
    ----------
    year : str
        The year for which player links are to be fetched, e.g., "2023-24", "2022-23".

    Returns:
    -------
    List[Dict[str, str]]
        List of dictionaries containing players' names and links.
    """
    scraper = GetPlayersLinks(year=year)
    data: List[Dict[str, str]] = await scraper.get_links()
    return {"data": data}
