.. note::
    The current version of the Web App is 0.4.3. Version 1.0 has not yet been implemented in the Streamlit Web App, as it is in the review and testing phase.

Web App
=========

Aplication that displays multiple archived tweets on Wayback Machine to avoid opening each link manually. The application is a prototype written in Python with the Streamlit framework and hosted on Streamlit Cloud, allowing users to apply filters and view tweets that lack the original URL.

`Open the application <https://waybacktweets.streamlit.app>`_.


Filters
----------
- Filtering by date range: Using the ``from`` and ``to`` filters

- Only unavailable tweets: Checks if the archived URL still exists on Twitter (see the :ref:`flowchart`)

- Only unique Wayback Machine URLs: Filtering by the collapse option using the ``urlkey`` field and the URL Match Scope ``prefix``


Pagination
------------

Pagination allows viewing up to 25 tweets per page. This helps to avoid rate limiting from the API, for parsing returns with the mimetype ``application/json``.


Community Comments
--------------------

.. raw:: html

   <ul>
        <li>"We're always delighted when we see our community members create tools for open source research." <a href="https://twitter.com/bellingcat/status/1728085974138122604" target="_blank">Bellingcat</a></li>
        <br>
        <li>"#myOSINTtip Clarissa Mendes launched a new tool for accessing old tweets via archive.org called the Wayback Tweets app. For those who love to look deeper at #osint tools, it is available on GitHub and uses the Wayback CDX Server API server (which is a hidden gem for accessing archive.org data!)" <a href="https://www.linkedin.com/posts/my-osint-training_myosinttip-osint-activity-7148425933324963841-0Q2n/" target="_blank">My OSINT Training</a></li>
        <br>
        <li>"Original way to find deleted tweets." <a href="https://twitter.com/henkvaness/status/1693298101765701676" target="_blank">Henk Van Ess</a></li>
        <br>
        <li>"This is an excellent tool to use now that most Twitter API-based tools have gone down with changes to the pricing structure over at X." <a href="https://osintnewsletter.com/p/22#%C2%A7osint-community" target="_blank">The OSINT Newsletter - Issue #22</a></li>
        <br>
        <li>"One of the keys to using the Wayback Machine effectively is knowing what it can and can't archive. It can, and has, archived many, many Twitter accounts... Utilize fun tools such as Wayback Tweets to do so more effectively." <a href="https://memeticwarfareweekly.substack.com/p/mww-paradise-by-the-telegram-dashboard" target="_blank">Ari Ben Am</a></li>
        <br>
        <li>"Want to see archived tweets on Wayback Machine in bulk? You can use Wayback Tweets." <a href="https://twitter.com/DailyOsint/status/1695065018662855102" target="_blank">Daily OSINT</a></li>
        <br>
        <li>"Untuk mempermudah penelusuran arsip, gunakan Wayback Tweets." <a href="https://twitter.com/gijnIndonesia/status/1685912219408805888" target="_blank">GIJN Indonesia</a></li>
        <br>
        <li>"A tool to quickly view tweets saved on archive.org." <a href="https://irinatechtips.substack.com/p/irina_tech_tips-newsletter-3-2023#%C2%A7wayback-tweets" target="_blank">Irina_Tech_Tips Newsletter #3</a></li>
        <br>
    </ul>

.. note::

   If the application is down, please check the `Streamlit Cloud Status <https://www.streamlitstatus.com/>`_.

