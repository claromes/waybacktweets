"""
CLI functions for retrieving archived tweets.
"""

from datetime import datetime
from typing import Any, Optional

import click
from rich import print as rprint

from waybacktweets.api.export import TweetsExporter
from waybacktweets.api.parse import TweetsParser
from waybacktweets.api.request import WaybackTweets
from waybacktweets.config.config import config


def _parse_date(
    ctx: Optional[Any] = None, param: Optional[Any] = None, value: Optional[str] = None
) -> Optional[str]:
    """
    Parses a date string and returns it in the format "YYYYMMDD".

    Args:
        ctx: Necessary when used with the click package. Defaults to None.
        param: Necessary when used with the click package. Defaults to None.
        value: A date string in the "YYYYMMDD" format. Defaults to None.

    Returns:
        The input date string formatted in the "YYYYMMDD" format, or None if no date string was provided.
    """  # noqa: E501
    try:
        if value is None:
            return None

        date = datetime.strptime(value, "%Y%m%d")

        return date.strftime("%Y%m%d")
    except ValueError:
        raise click.BadParameter("Date must be in format YYYYmmdd")


@click.command()
@click.argument("username", type=str)
@click.option(
    "-c",
    "--collapse",
    type=click.Choice(["urlkey", "digest", "timestamp:XX"], case_sensitive=False),
    default=None,
    help="Collapse results based on a field, or a substring of a field. XX in the timestamp value ranges from 1 to 14, comparing the first XX digits of the timestamp field. It is recommended to use from 4 onwards, to compare at least by years.",  # noqa: E501
)
@click.option(
    "-f",
    "--from",
    "timestamp_from",
    type=click.UNPROCESSED,
    metavar="DATE",
    callback=_parse_date,
    default=None,
    help="Filtering by date range from this date. Format: YYYYmmdd",
)
@click.option(
    "-t",
    "--to",
    "timestamp_to",
    type=click.UNPROCESSED,
    metavar="DATE",
    callback=_parse_date,
    default=None,
    help="Filtering by date range up to this date. Format: YYYYmmdd",
)
@click.option(
    "-l",
    "--limit",
    type=int,
    metavar="INTEGER",
    default=None,
    help="Query result limits.",
)
@click.option(
    "-o",
    "--offset",
    type=int,
    metavar="INTEGER",
    default=None,
    help="Allows for a simple way to scroll through the results.",
)
@click.option(
    "-mt",
    "--matchtype",
    type=click.Choice(["exact", "prefix", "host", "domain"], case_sensitive=False),
    default=None,
    help="Results matching a certain prefix, a certain host or all subdomains.",  # noqa: E501
)
@click.option(
    "-v",
    "--verbose",
    "verbose",
    is_flag=True,
    default=False,
    help="Shows the error log.",
)
def main(
    username: str,
    collapse: Optional[str],
    timestamp_from: Optional[str],
    timestamp_to: Optional[str],
    limit: Optional[int],
    offset: Optional[int],
    matchtype: Optional[str],
    verbose: Optional[bool],
) -> None:
    """
    Retrieves archived tweets CDX data from the Wayback Machine, performs necessary parsing, and saves the data.

    USERNAME: The Twitter username without @.
    """  # noqa: E501
    try:
        config.verbose = verbose

        api = WaybackTweets(
            username, collapse, timestamp_from, timestamp_to, limit, offset, matchtype
        )

        print("Making a request to the Internet Archive...")
        archived_tweets = api.get()

        if archived_tweets:
            field_options = [
                "archived_urlkey",
                "archived_timestamp",
                "parsed_archived_timestamp",
                "archived_tweet_url",
                "parsed_archived_tweet_url",
                "original_tweet_url",
                "parsed_tweet_url",
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
    except Exception as e:
        rprint(f"[red]{e}")
    finally:
        rprint(
            "[yellow]\nNeed help? Read the docs: https://claromes.github.io/waybacktweets"  # noqa: E501
        )
