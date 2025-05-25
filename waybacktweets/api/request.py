"""
Requests data from the Wayback Machine API.
"""

from typing import Any, Dict, Optional

from rich import print as rprint

from waybacktweets.config.config import config
from waybacktweets.exceptions.exceptions import (
    ConnectionError,
    EmptyResponseError,
    GetResponseError,
    HTTPError,
    ReadTimeoutError,
)
from waybacktweets.utils.utils import get_response


class WaybackTweets:
    """
    Class responsible for requesting data from the Wayback CDX Server API.

    Args:
        username (str): The username associated with the tweets.
        collapse (str, optional): The field to collapse duplicate lines on.
        timestamp_from (str, optional): The timestamp to start retrieving tweets from.
        timestamp_to (str, optional): The timestamp to stop retrieving tweets at.
        limit (int, optional): The maximum number of results to return.
        resumption_key (int, optional): Key to continue the query from the end of the previous query.
        matchtype (str, optional): Results matching a certain prefix, a certain host or all subdomains.
    """  # noqa: E501

    def __init__(
        self,
        username: str,
        collapse: str = None,
        timestamp_from: str = None,
        timestamp_to: str = None,
        limit: int = None,
        resumption_key: str = None,
        matchtype: str = None,
    ):
        self.username = username
        self.collapse = collapse
        self.timestamp_from = timestamp_from
        self.timestamp_to = timestamp_to
        self.limit = limit
        self.resumption_key = resumption_key
        self.matchtype = matchtype

    def get(self) -> Optional[Dict[str, Any]]:
        """
        Sends a GET request to the Internet Archive's CDX API to retrieve archived tweets.

        Returns:
            The response from the CDX API in JSON format, if successful. Otherwise, None.
        """  # noqa: E501
        url = "https://web.archive.org/cdx/search/cdx"

        wildcard_pathname = "" if self.matchtype else "/*"

        show_resume_key = bool(self.limit)

        params = {
            "url": f"https://twitter.com/{self.username}/status{wildcard_pathname}",
            "showResumeKey": show_resume_key,
            "output": "json",
        }

        if self.collapse:
            params["collapse"] = self.collapse

        if self.timestamp_from:
            params["from"] = self.timestamp_from

        if self.timestamp_to:
            params["to"] = self.timestamp_to

        if self.limit:
            params["limit"] = self.limit

        if self.resumption_key:
            params["resumption_key"] = self.resumption_key

        if self.matchtype:
            params["matchType"] = self.matchtype

        try:
            response = get_response(url=url, params=params)
            return response.json(), {"show_resume_key": show_resume_key}
        except ReadTimeoutError:
            if config.verbose:
                rprint("[red]Connection to web.archive.org timed out.")
        except ConnectionError:
            if config.verbose:
                rprint(
                    "[red]Failed to establish a new connection with web.archive.org. Max retries exceeded. Please wait a few minutes and try again."  # noqa: E501
                )
        except HTTPError as e:
            if config.verbose:
                rprint(f"[red]HTTP error occurred: {str(e)}")
        except EmptyResponseError:
            if config.verbose:
                rprint("[red]No data was saved due to an empty response.")
        except GetResponseError as e:
            if config.verbose:
                rprint(f"[red]An error occurred: {str(e)}")

        return None
