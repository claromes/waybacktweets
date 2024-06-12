import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import unquote

from requests import exceptions
from rich import print as rprint
from rich.progress import Progress

from waybacktweets.utils import (
    check_double_status,
    check_pattern_tweet,
    clean_tweet_url,
    delete_tweet_pathnames,
    get_response,
    semicolon_parser,
)


class TwitterEmbed:
    """Handles parsing of tweets using the Twitter Publish service."""

    def __init__(self, tweet_url):
        self.tweet_url = tweet_url

    def embed(self):
        """Parses the archived tweets when they are still available."""
        try:
            url = f"https://publish.twitter.com/oembed?url={self.tweet_url}"
            response = get_response(url=url)

            if response:
                json_response = response.json()
                html = json_response["html"]
                author_name = json_response["author_name"]

                regex = re.compile(
                    r'<blockquote class="twitter-tweet"(?: [^>]+)?><p[^>]*>(.*?)<\/p>.*?&mdash; (.*?)<\/a>',  # noqa
                    re.DOTALL,
                )
                regex_author = re.compile(r"^(.*?)\s*\(")

                matches_html = regex.findall(html)

                tweet_content = []
                user_info = []
                is_RT = []

                for match in matches_html:
                    tweet_content_match = re.sub(
                        r"<a[^>]*>|<\/a>", "", match[0].strip()
                    ).replace("<br>", "\n")
                    user_info_match = re.sub(
                        r"<a[^>]*>|<\/a>", "", match[1].strip()
                    ).replace(")", "), ")
                    match_author = regex_author.search(user_info_match)
                    author_tweet = match_author.group(1) if match_author else ""

                    if tweet_content_match:
                        tweet_content.append(tweet_content_match)
                    if user_info_match:
                        user_info.append(user_info_match)
                        is_RT.append(author_name != author_tweet)

                return tweet_content, is_RT, user_info
        except exceptions:
            rprint("[yellow]Error parsing the tweet, but the CDX data was saved.")
            return None


class JsonParser:
    """Handles parsing of tweets when the mimetype is application/json."""

    def __init__(self, archived_tweet_url):
        self.archived_tweet_url = archived_tweet_url

    def parse(self):
        """Parses the archived tweets in JSON format."""
        try:
            response = get_response(url=self.archived_tweet_url)

            if response:
                json_data = response.json()

                if "data" in json_data:
                    return json_data["data"].get("text", json_data["data"])

                if "retweeted_status" in json_data:
                    return json_data["retweeted_status"].get(
                        "text", json_data["retweeted_status"]
                    )

                return json_data.get("text", json_data)
        except exceptions.ConnectionError:
            rprint(
                f"[yellow]Connection error with {self.archived_tweet_url}. Max retries exceeded. Error parsing the JSON, but the CDX data was saved."  # noqa: E501
            )
            return ""
        except exceptions:
            rprint("[yellow]Error parsing the JSON, but the CDX data was saved.")

            return ""


class TweetsParser:
    """Handles the overall parsing of archived tweets."""

    def __init__(self, archived_tweets_response, username, field_options):
        self.archived_tweets_response = archived_tweets_response
        self.username = username
        self.field_options = field_options
        self.parsed_tweets = {option: [] for option in self.field_options}

    def add_field(self, key, value):
        """
        Appends a value to a list in the parsed data structure.
        Defines which data will be structured and saved.
        """
        if key in self.parsed_tweets:
            self.parsed_tweets[key].append(value)

    def process_response(self, response):
        """Process the archived tweet's response and add the relevant CDX data."""
        tweet_remove_char = unquote(response[2]).replace("’", "")
        cleaned_tweet = check_pattern_tweet(tweet_remove_char).strip('"')

        wayback_machine_url = (
            f"https://web.archive.org/web/{response[1]}/{tweet_remove_char}"
        )
        original_tweet = delete_tweet_pathnames(
            clean_tweet_url(cleaned_tweet, self.username)
        )
        parsed_wayback_machine_url = (
            f"https://web.archive.org/web/{response[1]}/{original_tweet}"
        )

        double_status = check_double_status(wayback_machine_url, original_tweet)

        if double_status:
            original_tweet = delete_tweet_pathnames(
                f"https://twitter.com/{original_tweet}"
            )
        elif "://" not in original_tweet:
            original_tweet = delete_tweet_pathnames(f"https://{original_tweet}")

        encoded_tweet = semicolon_parser(response[2])
        encoded_archived_tweet = semicolon_parser(wayback_machine_url)
        encoded_parsed_tweet = semicolon_parser(original_tweet)
        encoded_parsed_archived_tweet = semicolon_parser(parsed_wayback_machine_url)

        embed_parser = TwitterEmbed(encoded_tweet)
        content = embed_parser.embed()

        if content:
            self.add_field("available_tweet_text", semicolon_parser(content[0][0]))
            self.add_field("available_tweet_is_RT", content[1][0])
            self.add_field("available_tweet_info", semicolon_parser(content[2][0]))

        parsed_text_json = ""

        if response[3] == "application/json":
            json_parser = JsonParser(encoded_parsed_archived_tweet)
            if json_parser:
                text_json = json_parser.parse()
                parsed_text_json = semicolon_parser(text_json)

        self.add_field("parsed_tweet_text_mimetype_json", parsed_text_json)
        self.add_field("archived_urlkey", response[0])
        self.add_field("archived_timestamp", response[1])
        self.add_field("original_tweet_url", encoded_tweet)
        self.add_field("archived_tweet_url", encoded_archived_tweet)
        self.add_field("parsed_tweet_url", encoded_parsed_tweet)
        self.add_field("parsed_archived_tweet_url", encoded_parsed_archived_tweet)
        self.add_field("archived_mimetype", response[3])
        self.add_field("archived_statuscode", response[4])
        self.add_field("archived_digest", response[5])
        self.add_field("archived_length", response[6])

    def parse(self):
        """Parses the archived tweets CDX data and structures it."""
        with ThreadPoolExecutor(max_workers=10) as executor:

            futures = {
                executor.submit(self.process_response, response): response
                for response in self.archived_tweets_response[1:]
            }
            with Progress() as progress:
                task = progress.add_task(
                    f"Waybacking @{self.username} tweets\n", total=len(futures)
                )

                for future in as_completed(futures):
                    try:
                        future.result()
                    except Exception as e:
                        rprint(f"[red]{e}...")

                    progress.update(task, advance=1)

            return self.parsed_tweets
