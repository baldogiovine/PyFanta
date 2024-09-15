"""Router to get players links. Links are necessary to scrape players data."""

from fastapi import APIRouter, HTTPException

from src.scraping import GetPlayersLinks

router = APIRouter()


@router.get("/players-links/{year}")
def get_players_links(year: str):
    """Endpoint to get player links for a specified year."""
    try:
        scraper = GetPlayersLinks(year=year)
        scraper.get_links()
        return {"data": scraper.data}
    except ValueError as ve:
        # Handle specific error if the request fails
        raise HTTPException(status_code=400, detail=str(ve)) from ve
    except Exception as e:
        # General exception handler
        raise HTTPException(
            status_code=500, detail="An error occurred while processing the request."
        ) from e
