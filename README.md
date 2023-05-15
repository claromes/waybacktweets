# 🏛️ Wayback Tweets

[![GitHub release (latest by date)](https://img.shields.io/github/v/release/claromes/waybacktweets)](https://github.com/claromes/waybacktweets/releases)

Archived tweets on Wayback Machine in a easy way

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
    - [ ] Add message

## Roadmap

- [ ] Pagination
    - [x] Footer
    - [x] Disabled/ Empty
    - [ ] Double click
- [ ] Feedbacks
- [ ] Prevent duplicate URLs
- [ ] Grid
- [ ] About/Pagination