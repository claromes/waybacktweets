Exceptions
================

These are the most common errors and are handled by the ``waybacktweets`` package.

ReadTimeoutError
------------------

This error occurs when a request to the web.archive.org server takes too long to respond. The server could be overloaded or there could be network issues.

The output message from the package would be: ``Connection to web.archive.org timed out.``

ConnectionError
------------------

This error is raised when the package fails to establish a new connection with web.archive.org. This could be due to network issues or the server being down.

The output message from the package would be: ``Failed to establish a new connection with web.archive.org. Max retries exceeded.``


This is the error often returned when performing experimental parsing of URLs with the mimetype ``application/json``.

The warning output message from the package would be: ``Connection error with https://web.archive.org/web/<TIMESTAMP>/https://twitter.com/<USERNAME>/status/<TWEET_ID>. Max retries exceeded. Error parsing the JSON, but the CDX data was saved.``

HTTPError
------------------

This error occurs when the Internet Archive services are temporarily offline. This could be due to maintenance or server issues.

The output message from the package would be: ``Temporarily Offline: Internet Archive services are temporarily offline. Please check Internet Archive Twitter feed (https://twitter.com/internetarchive) for the latest information.``

EmptyResponseError
---------------------

This exception raised for empty responses.

The output message from the package would be: ``No data was saved due to an empty response.``

Warning
------------------

It is possible to encounter the following warning when running the ``TweetsParser`` class (:ref:`parser`): ``<TWEET_URL> not available on the user's Twitter account, but the CDX data was saved.``

This occurs when the original tweet is no longer available on Twitter and has possibly been deleted.
