"""Main API module."""

from typing import no_type_check

from fastapi import FastAPI

from src.api.exceptions import register_exception_handlers
from src.api.routers.links_router import router as links_router
from src.api.routers.matches_router import router as matches_router

app = FastAPI(
    title="Players API",
    description="An API to get players' information for the fantacalcio.",
    version="1.0.0",
)

# Include routers
app.include_router(links_router)
app.include_router(matches_router)

# Register exception handlers
register_exception_handlers(app=app)


@app.get("/")
@no_type_check
async def read_root() -> dict[str, str]:
    """Root endpoint.

    Returns:
    -------
    dict[str, str]
        Welcome message.
    """
    # TODO: use this root endpoint to provide more information about the API and how
    # to use it.
    return {"message": "Welcome to the pyFanta API!"}
