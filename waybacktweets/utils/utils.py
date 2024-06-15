"""
Module containing utility functions for handling HTTP requests and manipulating URLs.
"""

import re
from datetime import datetime
from typing import Any, Optional

import click
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


def get_response(
    url: str, params: Optional[dict] = None
) -> Optional[requests.Response]:
    """
    Sends a GET request to the specified URL and returns the response.

    :param url: The URL to send the GET request to.
    :param params: The parameters to include in the GET request.

    :returns: The response from the server,
        if the status code is not in the 400-511 range.
        If the status code is in the 400-511 range.
    """
    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.3)
    adapter = HTTPAdapter(max_retries=retry)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"  # noqa: E501
    }

    session.mount("http://", adapter)
    session.mount("https://", adapter)

    response = session.get(url, params=params, headers=headers)

    if 400 <= response.status_code <= 511:
        return None

    return response


def clean_tweet_url(tweet_url: str, username: str) -> str:
    """
    Cleans a tweet URL by ensuring it is associated with the correct username.

    :param tweet_url: The tweet URL to clean.
    :param username: The username to associate with the tweet URL.

    :returns: The cleaned tweet URL.
    """
    tweet_lower = tweet_url.lower()

    pattern = re.compile(r"/status/(\d+)")
    match_lower_case = pattern.search(tweet_lower)
    match_original_case = pattern.search(tweet_url)

    if match_lower_case and username in tweet_lower:
        return f"https://twitter.com/{username}/status/{match_original_case.group(1)}"
    else:
        return tweet_url


def clean_wayback_machine_url(
    wayback_machine_url: str, archived_timestamp: str, username: str
) -> str:
    """
    Cleans a Wayback Machine URL by ensuring it is associated with the correct username
    and timestamp.

    :param wayback_machine_url: The Wayback Machine URL to clean.
    :param archived_timestamp: The timestamp to associate with the Wayback Machine URL.
    :param username: The username to associate with the Wayback Machine URL.

    :returns: The cleaned Wayback Machine URL.
    """
    wayback_machine_url = wayback_machine_url.lower()

    pattern = re.compile(r"/status/(\d+)")
    match = pattern.search(wayback_machine_url)

    if match and username in wayback_machine_url:
        return f"https://web.archive.org/web/{archived_timestamp}/https://twitter.com/{username}/status/{match.group(1)}"  # noqa: E501
    else:
        return wayback_machine_url


def check_pattern_tweet(tweet_url: str) -> str:
    """
    Extracts the tweet ID from a tweet URL.

    :param tweet_url: The tweet URL to extract the ID from.

    :returns: The extracted tweet ID.
    """
    pattern = re.compile(r'/status/"([^"]+)"')

    match = pattern.search(tweet_url)
    if match:
        return match.group(1).lstrip("/")
    else:
        return tweet_url


def delete_tweet_pathnames(tweet_url: str) -> str:
    """
    Removes any pathnames from a tweet URL.

    :param tweet_url: The tweet URL to remove pathnames from.

    :returns: The tweet URL without any pathnames.
    """
    pattern_username = re.compile(r"https://twitter\.com/([^/]+)/status/\d+")
    match_username = pattern_username.match(tweet_url)

    pattern_id = r"https://twitter.com/\w+/status/(\d+)"
    match_id = re.search(pattern_id, tweet_url)

    if match_id and match_username:
        tweet_id = match_id.group(1)
        username = match_username.group(1)
        return f"https://twitter.com/{username}/status/{tweet_id}"
    else:
        return tweet_url


def check_double_status(wayback_machine_url: str, original_tweet_url: str) -> bool:
    """
    Checks if a Wayback Machine URL contains two occurrences of "/status/"
    and if the original tweet does not contain "twitter.com".

    :param wayback_machine_url: The Wayback Machine URL to check.
    :param original_tweet_url: The original tweet URL to check.

    :returns: True if the conditions are met, False otherwise.
    """
    if (
        wayback_machine_url.count("/status/") == 2
        and "twitter.com" not in original_tweet_url
    ):
        return True

    return False


def semicolon_parser(string: str) -> str:
    """
    Replaces semicolons in a string with %3B.

    :param string: The string to replace semicolons in.

    :returns: The string with semicolons replaced by %3B.
    """
    return "".join("%3B" if c == ";" else c for c in string)


def parse_date(
    ctx: Optional[Any] = None, param: Optional[Any] = None, value: Optional[str] = None
) -> Optional[str]:
    """
    Parses a date string and returns it in the format "YYYYMMDD".

    :param ctx: Necessary when used with the click package. Defaults to None.
    :param param: Necessary when used with the click package. Defaults to None.
    :param value: A date string in the "YYYYMMDD" format. Defaults to None.

    :returns: The input date string formatted in the "YYYYMMDD" format,
        or None if no date string was provided.
    """
    try:
        if value is None:
            return None

        date = datetime.strptime(value, "%Y%m%d")

        return date.strftime("%Y%m%d")
    except ValueError:
        raise click.BadParameter("Date must be in format YYYYmmdd")


def is_tweet_url(twitter_url: str) -> bool:
    """
    Checks if the provided URL is a Twitter status URL.

    This function checks if the provided URL contains "/status/" exactly once,
    which is a common pattern in Twitter status URLs.

    :param twitter_url: The URL to check.

    :returns: True if the URL is a Twitter status URL, False otherwise.
    """
    if twitter_url.count("/status/") == 1:
        return True

    return False
