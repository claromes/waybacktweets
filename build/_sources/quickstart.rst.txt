Quickstart
================

CLI
-------------

Using Wayback Tweets as a standalone command line tool.

waybacktweets [OPTIONS] USERNAME

.. code-block:: shell

    waybacktweets --from 20150101 --to 20191231 --limit 250 jack

Web App
-------------

Using Wayback Tweets as a Streamlit Web App.

`Open the application <https://waybacktweets.streamlit.app>`_, a prototype written in Python with the Streamlit framework and hosted on Streamlit Cloud.

Module
-------------

Using Wayback Tweets as a Python Module.

.. code-block:: python

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
