API
====

Request
---------

.. automodule:: waybacktweets.api.request

.. autoclass:: WaybackTweets
    :members:

Parse
---------

.. automodule:: waybacktweets.api.parse

.. autoclass:: TweetsParser
    :members:
    :private-members:

.. autoclass:: TwitterEmbed
    :members:

.. autoclass:: JsonParser
    :members:

Export
---------

.. automodule:: waybacktweets.api.export

.. autoclass:: TweetsExporter
    :members:
    :private-members:

Visualize
-----------

.. automodule:: waybacktweets.api.visualize

.. autoclass:: HTMLTweetsVisualizer
    :members:
    :private-members:

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

Config
------------

.. automodule:: waybacktweets.config.config
    :members:
