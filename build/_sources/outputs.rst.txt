Outputs
==========

It is possible to save the CDX data in three formats. In the command line tool, these three formats are saved automatically.

HTML
--------

This format allows for easy viewing of the archived tweets, through the use of the ``iframe`` tag. Each tweet contains four viewing options, which render when clicking on the accordion:

- ``archived_tweet_url``: (`str`) The archived URL.

- ``parsed_archived_tweet_url``: (`str`) The archived URL after parsing. It is not guaranteed that this option will be archived, it is just a facilitator, as the originally archived URL does not always exist, due to changes in URLs and web services of the social network Twitter. Check the :ref:`utils`.

- ``original_tweet_url``: (`str`) The original tweet URL.

- ``parsed_tweet_url``: (`str`) The original tweet URL after parsing. Old URLs were archived in a nested manner. The parsing applied here unnests these URLs, when necessary.  Check the :ref:`utils`.

Additionally, other fields are displayed.

CSV
--------

Option to analyze the CDX data in comma-separated values.

JSON
--------

Option to analyze the data in JavaScript Object Notation.
