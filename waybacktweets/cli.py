"""
CLI functions for retrieving archived tweets.
"""

from datetime import datetime

import click
from requests import exceptions
from rich import print as rprint

from waybacktweets.export_tweets import TweetsExporter
from waybacktweets.parse_tweets import TweetsParser
from waybacktweets.request_tweets import WaybackTweets


def parse_date(ctx, param, value):
    if value is None:
        return None

    date = datetime.strptime(value, "%Y%m%d")
    return date.strftime("%Y%m%d")


@click.command()
@click.argument("username", type=str)
@click.option(
    "--unique",
    type=bool,
    default=False,
    help="Only show unique URLs. Filtering by the collapse option using the urlkey field.",  # noqa: E501
)
@click.option(
    "--from",
    "timestamp_from",
    type=click.UNPROCESSED,
    callback=parse_date,
    default=None,
    help="Filtering by date range from this date.",
)
@click.option(
    "--to",
    "timestamp_to",
    type=click.UNPROCESSED,
    callback=parse_date,
    default=None,
    help="Filtering by date range up to this date.",
)
@click.option("--limit", type=int, default=None, help="Query result limits.")
@click.option(
    "--offset",
    type=int,
    default=None,
    help="Allows for a simple way to scroll through the results.",
)
def cli(username, unique, timestamp_from, timestamp_to, limit, offset):
    """
    Retrieves archived tweets' CDX data from the Wayback Machine,
    performs necessary parsing, and saves the data.

    USERNAME: The Twitter username without @.
    """
    try:
        api = WaybackTweets(
            username, unique, timestamp_from, timestamp_to, limit, offset
        )
        archived_tweets = api.get()

        if archived_tweets:
            field_options = [
                "archived_urlkey",
                "archived_timestamp",
                "original_tweet_url",
                "archived_tweet_url",
                "parsed_tweet_url",
                "parsed_archived_tweet_url",
                "parsed_tweet_text_mimetype_json",
                "available_tweet_text",
                "available_tweet_is_RT",
                "available_tweet_info",
                "archived_mimetype",
                "archived_statuscode",
                "archived_digest",
                "archived_length",
            ]

            parser = TweetsParser(archived_tweets, username, field_options)
            parsed_tweets = parser.parse()

            exporter = TweetsExporter(parsed_tweets, username, field_options)

            exporter.save_to_csv()
            exporter.save_to_json()
            exporter.save_to_html()

    except exceptions as e:
        rprint(f"[red]{e}")
    finally:
        rprint(
            "[yellow]\nNeed help? Open an issue: https://github.com/claromes/waybacktweets/issues"  # noqa: E501
        )
