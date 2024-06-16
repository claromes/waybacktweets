CLI
================

Usage
---------

.. click:: waybacktweets._cli:main
   :prog: waybacktweets
   :nested: full

Collapsing
------------

The Wayback Tweets command line tool recommends the use of three types of "collapse": ``urlkey``, ``digest``, and ``timestamp`` field.

- ``urlkey``: (`str`) A canonical transformation of the URL you supplied, for example, ``org,eserver,tc)/``. Such keys are useful for indexing.

- ``digest``: (`str`) The ``SHA1`` hash digest of the content, excluding the headers. It's usually a base-32-encoded string.

- ``timestamp``: (`datetime`) A 14 digit date-time representation in the ``YYYYMMDDhhmmss`` format. We recommend ``YYYYMMDD``.

However, it is possible to use it with other options. Read below text extracted from the official Wayback CDX Server API (Beta) documentation.

.. note::

   A new form of filtering is the option to "collapse" results based on a field, or a substring of a field. Collapsing is done on adjacent CDX lines where all captures after the first one that are duplicate are filtered out. This is useful for filtering out captures that are "too dense" or when looking for unique captures.

   To use collapsing, add one or more ``collapse=field`` or ``collapse=field:N`` where ``N`` is the first ``N`` characters of field to test.

   - Ex: Only show at most 1 capture per hour (compare the first 10 digits of the ``timestamp`` field). Given 2 captures ``20130226010000`` and ``20130226010800``, since first 10 digits ``2013022601`` match, the 2nd capture will be filtered out:

      http://web.archive.org/cdx/search/cdx?url=google.com&collapse=timestamp:10

      The calendar page at `web.archive.org` uses this filter by default: `http://web.archive.org/web/*/archive.org`

   - Ex: Only show unique captures by ``digest`` (note that only adjacent digest are collapsed, duplicates elsewhere in the cdx are not affected):

      http://web.archive.org/cdx/search/cdx?url=archive.org&collapse=digest

   - Ex: Only show unique urls in a prefix query (filtering out captures except first capture of a given url). This is similar to the old prefix query in wayback (note: this query may be slow at the moment):

      http://web.archive.org/cdx/search/cdx?url=archive.org&collapse=urlkey&matchType=prefix


URL Match Scope
-----------------

The CDX Server can return results matching a certain prefix, a certain host or all subdomains by using the ``matchType`` param.

The package ``waybacktweets`` uses the pathname ``/status`` followed by the wildcard '*' at the end of the URL to retrieve only tweets. However, if a value is provided for this parameter, the search will be made from the URL `twitter.com/<USERNAME>`.

Read below text extracted from the official Wayback CDX Server API (Beta) documentation.

.. note::

   For example, if given the url: archive.org/about/ and:

   - ``matchType=exact`` (default if omitted) will return results matching exactly archive.org/about/

   - ``matchType=prefix`` will return results for all results under the path archive.org/about/

      http://web.archive.org/cdx/search/cdx?url=archive.org/about/&matchType=prefix&limit=1000

   - ``matchType=host`` will return results from host archive.org

      http://web.archive.org/cdx/search/cdx?url=archive.org/about/&matchType=host&limit=1000

   - ``matchType=domain`` will return results from host archive.org and all subhosts \*.archive.org

      http://web.archive.org/cdx/search/cdx?url=archive.org/about/&matchType=domain&limit=1000

   The matchType may also be set implicitly by using wildcard '*' at end or beginning of the url:

   - If url is ends in '/\*', eg url=archive.org/\* the query is equivalent to url=archive.org/&matchType=prefix
   - If url starts with '\*.', eg url=\*.archive.org/ the query is equivalent to url=archive.org/&matchType=domain

   (Note: The domain mode is only available if the CDX is in `SURT <http://crawler.archive.org/articles/user_manual/glossary.html#surt>`_-order format.)
