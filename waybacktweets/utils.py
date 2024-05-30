"""
Helper functions.
"""

import re


def clean_tweet_url(tweet, username):
    """Converts the tweet to lowercase, checks if it contains a tweet URL associated with the username.
    Returns the original tweet URL with correct casing; or returns the original tweet."""
    tweet_lower = tweet.lower()

    pattern = re.compile(r'/status/(\d+)')
    match_lower_case = pattern.search(tweet_lower)
    match_original_case = pattern.search(tweet)

    if match_lower_case and username in tweet_lower:
        return f'https://twitter.com/{username}/status/{match_original_case.group(1)}'
    else:
        return tweet


def clean_wayback_machine_url(wayback_machine_url, archived_timestamp,
                              username):
    """Converts the Wayback Machine URL to lowercase, checks if it contains a tweet URL associated with the username.
    Returns the original tweet URL with correct casing and archived timestamp; otherwise, it returns the original Wayback Machine URL."""
    wayback_machine_url = wayback_machine_url.lower()

    pattern = re.compile(r'/status/(\d+)')
    match = pattern.search(wayback_machine_url)

    if match and username in wayback_machine_url:
        return f'https://web.archive.org/web/{archived_timestamp}/https://twitter.com/{username}/status/{match.group(1)}'
    else:
        return wayback_machine_url


def pattern_tweet(tweet):
    """Extracts tweet IDs from various types of tweet URLs or tweet-related patterns.

    Reply pattern: /status//
    Link pattern:  /status///
    Twimg pattern: /status/https://pbs"""
    pattern = re.compile(r'/status/"([^"]+)"')

    match = pattern.search(tweet)
    if match:
        return match.group(1).lstrip('/')
    else:
        return tweet


def delete_tweet_pathnames(tweet):
    """Removes any pathnames (/photos, /likes, /retweet...) from the tweet URL."""
    pattern_username = re.compile(r'https://twitter\.com/([^/]+)/status/\d+')
    match_username = pattern_username.match(tweet)

    pattern_id = r'https://twitter.com/\w+/status/(\d+)'
    match_id = re.search(pattern_id, tweet)

    if match_id and match_username:
        tweet_id = match_id.group(1)
        username = match_username.group(1)
        return f'https://twitter.com/{username}/status/{tweet_id}'
    else:
        return tweet


def check_double_status(wayback_machine_url, original_tweet):
    """Checks if a Wayback Machine URL contains two occurrences of "/status/" and if the original tweet does not contain "twitter.com".
    Returns a boolean."""
    if wayback_machine_url.count(
            '/status/') == 2 and not 'twitter.com' in original_tweet:
        return True

    return False


def semicolon_parse(string):
    """Replaces semicolons in a string with %3B."""
    return ''.join('%3B' if c == ';' else c for c in string)
