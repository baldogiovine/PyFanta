"""Module to define PyFanta API."""

from fastapi import FastAPI

from routers import get_player_links

app = FastAPI()

app.include_router(get_player_links.router)
