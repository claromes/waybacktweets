API
====

Request
---------

.. module:: waybacktweets.api.request_tweets

.. autoclass:: WaybackTweets
    :members:



Parse
---------

.. module:: waybacktweets.api.parse_tweets

.. autoclass:: TweetsParser
    :members:

.. autoclass:: TwitterEmbed
    :members:

.. TODO: JSON Issue
.. .. autoclass:: JsonParser
..     :members:


Export
---------

.. module:: waybacktweets.api.export_tweets

.. autoclass:: TweetsExporter
    :members:


Visualizer
-----------

.. module:: waybacktweets.api.viz_tweets

.. autoclass:: HTMLTweetsVisualizer
    :members:


Utils
-------

.. module:: waybacktweets.utils.utils

.. autofunction:: check_double_status
.. autofunction:: check_pattern_tweet
.. autofunction:: clean_tweet_url
.. autofunction:: clean_wayback_machine_url
.. autofunction:: delete_tweet_pathnames
.. autofunction:: get_response
.. autofunction:: parse_date
.. autofunction:: semicolon_parser
