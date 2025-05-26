Quickstart
================

CLI
-------------

Using Wayback Tweets as a standalone command line tool.

waybacktweets [OPTIONS] USERNAME

.. code-block:: shell

    waybacktweets --from 20150101 --to 20191231 --limit 250 jack

.. _module:

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

Web App
-------------

Using Wayback Tweets as a Streamlit Web App.

`Open the application <https://waybacktweets.streamlit.app>`_, a prototype written in Python with the Streamlit framework and hosted on Streamlit Cloud.
