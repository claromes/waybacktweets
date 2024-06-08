import httpx
from rich import print as rprint


class WaybackTweets:
    """Requests data from the Wayback CDX Server API and returns it in JSON format."""

    def __init__(self, username, unique=False, timestamp_from=None, timestamp_to=None):
        self.username = username
        self.unique = unique
        self.timestamp_from = timestamp_from
        self.timestamp_to = timestamp_to

    async def get(self):
        """GET request to the Internet Archive's CDX API to retrieve archived tweets."""
        url = "https://web.archive.org/cdx/search/cdx"
        params = {
            "url": f"https://twitter.com/{self.username}/status/*",
            "output": "json",
            "limit": 1000,
        }

        if self.unique:
            params["collapse"] = "urlkey"

        if self.timestamp_from:
            params["from"] = self.timestamp_from

        if self.timestamp_to:
            params["to"] = self.timestamp_to

        print("Hi, archivist...")

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, params=params)

            if not (400 <= response.status_code <= 511):
                return response.json()
        except httpx._exceptions.ReadTimeout:
            rprint("[red]Connection to web.archive.org timed out.")
        except httpx._exceptions.ConnectError:
            rprint("[red]Failed to establish a new connection with web.archive.org.")
        except httpx._exceptions.HTTPError:
            rprint(
                "[red]Temporarily Offline: Internet Archive services are temporarily offline. Please check Internet Archive Twitter feed (https://twitter.com/internetarchive) for the latest information."  # noqa: E501
            )
        except UnboundLocalError as e:
            print(e)
