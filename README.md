# Wayback Tweets

[![PyPI](https://img.shields.io/pypi/v/waybacktweets)](https://pypi.org/project/waybacktweets)

Retrieves archived tweets CDX data from the Wayback Machine, performs necessary parsing, and saves the data.

## Installation

```shell
pip install waybacktweets
```

## Quickstart

### Using Wayback Tweets as a standalone command line tool

waybacktweets [OPTIONS] USERNAME

```shell
waybacktweets --from 20150101 --to 20191231 --limit 250 jack
```

### Using Wayback Tweets as a Python Module

```python
from waybacktweets import WaybackTweets
from waybacktweets.utils import parse_date

username = "jack"
collapse = "urlkey"
timestamp_from = parse_date("20150101")
timestamp_to = parse_date("20191231")
limit = 250
offset = 0

api = WaybackTweets(username, collapse, timestamp_from, timestamp_to, limit, offset)

archived_tweets = api.get()
```

### Using Wayback Tweets as a Web App

[Access the application](https://waybacktweets.streamlit.app), a prototype written in Python with the Streamlit framework and hosted on Streamlit Cloud.

## Documentation

- [Wayback Tweets documentation]()
- [Wayback CDX Server API - Beta documentation](https://archive.org/developers/wayback-cdx-server.html)

## Acknowledgements

- Tristan Lee (Bellingcat's Data Scientist) for the idea of the application.
- Jessica Smith (Snowflake's Marketing Specialist) and Streamlit/Snowflake teams for the additional server resources on Streamlit Cloud.
- OSINT Community for recommending the application.
