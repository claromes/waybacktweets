Result
================

The package saves in three formats: CSV, JSON, and HTML. The files have the following fields:

- ``archived_urlkey``: (`str`) A canonical transformation of the URL you supplied, for example, ``org,eserver,tc)/``. Such keys are useful for indexing.

- ``archived_timestamp``: (`datetime`) A 14 digit date-time representation in the ``YYYYMMDDhhmmss`` format.

- ``original_tweet_url``: (`str`) The original tweet URL.

- ``archived_tweet_url``: (`str`) The original archived URL.

- ``parsed_tweet_url``: (`str`) The original tweet URL after parsing. `Check the utility functions <api.html#module-waybacktweets.utils.utils>`_.

- ``parsed_archived_tweet_url``: (`str`) The original archived URL after parsing. `Check the utility functions <api.html#module-waybacktweets.utils.utils>`_.

- ``parsed_tweet_text_mimetype_json``: (`str`) The tweet text extracted from the archived URL that has mimetype ``application/json``.

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
