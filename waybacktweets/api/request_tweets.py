from typing import Any, Dict, Optional

from requests import exceptions
from rich import print as rprint

from waybacktweets.utils.utils import get_response


class WaybackTweets:
    """
    Class responsible for requesting data from the Wayback CDX Server API.

    :param username: The username associated with the tweets.
    :param collapse: The field to collapse duplicate lines on.
    :param timestamp_from: The timestamp to start retrieving tweets from.
    :param timestamp_to: The timestamp to stop retrieving tweets at.
    :param limit: The maximum number of results to return.
    :param offset: The number of lines to skip in the results.
    :param matchType: Results matching a certain prefix, a certain host or all subdomains.
    """  # noqa: E501

    def __init__(
        self,
        username: str,
        collapse: str = None,
        timestamp_from: str = None,
        timestamp_to: str = None,
        limit: int = None,
        offset: int = None,
        matchtype: str = None,
    ):
        self.username = username
        self.collapse = collapse
        self.timestamp_from = timestamp_from
        self.timestamp_to = timestamp_to
        self.limit = limit
        self.offset = offset
        self.matchtype = matchtype

    def get(self) -> Optional[Dict[str, Any]]:
        """
        Sends a GET request to the Internet Archive's CDX API
        to retrieve archived tweets.

        :returns: The response from the CDX API in JSON format, if successful.
        """
        url = "https://web.archive.org/cdx/search/cdx"

        status = "/status/*"
        if self.matchtype != "exact":
            status = ""

        params = {
            "url": f"https://twitter.com/{self.username}{status}",
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

        if self.offset:
            params["offset"] = self.offset

        if self.matchtype:
            params["matchType"] = self.matchtype

        try:
            response = get_response(url=url, params=params)

            if response:
                return response.json()
        except exceptions.ReadTimeout:
            rprint("[red]Connection to web.archive.org timed out.")
        except exceptions.ConnectionError:
            rprint(
                "[red]Failed to establish a new connection with web.archive.org. Max retries exceeded. Please wait a few minutes and try again."  # noqa: E501
            )
        except exceptions.HTTPError:
            rprint(
                "[red]Temporarily Offline: Internet Archive services are temporarily offline. Please check Internet Archive Twitter feed (https://twitter.com/internetarchive) for the latest information."  # noqa: E501
            )
        except Exception as e:
            rprint(f"[red]{e}")
