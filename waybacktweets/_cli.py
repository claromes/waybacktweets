# flake8: noqa: E501
"""
CLI functions for retrieving archived tweets.
"""

from datetime import datetime
from importlib.metadata import version
from typing import Any, Optional

import click
from rich import print as rprint

from waybacktweets.api.export import TweetsExporter
from waybacktweets.api.parse import TweetsParser
from waybacktweets.api.request import WaybackTweets
from waybacktweets.config.config import config

PACKAGE_NAME = "waybacktweets"


class CustomCommand(click.Command):
    """
    Custom Click command that overrides the default help message.
    """

    def format_help(
        self, ctx: click.Context, formatter: click.HelpFormatter
    ) -> None:  # noqa: E501
        """
        Customize the help message shown when the command is invoked with --help.

        Args:
            ctx (click.Context): The Click context for the command.
            formatter (click.HelpFormatter): The formatter used to generate the help text.
        """  # noqa: E501
        formatter.write_heading("Usage")
        formatter.write_text(f"  {PACKAGE_NAME} [OPTIONS] USERNAME")
        formatter.write_text("  USERNAME: The Twitter username without @")

        self.format_options(ctx, formatter)
        formatter.write("\n")

        formatter.write_heading("Examples")
        formatter.write_text("  waybacktweets jack")
        formatter.write_text(
            "  waybacktweets --from 20200305 --to 20231231 --limit 300 --verbose jack"
        )
        formatter.write("\n")

        formatter.write_heading("Repository")
        formatter.write_text("  https://github.com/claromes/waybacktweets")
        formatter.write("\n")

        formatter.write_heading("Documentation")
        formatter.write_text("  https://waybacktweets.claromes.com")


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
    """
    try:
        if value is None:
            return None

        date = datetime.strptime(value, "%Y%m%d")

        return date.strftime("%Y%m%d")
    except ValueError:
        raise click.BadParameter("Date must be in format YYYYmmdd")


@click.command(
    cls=CustomCommand, context_settings={"help_option_names": ["-h", "--help"]}, help=""
)
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
    "-rk",
    "--resumption_key",
    type=str,
    default=None,
    help="Allows for a simple way to scroll through the results. Key to continue the query from the end of the previous query.",  # noqa: E501
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
    help="Shows the log.",
)
@click.version_option(version=version(PACKAGE_NAME), prog_name=PACKAGE_NAME)
def main(
    username: str,
    collapse: Optional[str],
    timestamp_from: Optional[str],
    timestamp_to: Optional[str],
    limit: Optional[int],
    resumption_key: Optional[str],
    matchtype: Optional[str],
    verbose: Optional[bool],
) -> None:
    """
    Handles CLI queries for archived tweets with filtering and pagination.

    Args:
        username (str): Twitter username to search (without the @ symbol).
        collapse (Optional[str]): Collapse results based on a specific field or a substring
            of a field. Possible values include 'urlkey', 'digest', or 'timestamp:XX', where
            XX is the number of digits to match in timestamps (recommended: 4 or more).
        timestamp_from (Optional[str]): Start date for filtering results (format: YYYYMMDD).
        timestamp_to (Optional[str]): End date for filtering results (format: YYYYMMDD).
        limit (Optional[int]): Maximum number of results to return.
        resumption_key (Optional[str]): Resume a previous query using this key (for pagination).
        matchtype (Optional[str]): Filter by URL match type: 'exact', 'prefix', 'host', or 'domain'.
        verbose (Optional[bool]): Print verbose logs during execution.
    """  # noqa: E501
    try:
        config.verbose = verbose

        api = WaybackTweets(
            username,
            collapse,
            timestamp_from,
            timestamp_to,
            limit,
            resumption_key,
            matchtype,
        )

        print("Retrieving...")
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
                "resumption_key",
            ]

            parser = TweetsParser(archived_tweets, username, field_options)
            parsed_tweets = parser.parse(print_progress=True)

            exporter = TweetsExporter(parsed_tweets, username, field_options)

            exporter.save_to_csv()
            exporter.save_to_json()
            exporter.save_to_html()
    except Exception as e:
        rprint(f"[red]{e}")
