"""Module to define FastAPI global exceptions."""

from typing import no_type_check

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.scraper.exceptions import FetchError, PageStructureError


def register_exception_handlers(app: FastAPI) -> None:
    """Register exception handlers with the FastAPI app.

    Parameters
    ----------
    app : FastAPI
        FastAPI app.
    """

    @app.exception_handler(FetchError)
    @no_type_check
    async def fetch_error_handler(
        request: Request,
        exc: FetchError,
    ) -> JSONResponse:
        """Handle FetchError exceptions.

        This exception handler catches `FetchError` exceptions and returns an HTTP 502
        Bad Gateway response with the exception details.

        Parameters
        ----------
        request : Request
            The HTTP request that resulted in the exception.
        exc : FetchError
            The `FetchError` exception instance that was raised.

        Returns:
        -------
        JSONResponse
            A JSON response with status code 502 and a detailed error message.
        """
        return JSONResponse(
            status_code=502,
            content={"detail": str(exc)},
        )

    @app.exception_handler(PageStructureError)
    @no_type_check
    async def page_structure_error_handler(
        request: Request,
        exc: PageStructureError,
    ) -> JSONResponse:
        """Handle PageStructureError exceptions.

        This exception handler catches `PageStructureError` exceptions and returns an
        HTTP 500 Internal Server Error response with the exception details.

        Parameters
        ----------
        request : Request
            The HTTP request that resulted in the exception.
        exc : PageStructureError
            The `PageStructureError` exception instance that was raised.

        Returns:
        -------
        JSONResponse
            A JSON response with status code 500 and a detailed error message.
        """
        return JSONResponse(
            status_code=500,
            content={"detail": str(exc)},
        )

    @app.exception_handler(ValueError)
    @no_type_check
    async def value_error_handler(
        request: Request,
        exc: ValueError,
    ) -> JSONResponse:
        """Handle ValueError exceptions.

        This exception handler catches `ValueError` exceptions and returns an
        HTTP 400 Bad Request response with the exception details.

        Parameters
        ----------
        request : Request
            The HTTP request that resulted in the exception.
        exc : ValueError
            The `ValueError` exception instance that was raised.

        Returns:
        -------
        JSONResponse
            A JSON response with status code 400 and a detailed error message.
        """
        return JSONResponse(
            status_code=400,
            content={"detail": str(exc)},
        )

    @app.exception_handler(Exception)
    @no_type_check
    async def general_exception_handler(
        request: Request,
        exc: Exception,
    ) -> JSONResponse:
        """Handle all unhandled exceptions.

        This exception handler catches any unhandled exceptions and returns an
        HTTP 500 Internal Server Error response with a generic error message.

        Parameters
        ----------
        request : Request
            The HTTP request that resulted in the exception.
        exc : Exception
            The exception instance that was raised.

        Returns:
        -------
        JSONResponse
            A JSON response with status code 500 and a generic error message.
        """
        return JSONResponse(
            status_code=500,
            content={"detail": "An internal server error occurred."},
        )
