"""
Parses the returned data from the Wayback CDX Server API.
"""

import requests
import re
from urllib.parse import unquote
from utils import *


def embed(tweet):
    """Parses the archived tweets when the tweets are still available using the Twitter Publish service from X.
    Returns the text of the tweet, if it's a retweet, and the username of the account."""
    try:
        url = f'https://publish.twitter.com/oembed?url={tweet}'
        response = requests.get(url)

        regex = r'<blockquote class="twitter-tweet"(?: [^>]+)?><p[^>]*>(.*?)<\/p>.*?&mdash; (.*?)<\/a>'
        regex_author = r'^(.*?)\s*\('

        if not (400 <= response.status_code <= 511):
            html = response.json()['html']
            author_name = response.json()['author_name']

            matches_html = re.findall(regex, html, re.DOTALL)

            tweet_content = []
            user_info = []
            is_RT = []

            for match in matches_html:
                tweet_content_match = re.sub(r'<a[^>]*>|<\/a>', '',
                                             match[0].strip())
                tweet_content_match = tweet_content_match.replace('<br>', '\n')

                user_info_match = re.sub(r'<a[^>]*>|<\/a>', '',
                                         match[1].strip())
                user_info_match = user_info_match.replace(')', '), ')

                match_author = re.search(regex_author, user_info_match)
                author_tweet = match_author.group(1)

                if tweet_content_match:
                    tweet_content.append(tweet_content_match)
                if user_info_match:
                    user_info.append(user_info_match)

                    is_RT_match = False
                    if author_name != author_tweet:
                        is_RT_match = True

                    is_RT.append(is_RT_match)

            return tweet_content, is_RT, user_info
    except:
        return None


def parse_json_mimetype(tweet):
    """Parses the archived tweets when the mimetype is application/json and returns the text of the tweet."""
    response_json = requests.get(tweet)

    if not (400 <= response_json.status_code <= 511):
        json_data = response_json.json()

        if 'data' in json_data:
            if 'text' in json_data['data']:
                json_text = json_data['data']['text']
                return json_text
            else:
                json_text = json_data['data']
                return json_text
        else:
            if 'text' in json_data:
                json_text = json_data['text']
                return json_text
            else:
                json_text = json_data
                return json_text


def parse_archived_tweets(archived_tweets_response, username):
    """Parses the archived tweets metadata and structures it in a more readable format."""
    archived_urlkey = []
    archived_timestamp = []
    tweet = []
    archived_tweet = []
    parsed_tweet = []
    parsed_tweet_mimetype_json = []
    available_tweet_content = []
    available_tweet_is_RT = []
    available_tweet_username = []
    parsed_archived_tweet = []
    archived_mimetype = []
    archived_statuscode = []
    archived_digest = []
    archived_length = []

    for response in archived_tweets_response[1:]:
        tweet_remove_char = unquote(response[2]).replace('’', '')
        cleaned_tweet = pattern_tweet(tweet_remove_char).strip('"')

        wayback_machine_url = f'https://web.archive.org/web/{response[1]}/{tweet_remove_char}'

        original_tweet = delete_tweet_pathnames(
            clean_tweet_url(cleaned_tweet, username))

        parsed_wayback_machine_url = f'https://web.archive.org/web/{response[1]}/{original_tweet}'

        double_status = check_double_status(wayback_machine_url,
                                            original_tweet)

        if double_status:
            original_tweet = delete_tweet_pathnames(
                f'https://twitter.com/{original_tweet}')

        elif not '://' in original_tweet:
            original_tweet = delete_tweet_pathnames(
                f'https://{original_tweet}')

        encoded_tweet = semicolon_parse(response[2])
        encoded_archived_tweet = semicolon_parse(wayback_machine_url)
        encoded_parsed_tweet = semicolon_parse(original_tweet)
        encoded_parsed_archived_tweet = semicolon_parse(
            parsed_wayback_machine_url)

        content = embed(encoded_tweet)
        if content:
            available_tweet_content.append(content[0][0])
            available_tweet_is_RT.append(content[1][0])
            available_tweet_username.append(content[2][0])

        if response[3] == 'application/json':
            json_mimetype = parse_json_mimetype(encoded_archived_tweet)
            parsed_tweet_mimetype_json.append(json_mimetype)

        archived_urlkey.append(response[0])
        archived_timestamp.append(response[1])
        tweet.append(encoded_tweet)
        archived_tweet.append(encoded_archived_tweet)
        parsed_tweet.append(encoded_parsed_tweet)
        parsed_archived_tweet.append(encoded_parsed_archived_tweet)
        archived_mimetype.append(response[3])
        archived_statuscode.append(response[4])
        archived_digest.append(response[5])
        archived_length.append(response[6])

    return archived_urlkey, archived_timestamp, tweet, archived_tweet, parsed_tweet, parsed_tweet_mimetype_json, parsed_archived_tweet, archived_mimetype, archived_statuscode, archived_digest, archived_length, available_tweet_content, available_tweet_is_RT, available_tweet_username
