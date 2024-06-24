"""
Wayback Tweets Exceptions
"""


class GetResponseError(Exception):
    """
    Base class for exceptions in get_response.
    """


class ReadTimeoutError(GetResponseError):
    """
    Exception raised for read timeout errors.
    """


class ConnectionError(GetResponseError):
    """
    Exception raised for connection errors.
    """


class HTTPError(GetResponseError):
    """
    Exception raised for HTTP errors.
    """


class EmptyResponseError(GetResponseError):
    """
    Exception raised for empty responses.
    """
