import requests


class WaybackTweets:
    """Requests data from the Wayback CDX Server API and returns it in JSON format."""

    def __init__(self,
                 username,
                 unique=False,
                 timestamp_from='',
                 timestamp_to=''):
        self.username = username
        self.unique = unique
        self.timestamp_from = timestamp_from
        self.timestamp_to = timestamp_to

    def get(self):
        unique_param = '&collapse=urlkey' if self.unique else ''
        timestamp_from_param = f'&from={self.timestamp_from}' if self.timestamp_from else ''
        timestamp_to_param = f'&to={self.timestamp_to}' if self.timestamp_to else ''

        url = (
            f'https://web.archive.org/cdx/search/cdx?url=https://twitter.com/{self.username}/status/*'
            f'&output=json{unique_param}{timestamp_from_param}{timestamp_to_param}&limit=20'
        )
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
        return None
