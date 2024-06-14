"""
CLI function for retrieving archived tweets.
"""

from typing import Optional

import click
from requests import exceptions
from rich import print as rprint

from waybacktweets.api.export_tweets import TweetsExporter
from waybacktweets.api.parse_tweets import TweetsParser
from waybacktweets.api.request_tweets import WaybackTweets
from waybacktweets.utils.utils import parse_date


@click.command()
@click.argument("username", type=str)
@click.option(
    "--collapse",
    type=click.Choice(["urlkey", "digest", "timestamp:XX"], case_sensitive=False),
    default=None,
    help="Collapse results based on a field, or a substring of a field. XX in the timestamp value ranges from 1 to 14, comparing the first XX digits of the timestamp field. It is recommended to use from 4 onwards, to compare at least by years.",  # noqa: E501
)
@click.option(
    "--from",
    "timestamp_from",
    type=click.UNPROCESSED,
    metavar="DATE",
    callback=parse_date,
    default=None,
    help="Filtering by date range from this date. Format: YYYYmmdd",
)
@click.option(
    "--to",
    "timestamp_to",
    type=click.UNPROCESSED,
    metavar="DATE",
    callback=parse_date,
    default=None,
    help="Filtering by date range up to this date. Format: YYYYmmdd",
)
@click.option("--limit", type=int, default=None, help="Query result limits.")
@click.option(
    "--offset",
    type=int,
    default=None,
    help="Allows for a simple way to scroll through the results.",
)
def cli(
    username: str,
    collapse: Optional[str],
    timestamp_from: Optional[str],
    timestamp_to: Optional[str],
    limit: Optional[int],
    offset: Optional[int],
) -> None:
    """
    Retrieves archived tweets CDX data from the Wayback Machine,
    performs necessary parsing, and saves the data.

    USERNAME: The Twitter username without @.
    """
    try:
        api = WaybackTweets(
            username, collapse, timestamp_from, timestamp_to, limit, offset
        )

        print("Making a request to the Internet Archive...")
        archived_tweets = api.get()

        if archived_tweets:
            field_options = [
                "archived_urlkey",
                "archived_timestamp",
                "original_tweet_url",
                "archived_tweet_url",
                "parsed_tweet_url",
                "parsed_archived_tweet_url",
                # "parsed_tweet_text_mimetype_json", # TODO: JSON Issue
                "available_tweet_text",
                "available_tweet_is_RT",
                "available_tweet_info",
                "archived_mimetype",
                "archived_statuscode",
                "archived_digest",
                "archived_length",
            ]

            parser = TweetsParser(archived_tweets, username, field_options)
            parsed_tweets = parser.parse(print_progress=True)

            exporter = TweetsExporter(parsed_tweets, username, field_options)

            exporter.save_to_csv()
            exporter.save_to_json()
            exporter.save_to_html()
    except exceptions as e:
        rprint(f"[red]{e}")
    finally:
        rprint(
            "[yellow]\nNeed help? Read the docs: https://claromes.github.io/waybacktweets"  # noqa: E501
        )
