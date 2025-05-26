# Wayback Tweets

[![PyPI](https://img.shields.io/pypi/v/waybacktweets)](https://pypi.org/project/waybacktweets) [![PyPI Downloads](https://static.pepy.tech/badge/waybacktweets)](https://pepy.tech/projects/waybacktweets)

Retrieves archived tweets CDX data from the Wayback Machine, performs necessary parsing (see [Field Options](https://waybacktweets.claromes.com/field_options)), and saves the data in HTML, for easy viewing of the tweets using the iframe tags, CSV, and JSON formats.

## Installation

It is compatible with Python versions 3.10 and above. [See installation options](https://waybacktweets.claromes.com/installation).

```shell
pipx install waybacktweets
```

## CLI

```shell
Usage:
  waybacktweets [OPTIONS] USERNAME
  USERNAME: The Twitter username without @

Options:
  -c, --collapse [urlkey|digest|timestamp:xx]
                                  Collapse results based on a field, or a
                                  substring of a field. XX in the timestamp
                                  value ranges from 1 to 14, comparing the
                                  first XX digits of the timestamp field. It
                                  is recommended to use from 4 onwards, to
                                  compare at least by years.
  -f, --from DATE                 Filtering by date range from this date.
                                  Format: YYYYmmdd
  -t, --to DATE                   Filtering by date range up to this date.
                                  Format: YYYYmmdd
  -l, --limit INTEGER             Query result limits.
  -rk, --resumption_key TEXT      Allows for a simple way to scroll through
                                  the results. Key to continue the query from
                                  the end of the previous query.
  -mt, --matchtype [exact|prefix|host|domain]
                                  Results matching a certain prefix, a certain
                                  host or all subdomains.
  -v, --verbose                   Shows the log.
  --version                       Show the version and exit.
  -h, --help                      Show this message and exit.

Examples:
  waybacktweets jack
  waybacktweets --from 20200305 --to 20231231 --limit 300 --verbose jack

Repository:
  https://github.com/claromes/waybacktweets

Documentation:
  https://waybacktweets.claromes.com
```

## Module

[![Open In Collab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1tnaM3rMWpoSHBZ4P_6iHFPjraWRQ3OGe?usp=sharing)

```python
from waybacktweets import WaybackTweets, TweetsParser, TweetsExporter

USERNAME = "jack"

api = WaybackTweets(USERNAME)
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

    parser = TweetsParser(archived_tweets, USERNAME, field_options)
    parsed_tweets = parser.parse()

    exporter = TweetsExporter(parsed_tweets, USERNAME, field_options)
    exporter.save_to_csv()
    exporter.save_to_json()
    exporter.save_to_html()
```

## Web App

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://waybacktweets.streamlit.app)

A prototype written in Python with the Streamlit framework and hosted on Streamlit Cloud.

Important: Starting from version 1.0, the web app will no longer receive all updates from the official package. To access all features, prefer using the package from PyPI.

## Documentation

- [Wayback Tweets documentation](https://waybacktweets.claromes.com/).
- [Wayback CDX Server API (Beta) documentation](https://archive.org/developers/wayback-cdx-server.html).

## Acknowledgements

- Tristan Lee (Bellingcat's Data Scientist) for the idea.
- Jessica Smith (Snowflake's Community Growth Specialist) and Streamlit team for the additional server resources on Streamlit Cloud.
- OSINT Community for recommending the package and the application.

## License

[GPL-3.0](LICENSE.md)
