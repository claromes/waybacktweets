from requests import exceptions
from rich import print as rprint

from waybacktweets.utils.utils import get_response


class WaybackTweets:
    """Requests data from the Wayback CDX Server API and returns it in JSON format."""

    def __init__(self, username, collapse, timestamp_from, timestamp_to, limit, offset):
        self.username = username
        self.collapse = collapse
        self.timestamp_from = timestamp_from
        self.timestamp_to = timestamp_to
        self.limit = limit
        self.offset = offset

    def get(self):
        """GET request to the Internet Archive's CDX API to retrieve archived tweets."""
        url = "https://web.archive.org/cdx/search/cdx"
        params = {
            "url": f"https://twitter.com/{self.username}/status/*",
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

        print("Making a request to the Internet Archive...")

        try:
            response = get_response(url=url, params=params)

            if response:
                return response.json()
        except exceptions.ReadTimeout:
            rprint("[red]Connection to web.archive.org timed out.")
        except exceptions.ConnectionError:
            rprint(
                "[red]Failed to establish a new connection with web.archive.org. Max retries exceeded."  # noqa: E501
            )
        except exceptions.HTTPError:
            rprint(
                "[red]Temporarily Offline: Internet Archive services are temporarily offline. Please check Internet Archive Twitter feed (https://twitter.com/internetarchive) for the latest information."  # noqa: E501
            )
        except Exception as e:
            rprint(f"[red]{e}")
