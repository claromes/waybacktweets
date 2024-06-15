Quickstart
================

CLI
-------------

Using Wayback Tweets as a standalone command line tool

waybacktweets [OPTIONS] USERNAME

.. code-block:: shell

    waybacktweets --from 20150101 --to 20191231 --limit 250 jack`


Module
-------------

Using Wayback Tweets as a Python Module

.. code-block:: python

    from waybacktweets import WaybackTweets
    from waybacktweets.utils import parse_date

    username = "jack"
    collapse = "urlkey"
    timestamp_from = parse_date("20150101")
    timestamp_to = parse_date("20191231")
    limit = 250
    offset = 0
    matchtype = "exact"

    api = WaybackTweets(username, collapse, timestamp_from, timestamp_to, limit, offset, matchtype)

    archived_tweets = api.get()

Web App
-------------

Using Wayback Tweets as a Streamlit Web App

`Access the application <https://waybacktweets.streamlit.app>`_, a prototype written in Python with the Streamlit framework and hosted on Streamlit Cloud.
