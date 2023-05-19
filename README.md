# 🏛️ Wayback Tweets

[![GitHub release (latest by date)](https://img.shields.io/github/v/release/claromes/waybacktweets)](https://github.com/claromes/waybacktweets/releases)

Archived tweets on Wayback Machine in a easy way

[waybacktweets.streamlit.app](https://waybacktweets.streamlit.app/)

*Thanks Tristan Lee for the idea.*

## Development

### Requirements

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
    - [ ] Check and add message if handle has no deleted tweets in the range
- [x] Pagination: set session variable on first click
- [x] Pagination: scroll to top
- [ ] Review data cache

## Roadmap

- [x] Pagination
    - [x] Footer
    - [x] Disabled/ Empty
- [ ] Feedbacks
- [ ] Prevent duplicate URLs
- [ ] Grid
- [ ] About
- [ ] Changelog