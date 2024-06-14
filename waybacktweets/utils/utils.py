"""
Helper functions.
"""

import re
from datetime import datetime

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


def get_response(url, params=None):
    """Sends a GET request to the specified URL and returns the response."""
    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.3)
    adapter = HTTPAdapter(max_retries=retry)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"  # noqa: E501
    }

    session.mount("http://", adapter)
    session.mount("https://", adapter)

    response = session.get(url, params=params, headers=headers)

    if not 400 <= response.status_code <= 511:
        return response


def clean_tweet_url(tweet_url, username):
    """
    Converts the tweet to lowercase,
    checks if it contains a tweet URL associated with the username.
    Returns the original tweet URL with correct casing;
    or returns the original tweet.
    """
    tweet_lower = tweet_url.lower()

    pattern = re.compile(r"/status/(\d+)")
    match_lower_case = pattern.search(tweet_lower)
    match_original_case = pattern.search(tweet_url)

    if match_lower_case and username in tweet_lower:
        return f"https://twitter.com/{username}/status/{match_original_case.group(1)}"
    else:
        return tweet_url


def clean_wayback_machine_url(wayback_machine_url, archived_timestamp, username):
    """
    Converts the Wayback Machine URL to lowercase,
    checks if it contains a tweet URL associated with the username.
    Returns the original tweet URL with correct casing and archived timestamp;
    otherwise, it returns the original Wayback Machine URL.
    """
    wayback_machine_url = wayback_machine_url.lower()

    pattern = re.compile(r"/status/(\d+)")
    match = pattern.search(wayback_machine_url)

    if match and username in wayback_machine_url:
        return f"https://web.archive.org/web/{archived_timestamp}/https://twitter.com/{username}/status/{match.group(1)}"  # noqa: E501
    else:
        return wayback_machine_url


def check_pattern_tweet(tweet_url):
    """
    Extracts tweet IDs from various types of tweet URLs or tweet-related patterns.

    Reply pattern: /status//
    Link pattern:  /status///
    Twimg pattern: /status/https://pbs
    """
    pattern = re.compile(r'/status/"([^"]+)"')

    match = pattern.search(tweet_url)
    if match:
        return match.group(1).lstrip("/")
    else:
        return tweet_url


def delete_tweet_pathnames(tweet_url):
    """Removes any pathnames (/photos, /likes, /retweet...) from the tweet URL."""
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


def check_double_status(wayback_machine_url, original_tweet_url):
    """
    Checks if a Wayback Machine URL contains two occurrences of "/status/"
    and if the original tweet does not contain "twitter.com".
    Returns a boolean.
    """
    if (
        wayback_machine_url.count("/status/") == 2
        and "twitter.com" not in original_tweet_url
    ):
        return True

    return False


def semicolon_parser(string):
    """Replaces semicolons in a string with %3B."""
    return "".join("%3B" if c == ";" else c for c in string)


def parse_date(ctx=None, param=None, value=None):
    """
    Parses a date string and returns it in the format "YYYYMMDD".

    This function takes an optional date string as input,
    and if a date string is provided, it parses the date string into a datetime object
    and then formats it in the "YYYYMMDD" format.

    Args:
        ctx (None, optional): Necessary when used with the click package.
        Defaults to None.
        param (None, optional): Necessary when used with the click package.
        Defaults to None.
        value (str, optional): A date string in the "YYYYMMDD" format. Defaults to None.

    Returns:
        str: The input date string formatted in the "YYYYMMDD" format,
        or None if no date string was provided.
    """
    if value is None:
        return None

    date = datetime.strptime(value, "%Y%m%d")
    return date.strftime("%Y%m%d")
