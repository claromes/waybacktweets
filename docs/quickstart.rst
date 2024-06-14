Quick Start
================

CLI
-------------

Using Wayback Tweets as a standalone command line tool

wbt [OPTIONS] USERNAME

$ ``wbt --from 2015-01-01 --to 2019-12-31 --limit 250 jack``


Module
-------------

Using Wayback Tweets as a Python Module

.. code-block:: python

    from waybacktweets import WaybackTweets
    from waybacktweets.utils import parse_date

    username = "jack"
    collapse = "urlkey"
    timestamp_from = parse_date("2015-01-01")
    timestamp_to = parse_date("2019-12-31")
    limit = 250
    offset = 0

    api = WaybackTweets(username, collapse, timestamp_from, timestamp_to, limit, offset)
    archived_tweets = api.get()
