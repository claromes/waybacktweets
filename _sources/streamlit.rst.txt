Web App
=========

The application is a prototype hosted on Streamlit Cloud, serving as an alternative to the command line tool.

`Open the application <https://waybacktweets.streamlit.app>`_.


Filters
----------

- Filtering by date range: Using the ``from`` and ``to`` filters

- Limit: Query result limits.

- Offset: Allows for a simple way to scroll through the results.

- Only unique Wayback Machine URLs: Filtering by the collapse option using the ``urlkey`` field and the URL Match Scope ``prefix``


Username Query Parameter
--------------------------

An alternative way to access the application is by using the ``username`` query parameter. This allows for automatic configuration of the Username input and automatically searches. Additionally, when the ``username`` parameter is sent, the accordion with the filters will already be open.

Example URL format:

``https://waybacktweets.streamlit.app?username=<USERNAME>``


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

Legacy App
-------------

To access the legacy version of Wayback Tweets `click here <https://waybacktweets-legacy.streamlit.app>`_.

.. note::

   If the application is down, please check the `Streamlit Cloud Status <https://www.streamlitstatus.com/>`_.

