"""
Main function for retrieving archived tweets.
"""

from export_tweets import TweetsExporter
from parse_tweets import TweetsParser
from request_tweets import WaybackTweets
from rich import print as rprint

username = "claromes"
unique = False
datetime_from = "2020-01-01"
datetime_to = "2024-05-31"
ascending = False


def main():
    """
    Invokes the classes to retrieve archived tweets, perform necessary parsing,
    and save the data.
    """
    try:
        api = WaybackTweets(username, unique, datetime_from, datetime_to)
        archived_tweets = api.get()

        if archived_tweets:
            metadata_options = [
                "archived_urlkey",
                "archived_timestamp",
                "original_tweet_url",
                "archived_tweet_url",
                "parsed_tweet_url",
                "parsed_archived_tweet_url",
                "parsed_tweet_text_mimetype_json",
                "available_tweet_text",
                "available_tweet_is_RT",
                "available_tweet_username",
                "archived_mimetype",
                "archived_statuscode",
                "archived_digest",
                "archived_length",
            ]

            parser = TweetsParser(archived_tweets, username, metadata_options)
            parsed_tweets = parser.parse()

            exporter = TweetsExporter(
                parsed_tweets, username, metadata_options, ascending
            )
            exporter.save_to_csv()
            exporter.save_to_json()
            exporter.save_to_html()
        else:
            print("Nothing here.")

    except TypeError as e:
        print(e)
    finally:
        rprint(
            "[yellow]\nNeed help? Open an issue: https://github.com/claromes/waybacktweets/issues"  # noqa: E501
        )


if __name__ == "__main__":
    main()
