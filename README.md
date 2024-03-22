# 🏛️ Wayback Tweets

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://waybacktweets.streamlit.app) [![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/claromes/waybacktweets?include_prereleases)](https://github.com/claromes/waybacktweets/releases)

Tool that displays, via [Wayback CDX Server API](https://github.com/internetarchive/wayback/tree/master/wayback-cdx-server), multiple archived tweets on Wayback Machine to avoid opening each link manually. The application is a prototype written in Python with the Streamlit framework and hosted on Streamlit Cloud, allowing users to apply filters based on specific years and view tweets that lack the original URL.

## Community

> "We're always delighted when we see our community members create tools for open source research." — [Bellingcat](https://twitter.com/bellingcat/status/1728085974138122604)

> "#myOSINTtip Clarissa Mendes launched a new tool for accessing old tweets via archive.org called the Wayback Tweets app. For those who love to look deeper at #osint tools, it is available on GitHub and uses the Wayback CDX Server API server (which is a hidden gem for accessing archive.org data!)" — [My OSINT Training](https://www.linkedin.com/posts/my-osint-training_myosinttip-osint-activity-7148425933324963841-0Q2n/)

> "Original way to find deleted tweets." — [Henk Van Ess](https://twitter.com/henkvaness/status/1693298101765701676)

> "This is an excellent tool to use now that most Twitter API-based tools have gone down with changes to the pricing structure over at X." — [The OSINT Newsletter - Issue #22](https://osintnewsletter.com/p/22#%C2%A7osint-community)

> "One of the keys to using the Wayback Machine effectively is knowing what it can and can’t archive. It can, and has, archived many, many Twitter accounts... Utilize fun tools such as Wayback Tweets to do so more effectively." — [Ari Ben Am](https://memeticwarfareweekly.substack.com/p/mww-paradise-by-the-telegram-dashboard)

> "Want to see archived tweets on Wayback Machine in bulk? You can use Wayback Tweets." — [Daily OSINT](https://twitter.com/DailyOsint/status/1695065018662855102)

> "Untuk mempermudah penelusuran arsip, gunakan Wayback Tweets." — [GIJN Indonesia](https://twitter.com/gijnIndonesia/status/1685912219408805888)

> "A tool to quickly view tweets saved on archive.org." — [Irina_Tech_Tips Newsletter #3](https://irinatechtips.substack.com/p/irina_tech_tips-newsletter-3-2023#%C2%A7wayback-tweets)

## Development

### Requirement

- Python 3.8+

### Installation

$ `git clone git@github.com:claromes/waybacktweets.git`

$ `cd waybacktweets`

$ `pip install -r requirements.txt`

$ `streamlit run app.py`

Streamlit will be served at http://localhost:8501

### Changelog

Check out the [releases](https://github.com/claromes/waybacktweets/releases).

### Todo (2024 planning)

- [ ] Code review
- [ ] UX review (filter before requesting)
- [ ] Add a calendar interface (Wayback Machine timestamp)
- [ ] Prevent duplicate URLs/Review the "Unique tweets" option
  - Counters
  - Collapsing
- [ ] Sorting in ascending and descending order
- [ ] Download dataset
- [ ] Fix `parse_links` exception
- [ ] Update Streamlit version
- [ ] Add metadata information
- [ ] Parse MIME types: `warc/revisit`, `text/plain`, `application/http`
- [ ] Documentation: Explain the mapping of archived URLs and the parsing process
- [ ] Create CLI
- [x] Pagination
  - [x] Footer
  - [x] Disabled/Empty states
- [x] Feedback
- [x] Review data cache
- [x] Changelog
- [x] Define range size by user
- [x] Filter by period/datetime
- [x] Add contributing guidelines

## Contributing

We welcome contributions from everyone, whether it's through bug reporting, feature suggestions or code contributions.

If you need help, or have ideas on improving this app, please open a new issue or reach out to support@claromes.com.

## Acknowledgements

- Tristan Lee (Bellingcat's Data Scientist) for the idea of the application.
- Jessica Smith (Snowflake's Marketing Specialist) and Streamlit/Snowflake teams for the additional server resources on Streamlit Cloud.
- OSINT Community for recommending the application.

> [!NOTE]
> If the application is down, please check the [Streamlit Cloud Status](https://www.streamlitstatus.com/).
