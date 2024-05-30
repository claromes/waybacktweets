"""
Main function for retrieving archived tweets.
"""

from request_tweets import *
from parse_tweets import *
from export_tweets import *

username = 'claromes'
unique = False
datetime_from = ''
datetime_to = ''


def main():
    """Invokes the functions to retrieve archived tweets, perform necessary parsing, and save the data."""
    try:
        archived_tweets = get_archived_tweets(username, unique, datetime_from,
                                              datetime_to)
        if archived_tweets:
            data = parse_archived_tweets(archived_tweets, username)

            save_tweets(data, username)

        print(
            f'\nNeed help? Open an issue: https://github.com/claromes/waybacktweets/issues.'
        )
    except TypeError as e:
        print(e)


if __name__ == '__main__':
    main()
