import requests


def get_archived_tweets(username,
                        unique=False,
                        timestamp_from='',
                        timestamp_to=''):

    unique = f'&collapse=urlkey' if unique else ''

    if timestamp_from:
        timestamp_from = f'&from={timestamp_from}'

    if timestamp_to:
        timestamp_to = f'&to={timestamp_to}'

    url = f'https://web.archive.org/cdx/search/cdx?url=https://twitter.com/{username}/status/*&output=json{unique}{timestamp_from}{timestamp_to}'
    print(f'Getting and parsing archived tweets from {url}')

    try:
        response = requests.get(url)
        response.raise_for_status()

        if not (400 <= response.status_code <= 511):
            return response.json()
    except requests.exceptions.Timeout as e:
        print(f'{e}.\nConnection to web.archive.org timed out.')
    except requests.exceptions.ConnectionError as e:
        print(
            f'{e}.\nFailed to establish a new connection with web.archive.org.'
        )
    except requests.exceptions.HTTPError as e:
        print(
            f'{e}.\nTemporarily Offline: Internet Archive services are temporarily offline. Please check Internet Archive [Twitter feed](https://twitter.com/internetarchive/) for the latest information.'
        )
    except UnboundLocalError as e:
        print(e)
