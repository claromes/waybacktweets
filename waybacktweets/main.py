from request_tweets import *
from tweet_parse import *
from export_tweets import *

username = 'dfrlab'
unique = False
datetime_from = ''
datetime_to = ''


def main():
    try:
        archived_tweets = get_archived_tweets(username, unique, datetime_from,
                                              datetime_to)
        if archived_tweets:
            data = parse_archived_tweets(archived_tweets, username)

            response_tweets_csv(data, username)
    except TypeError as e:
        print(e)


if __name__ == '__main__':
    main()
