"""
Parses the returned data from the Wayback CDX Server API.
"""

import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from contextlib import nullcontext
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import unquote

from rich import print as rprint
from rich.progress import Progress

from waybacktweets.config.config import config
from waybacktweets.config.field_options import FIELD_OPTIONS
from waybacktweets.exceptions.exceptions import (
    ConnectionError,
    GetResponseError,
    HTTPError,
)
from waybacktweets.utils.utils import (
    check_double_status,
    check_pattern_tweet,
    check_url_scheme,
    clean_tweet_url,
    delete_tweet_pathnames,
    get_response,
    is_tweet_url,
    semicolon_parser,
    timestamp_parser,
)


class TwitterEmbed:
    """
    This class is responsible for parsing tweets using the Twitter Publish service.

    Args:
        tweet_url (str): The URL of the tweet to be parsed.
    """

    def __init__(self, tweet_url: str):
        self.tweet_url = tweet_url

    def embed(self) -> Optional[Tuple[List[str], List[bool], List[str]]]:
        """
        Parses the archived tweets when they are still available.

        This function goes through each archived tweet and checks if it is still available. If the tweet is available, it extracts the necessary information and adds it to the respective lists. The function returns a tuple of three lists:

        - The first list contains the tweet texts.
        - The second list contains boolean values indicating whether each tweet is still available.
        - The third list contains the URLs of the tweets.

        Returns:
            A tuple of three lists containing the tweet texts, availability statuses, and URLs, respectively. If no tweets are available, returns None.
        """  # noqa: E501
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
        except ConnectionError:
            if config.verbose:
                rprint("[yellow]Error parsing the tweet, but the CDX data was saved.")
        except HTTPError:
            if config.verbose:
                rprint(
                    f"[yellow]{self.tweet_url} not available on the user's account, but the CDX data was saved."  # noqa: E501
                )
        except GetResponseError as e:
            if config.verbose:
                rprint(f"[red]An error occurred: {str(e)}")

        return None


class JsonParser:
    """
    This class is responsible for parsing tweets when the mimetype is application/json.

    Note: This class is in an experimental phase, but it is currently being used by the Streamlit Web App.

    Args:
        archived_tweet_url (str): The URL of the archived tweet to be parsed.
    """  # noqa: E501

    def __init__(self, archived_tweet_url: str):
        self.archived_tweet_url = archived_tweet_url

    def parse(self) -> str:
        """
        Parses the archived tweets in JSON format.

        Returns:
            The parsed tweet text.
        """
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
        except ConnectionError:
            if config.verbose:
                rprint(
                    f"[yellow]Connection error with {self.archived_tweet_url}. Max retries exceeded. Error parsing the JSON, but the CDX data was saved."  # noqa: E501
                )
        except GetResponseError as e:
            if config.verbose:
                rprint(f"[red]An error occurred: {str(e)}")

        return None


class TweetsParser:
    """
    This class is responsible for the overall parsing of archived tweets.

    Args:
        archived_tweets_response (List[str]): The response from the archived tweets.
        username (str): The username associated with the tweets.
        field_options (List[str]): The fields to be included in the parsed data. For more details on each option, visit :ref:`field_options`.
    """  # noqa: E501

    def __init__(
        self,
        archived_tweets_response: List[str],
        username: str,
        field_options: List[str],
    ):
        if not all(option in FIELD_OPTIONS for option in field_options):
            raise ValueError("Some field options are not valid.")

        self.archived_tweets_response = archived_tweets_response
        self.username = username
        self.field_options = field_options
        self.parsed_tweets = {option: [] for option in self.field_options}

    def _add_field(self, key: str, value: Any) -> None:
        """
        Appends a value to a list in the parsed data structure.

        Args:
            key (str): The key in the parsed data structure.
            value (Any): The value to be appended.
        """
        if key in self.parsed_tweets:
            self.parsed_tweets[key].append(value)

    def _process_response(self, response: List[str]) -> None:
        """
        Processes the archived tweet's response and adds the relevant CDX data.

        Args:
            response (List[str]): The response from the archived tweet.
        """
        tweet_remove_char = unquote(response[2]).replace("’", "")
        cleaned_tweet = check_pattern_tweet(tweet_remove_char).strip('"')

        wayback_machine_url = (
            f"https://web.archive.org/web/{response[1]}/{tweet_remove_char}"
        )
        original_tweet = delete_tweet_pathnames(
            clean_tweet_url(cleaned_tweet, self.username)
        )

        double_status = check_double_status(wayback_machine_url, original_tweet)

        if double_status:
            original_tweet = delete_tweet_pathnames(
                f"https://twitter.com{original_tweet}"
            )
        elif "://" not in original_tweet:
            original_tweet = delete_tweet_pathnames(f"https://{original_tweet}")

        parsed_wayback_machine_url = (
            f"https://web.archive.org/web/{response[1]}/{original_tweet}"
        )

        encoded_archived_tweet = check_url_scheme(semicolon_parser(wayback_machine_url))
        encoded_parsed_archived_tweet = check_url_scheme(
            semicolon_parser(parsed_wayback_machine_url)
        )
        encoded_tweet = check_url_scheme(semicolon_parser(response[2]))
        encoded_parsed_tweet = check_url_scheme(semicolon_parser(original_tweet))

        available_tweet_text = None
        available_tweet_is_RT = None
        available_tweet_info = None

        is_tweet = is_tweet_url(encoded_tweet)

        if is_tweet:
            embed_parser = TwitterEmbed(encoded_tweet)
            content = embed_parser.embed()

            if content:
                available_tweet_text = semicolon_parser(content[0][0])
                available_tweet_is_RT = content[1][0]
                available_tweet_info = semicolon_parser(content[2][0])

        self._add_field("available_tweet_text", available_tweet_text)
        self._add_field("available_tweet_is_RT", available_tweet_is_RT)
        self._add_field("available_tweet_info", available_tweet_info)

        self._add_field("archived_urlkey", response[0])
        self._add_field("archived_timestamp", response[1])
        self._add_field("parsed_archived_timestamp", timestamp_parser(response[1]))
        self._add_field("archived_tweet_url", encoded_archived_tweet)
        self._add_field("parsed_archived_tweet_url", encoded_parsed_archived_tweet)
        self._add_field("original_tweet_url", encoded_tweet)
        self._add_field("parsed_tweet_url", encoded_parsed_tweet)
        self._add_field("archived_mimetype", response[3])
        self._add_field("archived_statuscode", response[4])
        self._add_field("archived_digest", response[5])
        self._add_field("archived_length", response[6])

    def parse(self, print_progress=False) -> Dict[str, List[Any]]:
        """
        Parses the archived tweets CDX data and structures it.

        Args:
            print_progress (bool): A boolean indicating whether to print progress or not.

        Returns:
            The parsed tweets data.
        """  # noqa: E501
        with ThreadPoolExecutor(max_workers=10) as executor:

            futures = {
                executor.submit(self._process_response, response): response
                for response in self.archived_tweets_response[1:]
            }

            progress_context = Progress() if print_progress else nullcontext()
            with progress_context as progress:
                task = None
                if print_progress:
                    task = progress.add_task(
                        f"Waybacking @{self.username} tweets\n", total=len(futures)
                    )

                for future in as_completed(futures):
                    try:
                        future.result()
                    except Exception as e:
                        rprint(f"[red]{e}")

                    if print_progress:
                        progress.update(task, advance=1)

            return self.parsed_tweets
