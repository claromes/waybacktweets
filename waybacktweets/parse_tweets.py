import requests
import re
from urllib.parse import unquote
from utils import *
from rich.progress import track


class TwitterEmbed:
    """Handles parsing of tweets using the Twitter Publish service."""

    def __init__(self, tweet_url):
        self.tweet_url = tweet_url

    def embed(self):
        """Parses the archived tweets when they are still available."""
        try:
            url = f'https://publish.twitter.com/oembed?url={self.tweet_url}'
            response = requests.get(url)
            if not (400 <= response.status_code <= 511):
                html = response.json()['html']
                author_name = response.json()['author_name']

                regex = r'<blockquote class="twitter-tweet"(?: [^>]+)?><p[^>]*>(.*?)<\/p>.*?&mdash; (.*?)<\/a>'
                regex_author = r'^(.*?)\s*\('

                matches_html = re.findall(regex, html, re.DOTALL)

                tweet_content = []
                user_info = []
                is_RT = []

                for match in matches_html:
                    tweet_content_match = re.sub(r'<a[^>]*>|<\/a>', '',
                                                 match[0].strip())
                    tweet_content_match = tweet_content_match.replace(
                        '<br>', '\n')

                    user_info_match = re.sub(r'<a[^>]*>|<\/a>', '',
                                             match[1].strip())
                    user_info_match = user_info_match.replace(')', '), ')

                    match_author = re.search(regex_author, user_info_match)
                    author_tweet = match_author.group(
                        1) if match_author else ""

                    if tweet_content_match:
                        tweet_content.append(tweet_content_match)
                    if user_info_match:
                        user_info.append(user_info_match)

                        is_RT_match = False
                        if author_name != author_tweet:
                            is_RT_match = True

                        is_RT.append(is_RT_match)

                return tweet_content, is_RT, user_info
        except Exception as e:
            print(f"Error parsing tweet: {e}")
            return None


class JsonParser:
    """Handles parsing of tweets when the mimetype is application/json."""

    def __init__(self, archived_tweet_url):
        self.archived_tweet_url = archived_tweet_url

    def parse(self):
        """Parses the archived tweets in JSON format."""
        try:
            response = requests.get(self.archived_tweet_url)
            if not (400 <= response.status_code <= 511):
                json_data = response.json()

                if 'data' in json_data:
                    return json_data['data'].get('text', json_data['data'])
                elif 'retweeted_status' in json_data:
                    return json_data['retweeted_status'].get(
                        'text', json_data['retweeted_status'])
                else:
                    return json_data.get('text', json_data)
        except Exception as e:
            print(f"Error parsing JSON mimetype tweet: {e}")
            return None


class TweetsParser:
    """Handles the overall parsing of archived tweets."""

    def __init__(self, archived_tweets_response, username, metadata_options):
        self.archived_tweets_response = archived_tweets_response
        self.username = username
        self.metadata_options = metadata_options
        self.parsed_tweets = {option: [] for option in self.metadata_options}

    def add_metadata(self, key, value):
        """Appends a value to a list in the parsed data structure.
        Defines which data will be structured and saved."""
        if key in self.parsed_tweets:
            self.parsed_tweets[key].append(value)

    def parse(self):
        """Parses the archived tweets metadata and structures it."""
        for response in track(
                self.archived_tweets_response[1:],
                description=f'Wayback @{self.username} tweets\n'):
            tweet_remove_char = unquote(response[2]).replace('’', '')
            cleaned_tweet = pattern_tweet(tweet_remove_char).strip('"')

            wayback_machine_url = f'https://web.archive.org/web/{response[1]}/{tweet_remove_char}'
            original_tweet = delete_tweet_pathnames(
                clean_tweet_url(cleaned_tweet, self.username))
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

            embed_parser = TwitterEmbed(encoded_tweet)
            content = embed_parser.embed()

            if content:
                self.add_metadata('available_tweet_text',
                                  semicolon_parse(content[0][0]))
                self.add_metadata('available_tweet_is_RT', content[1][0])
                self.add_metadata('available_tweet_username',
                                  semicolon_parse(content[2][0]))

            if response[3] == 'application/json':
                json_parser = JsonParser(encoded_archived_tweet)
                text_json = json_parser.parse()
                parsed_text_json = semicolon_parse(text_json)
            else:
                parsed_text_json = None

            self.add_metadata('parsed_tweet_text_mimetype_json',
                              parsed_text_json)

            self.add_metadata('archived_urlkey', response[0])
            self.add_metadata('archived_timestamp', response[1])
            self.add_metadata('original_tweet_url', encoded_tweet)
            self.add_metadata('archived_tweet_url', encoded_archived_tweet)
            self.add_metadata('parsed_tweet_url', encoded_parsed_tweet)
            self.add_metadata('parsed_archived_tweet_url',
                              encoded_parsed_archived_tweet)
            self.add_metadata('archived_mimetype', response[3])
            self.add_metadata('archived_statuscode', response[4])
            self.add_metadata('archived_digest', response[5])
            self.add_metadata('archived_length', response[6])

        return self.parsed_tweets
