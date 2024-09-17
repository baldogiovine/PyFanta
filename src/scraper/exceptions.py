"""Module to manage exceptions."""


class PageStructureError(Exception):
    """Exception raised when the page structure is not as expected."""


class FetchError(Exception):
    """Exception raised when fetching the page fails."""
