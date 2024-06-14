CLI
================

Usage
---------

.. click:: waybacktweets.cli.main:cli
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
