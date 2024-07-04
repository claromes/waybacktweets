# Wayback Tweets

[![PyPI](https://img.shields.io/pypi/v/waybacktweets)](https://pypi.org/project/waybacktweets) [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.12528448.svg)](https://doi.org/10.5281/zenodo.12528448) [![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://waybacktweets.streamlit.app) [![Open In Collab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1zRqi6uTMiGi5z8GQ-PC0tbpCJWULCqMO?usp=sharing)


Retrieves archived tweets CDX data from the Wayback Machine, performs necessary parsing (see [Field Options](https://claromes.github.io/waybacktweets/field_options.html)), and saves the data in HTML, for easy viewing of the tweets using the iframe tags, CSV, and JSON formats.

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

### Using Wayback Tweets as a Web App

[Open the application](https://waybacktweets.streamlit.app), a prototype written in Python with the Streamlit framework and hosted on Streamlit Cloud.

### Using Wayback Tweets as a Python Module

```python
from waybacktweets import WaybackTweets, TweetsParser, TweetsExporter

USERNAME = "jack"

api = WaybackTweets(USERNAME)
archived_tweets = api.get()

if archived_tweets:
    field_options = [
        "archived_timestamp",
        "original_tweet_url",
        "archived_tweet_url",
        "archived_statuscode",
    ]

    parser = TweetsParser(archived_tweets, USERNAME, field_options)
    parsed_tweets = parser.parse()

    exporter = TweetsExporter(parsed_tweets, USERNAME, field_options)
    exporter.save_to_csv()
```

## Documentation

- [Wayback Tweets documentation](https://claromes.github.io/waybacktweets)
- [Wayback CDX Server API (Beta) documentation](https://archive.org/developers/wayback-cdx-server.html)

## Acknowledgements

- Tristan Lee (Bellingcat's Data Scientist) for the idea of the application.
- Jessica Smith (Snowflake's Community Growth Specialist) and Streamlit/Snowflake team for the additional server resources on Streamlit Cloud.
- OSINT Community for recommending the application.

> [!NOTE]
> If the Streamlit application is down, please check the [Streamlit Cloud Status](https://www.streamlitstatus.com/).
