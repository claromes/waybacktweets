# Changelog

## [v0.4.3](https://github.com/claromes/waybacktweets/releases/tag/v0.4.3) - 2023-12-13
- Add:
  - 8-digit collapsing strategy (one capture per day)
  - Messages about collapsing strategy and number of tweets displayed

## [v0.4.2](https://github.com/claromes/waybacktweets/releases/tag/v0.4.2) - 2023-12-13
- Add:
  - Parse tweet URLs to delete `/photos`, `/likes`, `/retweets` and other sub-endpoints
    - Only for "original url"

## [v0.4.1](https://github.com/claromes/waybacktweets/releases/tag/v0.4.1) - 2023-12-13
- Add:
  - Warning message for non 200/300 status code
- Update:
  - Set a fixed tweets per page (25) due the API rate limit

## [v0.4](https://github.com/claromes/waybacktweets/releases/tag/v0.4) - 2023-12-13
- Add:
  - Parse old tweets URLs
      - Picture: `twimg.com`
      - Reply `username/status/"/user_reply/status/user_reply_msg_ID"`
  - Allows MIME type `warc/revisit` and `unk` (**to be reviewed**)

- Update:
  - Change filter text "Only deleted tweets" to "Original URLs not available" with a help info
  - Change "tweet" text to "original link" on each header

## [v0.3](https://github.com/claromes/waybacktweets/releases/tag/v0.3) - 2023-11-13
- Add:
  - Add filter by year
  - Add filter by range size 
  - Add spinner to load data
  - Add f-string to code

- Update:
  - Streamlit version to 1.27.0
  - Style (font, BG color)
  - README
  - Fix MIME type display logic
  - Fix pagination
  - Fix error messages
  - Fix JSON response

- Delete:
  Progress bar

## [v0.2](https://github.com/claromes/waybacktweets/releases/tag/v0.2) - 2023-08-16
- Displays tweets as text
- Displays RTs info
- Displays JSON MIME type as JSON (if tweet was deleted)
- Adds progress bar
- Adds warning to `warc/revisit` MIME type
- Improves code quality
- Screenshot tests as an alternative to `iframe`
  - Keeps `iframe`
  - Each website screenshot takes too long

## [v0.1.4](https://github.com/claromes/waybacktweets/releases/tag/v0.1.4) - 2023-07-21
- Add Pagination via CDX Server API
- Update theme/ style
- Update about
- Decrease tweets per page (30)
- Fix `cache_data`

## [v0.1.3.2](https://github.com/claromes/waybacktweets/releases/tag/v0.1.3.2) - 2023-06-04
- Update Streamlit version

## [v0.1.3.1](https://github.com/claromes/waybacktweets/releases/tag/v0.1.3.1) - 2023-06-01
- Add `cache_data`

## [v0.1.3](https://github.com/claromes/waybacktweets/releases/tag/v0.1.3) - 2023-05-31
- Fix TypeError 'NoneType'

## [v0.1.2.1](https://github.com/claromes/waybacktweets/releases/tag/v0.1.2.1) - 2023-05-27
- Fix range

## [v0.1.2](https://github.com/claromes/waybacktweets/releases/tag/v0.1.2) - 2023-05-19
- Increase tweets per page (100)
- Increase iframe height
- Fix "Only deleted tweets" msg

## [v0.1.1](https://github.com/claromes/waybacktweets/releases/tag/v0.1.1) - 2023-05-19
- Fix scroll to top

## [v0.1.0](https://github.com/claromes/waybacktweets/releases/tag/v0.1.0) - 2023-05-19
- Add Pagination

## [v0.0.2](https://github.com/claromes/waybacktweets/releases/tag/v0.0.2) - 2023-05-12
- Minor bugs

## [v0.0.1](https://github.com/claromes/waybacktweets/releases/tag/v0.0.1) - 2023-05-11
- Initial commit
