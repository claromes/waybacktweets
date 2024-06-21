.. _field_options:

Field Options
================

The package performs several parses to facilitate the analysis of archived tweets and types of tweets. The fields below are available, which can be passed to the :ref:`parser` and :ref:`exporter`, in addition, the command line tool returns all these fields.

- ``archived_urlkey``: (`str`) A canonical transformation of the URL you supplied, for example, ``org,eserver,tc)/``. Such keys are useful for indexing.

- ``archived_timestamp``: (`str`) A 14 digit date-time representation in the ``YYYYMMDDhhmmss`` format.

- ``parsed_archived_timestamp``: (`str`) The ``archived_timestamp`` in human-readable format.

- ``archived_tweet_url``: (`str`) The archived URL.

- ``parsed_archived_tweet_url``: (`str`) The archived URL after parsing. It is not guaranteed that this option will be archived, it is just a facilitator, as the originally archived URL does not always exist, due to changes in URLs and web services of the social network Twitter. Check the :ref:`utils`.

- ``original_tweet_url``: (`str`) The original tweet URL.

- ``parsed_tweet_url``: (`str`) The original tweet URL after parsing. Old URLs were archived in a nested manner. The parsing applied here unnests these URLs, when necessary.  Check the :ref:`utils`.

- ``available_tweet_text``: (`str`) The tweet text extracted from the URL that is still available on the Twitter account.

- ``available_tweet_is_RT``: (`bool`) Whether the tweet from the ``available_tweet_text`` field is a retweet or not.

- ``available_tweet_info``: (`str`) Name and date of the tweet from the ``available_tweet_text`` field.

- ``archived_mimetype``: (`str`) The mimetype of the archived content, which can be one of these:

    - ``text/html``

    - ``warc/revisit``

    - ``application/json``

    - ``unk``

- ``archived_statuscode``: (`str`) The HTTP status code of the snapshot. If the mimetype is ``warc/revisit``, the value returned for the ``statuscode`` key can be blank, but the actual value is the same as that of any other entry that has the same ``digest`` as this entry. If the mimetype is ``application/json``, the value is usually empty or ``-``.

- ``archived_digest``: (`str`) The ``SHA1`` hash digest of the content, excluding the headers. It's usually a base-32-encoded string.

- ``archived_length``: (`int`) The compressed byte size of the corresponding WARC record, which includes WARC headers, HTTP headers, and content payload.
