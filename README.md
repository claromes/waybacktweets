> [!IMPORTANT]
> If the application is down, please check the [Streamlit Cloud Status](https://www.streamlitstatus.com/).

<br>

# 🏛️ Wayback Tweets

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_red.svg)](https://waybacktweets.streamlit.app) [![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/claromes/waybacktweets?include_prereleases)](https://github.com/claromes/waybacktweets/releases) [![License](https://img.shields.io/github/license/claromes/waybacktweets)](https://github.com/claromes/waybacktweets/blob/main/LICENSE.md)


Tool that displays multiple archived tweets on Wayback Machine to avoid opening each link manually. Via [Wayback CDX Server API](https://github.com/internetarchive/wayback/tree/master/wayback-cdx-server).

<p align="center">
    <img src="assets/wbt-0.2.gif" width="500">
</p>

*Thanks Tristan Lee for the idea.*

## Features

- 30 tweets per page
- Filtering by only deleted tweets

## Development

### Requirement

- Python 3.8+

### Installation

$ `git clone git@github.com:claromes/waybacktweets.git`

$ `cd waybacktweets`

$ `pip install -r requirements.txt`

$ `streamlit run app.py`

Streamlit will be served at http://localhost:8501

## Bugs

- [ ] "web.archive.org took too long to respond."
- [x] `only_deleted` checkbox selected for handles without deleted tweets
- [x] Pagination: set session variable on first click
- [x] Pagination: scroll to top
- [x] `IndexError`
- [ ] Timeout error

## Roadmap

- [x] Pagination
    - [x] Footer
    - [x] Disabled/ Empty
- [x] Feedbacks
- [ ] Download dataset
- [x] Review data cache
- [x] Changelog
- [ ] Prevent duplicate URLs
- [ ] Range size defined by user
- [ ] `parse_links` exception
- [ ] Add current page to page title
- [ ] Parse MIME type `warc/revisit`
- [ ] Filter by period/datetime
- [ ] Apply filters by API endpoints
- [ ] Add contributing guidelines

## [Changelog](/CHANGELOG.md)
