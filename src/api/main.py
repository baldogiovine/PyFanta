"""Main API module."""

from typing import no_type_check

from fastapi import FastAPI

from src.api.exceptions import register_exception_handlers
from src.api.routers.links_router import router as links_router

app = FastAPI(
    title="Players API",
    description="An API to get players' names and links for a specified year.",
    version="1.0.0",
)

# Include routers
app.include_router(links_router)

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
    return {"message": "Welcome to the Players API!"}
