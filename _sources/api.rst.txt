API
====

Config
------------

.. automodule:: waybacktweets.config.config
    :members:


Exceptions
------------

.. automodule:: waybacktweets.exceptions.exceptions

.. autoclass:: ReadTimeoutError
    :members:

.. autoclass:: ConnectionError
    :members:

.. autoclass:: HTTPError
    :members:

.. autoclass:: EmptyResponseError
    :members:

.. autoclass:: GetResponseError
    :members:


Export
---------

.. automodule:: waybacktweets.api.export

.. autoclass:: TweetsExporter
    :members:


Parse
---------

.. automodule:: waybacktweets.api.parse

.. autoclass:: TweetsParser
    :members:

.. autoclass:: TwitterEmbed
    :members:

.. autoclass:: JsonParser
    :members:


Request
---------

.. automodule:: waybacktweets.api.request

.. autoclass:: WaybackTweets
    :members:


Utils
-------

.. automodule:: waybacktweets.utils.utils

.. autofunction:: check_double_status
.. autofunction:: check_pattern_tweet
.. autofunction:: clean_tweet_url
.. autofunction:: clean_wayback_machine_url
.. autofunction:: delete_tweet_pathnames
.. autofunction:: get_response
.. autofunction:: is_tweet_url
.. autofunction:: semicolon_parser


Visualizer
-----------

.. automodule:: waybacktweets.api.visualize

.. autoclass:: HTMLTweetsVisualizer
    :members:
