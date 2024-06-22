from datetime import datetime

import streamlit as st
import streamlit.components.v1 as components

from waybacktweets.api.export import TweetsExporter
from waybacktweets.api.parse import JsonParser, TweetsParser
from waybacktweets.api.request import WaybackTweets
from waybacktweets.config.config import config

# Initial Settings

LOGO = "assets/parthenon.png"
TITLE = "assets/waybacktweets.png"
FIELD_OPTIONS = [
    "parsed_archived_timestamp",
    "archived_tweet_url",
    "parsed_archived_tweet_url",
    "original_tweet_url",
    "parsed_tweet_url",
    "available_tweet_text",
    "available_tweet_is_RT",
    "available_tweet_info",
    "archived_mimetype",
    "archived_statuscode",
]

st.set_page_config(
    page_title="Wayback Tweets",
    page_icon=LOGO,
    layout="centered",
    menu_items={
        "About": f"""
    [![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/claromes/waybacktweets?include_prereleases)](https://github.com/claromes/waybacktweets/releases) [![License](https://img.shields.io/github/license/claromes/waybacktweets)](https://github.com/claromes/waybacktweets/blob/main/LICENSE.md) [![Star](https://img.shields.io/github/stars/claromes/waybacktweets?style=social)](https://github.com/claromes/waybacktweets)

    Application that displays multiple archived tweets on Wayback Machine to avoid opening each link manually.

    The application is a prototype hosted on Streamlit Cloud, allowing users to apply filters and view tweets that lack the original URL. [Read more](https://claromes.github.io/waybacktweets/streamlit.html).

    © 2023 - {datetime.now().year}, [Claromes](https://claromes.com) · Icon by The Doodle Library · Title font by Google, licensed under the Open Font License

    ---
""",  # noqa: E501
        "Report a bug": "https://github.com/claromes/waybacktweets/issues",
    },
)

# https://discuss.streamlit.io/t/remove-hide-running-man-animation-on-top-of-page/21773/3
st.html(
    """
<style>
    header[data-testid="stHeader"] {
        opacity: 0.5;
    }
     iframe {
        border: 1px solid #dddddd;
        border-radius: 0.5rem;
    }
    div[data-testid="InputInstructions"] {
        visibility: hidden;
    }
    img[data-testid="stLogo"] {
        scale: 4;
        padding-left: 10px;
    }
    button[data-testid="StyledFullScreenButton"] {
        display: none;
    }
</style>
"""
)

if "current_username" not in st.session_state:
    st.session_state.current_username = ""

if "prev_disabled" not in st.session_state:
    st.session_state.prev_disabled = False

if "next_disabled" not in st.session_state:
    st.session_state.next_disabled = False

if "next_button" not in st.session_state:
    st.session_state.next_button = False

if "prev_button" not in st.session_state:
    st.session_state.prev_button = False

if "update_component" not in st.session_state:
    st.session_state.update_component = 0

if "offset" not in st.session_state:
    st.session_state.offset = 0

if "count" not in st.session_state:
    st.session_state.count = False

start_date = datetime(2006, 1, 1)
end_date = datetime.now()

if "archived_timestamp_filter" not in st.session_state:
    st.session_state.archived_timestamp_filter = (start_date, end_date)


# Verbose mode configuration

config.verbose = True


# Pagination Settings


def scroll_into_view():
    script = f"""
    <script>
        window.parent.document.querySelector('section.main').scrollTo(0, 0);
        let update_component = {st.session_state.update_component}
    </script>
    """

    components.html(script, width=0, height=0)


def prev_page():
    st.session_state.offset -= tweets_per_page

    st.session_state.update_component += 1
    scroll_into_view()


def next_page():
    st.session_state.offset += tweets_per_page

    st.session_state.update_component += 1
    scroll_into_view()


# Requesting


@st.cache_data(ttl=1800, show_spinner=False)
def wayback_tweets(
    username,
    collapse,
    timestamp_from,
    timestamp_to,
    limit,
    offset,
    matchtype,
):
    response = WaybackTweets(
        username,
        collapse,
        timestamp_from,
        timestamp_to,
        limit,
        offset,
        matchtype,
    )
    archived_tweets = response.get()

    return archived_tweets


@st.cache_data(ttl=1800, show_spinner=False)
def tweets_parser(archived_tweets, field_options):
    parser = TweetsParser(archived_tweets, username, field_options)
    parsed_tweets = parser.parse()

    return parsed_tweets


@st.cache_data(ttl=1800, show_spinner=False)
def tweets_exporter(parsed_tweets, username, field_options):
    exporter = TweetsExporter(parsed_tweets, username, field_options)

    df = exporter.dataframe

    return df


@st.cache_data(ttl=1800, show_spinner=False)
def tweets_json_parser():
    if archived_mimetype[i] == "application/json":
        json_parser = JsonParser(parsed_archived_tweet_url[i])
        text_json = json_parser.parse()

        if text_json:
            return text_json

        return None


def display_tweet_header():
    header = st.markdown(
        f"[**archived url ↗**]({archived_tweet_url[i]}) · [**tweet url ↗**]({original_tweet_url[i]}) · **mimetype:** {archived_mimetype[i]} · **archived timestamp:** {parsed_archived_timestamp[i]} · **archived status code:** {archived_statuscode[i]}"  # noqa: E501
    )

    return header


def display_tweet_iframe():
    tweet_iframe = components.iframe(
        archived_tweet_url[i],
        height=500,
        scrolling=True,
    )

    return tweet_iframe


# Interface Settings

st.logo(LOGO)

st.success(
    """**v1.0 🎉: CLI and Python Module**

$ `pip install waybacktweets`

$ `waybacktweets --from 20150101 --to 20191231 --limit 250 jack`

Retrieve archived tweets CDX data in CSV, JSON, and HTML formats using the command line.

Read the documentation: [claromes.github.io/waybacktweets](https://claromes.github.io/waybacktweets)."""  # noqa: E501
)

st.image(TITLE, use_column_width="never")
st.caption(
    "[![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/claromes/waybacktweets?include_prereleases)](https://github.com/claromes/waybacktweets/releases) [![Star](https://img.shields.io/github/stars/claromes/waybacktweets?style=social)](https://github.com/claromes/waybacktweets)"  # noqa: E501
)
st.caption("Display multiple archived tweets on Wayback Machine.")
st.caption(
    "Download data via command line with the [`waybacktweets`](https://pypi.org/project/waybacktweets) Python package."  # noqa: E501
)

username = st.text_input("Username", placeholder="Without @")

start_date = datetime(2006, 1, 1)
end_date = datetime.now()

st.session_state.archived_timestamp_filter = st.date_input(
    "Tweets saved between",
    (start_date, end_date),
    start_date,
    end_date,
    format="YYYY/MM/DD",
    help="Using the `from` and `to` filters. Format: YYYY/MM/DD",
)

not_available = st.checkbox(
    "Only tweets not available",
    help="Checks if the archived URL still exists on Twitter",
)

unique = st.checkbox(
    "Only unique Wayback Machine URLs",
    help="Filtering by the collapse option using the `urlkey` field and the URL Match Scope `prefix`",  # noqa: E501
)

query = st.button("Query", type="primary", use_container_width=True)

# Tweet Listing Settings

if username != st.session_state.current_username:
    st.session_state.current_username = username
    st.session_state.offset = 0

if query or st.session_state.count:
    tweets_per_page = 25

    collapse = None
    matchType = None

    if unique:
        collapse = "urlkey"
        matchType = "prefix"

    try:
        with st.spinner("Waybacking..."):
            wayback_tweets = wayback_tweets(
                st.session_state.current_username,
                collapse,
                st.session_state.archived_timestamp_filter[0],
                st.session_state.archived_timestamp_filter[1],
                tweets_per_page,
                st.session_state.offset,
                matchType,
            )

            parsed_tweets = tweets_parser(wayback_tweets, FIELD_OPTIONS)
            df = tweets_exporter(
                parsed_tweets, st.session_state.current_username, FIELD_OPTIONS
            )

            st.session_state.count = len(df)

            # st.caption(
            #     "The number of tweets per page is set to 25, and this is a fixed value due to the API rate limit."  # noqa: E501
            # )
            # st.write(f"**{st.session_state.count} URLs have been captured**")

            if st.session_state.count:
                if tweets_per_page > st.session_state.count:
                    tweets_per_page = st.session_state.count

            # Tweet Listing Processing

            progress = st.empty()

            parsed_archived_timestamp = df["parsed_archived_timestamp"]
            archived_tweet_url = df["archived_tweet_url"]
            parsed_archived_tweet_url = df["parsed_archived_tweet_url"]
            original_tweet_url = df["original_tweet_url"]
            parsed_tweet_url = df["parsed_tweet_url"]
            available_tweet_text = df["available_tweet_text"]
            available_tweet_is_RT = df["available_tweet_is_RT"]
            available_tweet_info = df["available_tweet_info"]
            archived_mimetype = df["archived_mimetype"]
            archived_statuscode = df["archived_statuscode"]

            st.divider()
            st.session_state.current_username = username

            return_none_count = 0

            start_index = st.session_state.offset
            end_index = min(st.session_state.count, start_index + tweets_per_page)

            for i in range(tweets_per_page):
                try:
                    parsed_text_json = tweets_json_parser()

                    # Display all tweets
                    if not not_available:
                        # Display available tweets
                        if available_tweet_text[i]:
                            display_tweet_header()

                            if available_tweet_is_RT[i]:
                                st.info("*Retweet*")

                            st.write(available_tweet_text[i])
                            st.write(f"**{available_tweet_info[i]}**")

                            st.divider()
                        # Display tweets not available with text/html, unk, warc/revisit mimetype or application/json mimetype without parsed JSON text # noqa: E501
                        elif (
                            archived_mimetype[i] != "application/json"
                            and not available_tweet_text[i]
                        ):
                            display_tweet_header()
                            if (
                                ".jpg" in parsed_tweet_url[i]
                                or ".png" in parsed_tweet_url[i]
                            ) and (400 <= archived_statuscode[i] <= 511):
                                display_tweet_iframe()
                            elif "/status/" not in parsed_tweet_url[i]:
                                st.info(
                                    "This isn't a status or is not available"  # noqa: E501
                                )
                            elif (
                                f"{st.session_state.current_username}"
                                not in parsed_tweet_url[i]
                            ):
                                st.info(
                                    f"Replying to {st.session_state.current_username}"  # noqa: E501
                                )
                            else:
                                display_tweet_iframe()

                            st.divider()
                        # Display tweets not available with application/json mimetype and parsed JSON text # noqa: E501
                        elif (
                            archived_mimetype[i] == "application/json"
                            and not available_tweet_text[i]
                        ):
                            display_tweet_header()
                            st.code(parsed_text_json)

                            st.divider()

                    # Display only tweets not available
                    if not_available:
                        # Display tweets not available with text/html, unk, warc/revisit return # noqa: E501
                        if (
                            archived_mimetype[i] != "application/json"
                            and not available_tweet_text[i]
                        ):
                            return_none_count += 1

                            display_tweet_header()
                            if (
                                ".jpg" in parsed_tweet_url[i]
                                or ".png" in parsed_tweet_url[i]
                            ) and (400 <= archived_statuscode[i] <= 511):
                                display_tweet_iframe()
                            elif "/status/" not in parsed_tweet_url[i]:
                                st.info(
                                    "This isn't a status or is not available"  # noqa: E501
                                )
                            elif (
                                f"{st.session_state.current_username}"
                                not in parsed_tweet_url[i]
                            ):
                                st.info(
                                    f"Replying to {st.session_state.current_username}"  # noqa: E501
                                )
                            else:
                                display_tweet_iframe()

                            st.divider()

                        # Display tweets not available with application/json return # noqa: E501
                        elif (
                            archived_mimetype[i] == "application/json"
                            and not available_tweet_text[i]
                        ):
                            return_none_count += 1

                            display_tweet_header()
                            st.code(parsed_text_json)

                            st.divider()

                        progress.write(
                            f"{return_none_count} URLs have been captured in the range {start_index}-{end_index}"  # noqa: E501
                        )
                except IndexError:
                    if start_index <= 0:
                        st.session_state.prev_disabled = True
                    else:
                        st.session_state.prev_disabled = False

                    st.session_state.next_disabled = True

            prev, _, next = st.columns([3, 4, 3])

        prev.button(
            "Previous",
            disabled=st.session_state.prev_disabled,
            key="prev_button_key",
            on_click=prev_page,
            type="primary",
            use_container_width=True,
        )
        next.button(
            "Next",
            disabled=st.session_state.next_disabled,
            key="next_button_key",
            on_click=next_page,
            type="primary",
            use_container_width=True,
        )

        if not wayback_tweets:
            st.error(
                "Failed to establish a new connection with web.archive.org. Max retries exceeded. Please wait a few minutes and try again."  # noqa: E501
            )
    except TypeError as e:
        st.error(
            f"""
        {e}. Refresh this page and try again.

        If the problem persists [open an issue](https://github.com/claromes/waybacktweets/issues)."""  # noqa: E501
        )
        st.session_state.offset = 0
    except Exception as e:
        st.error(f"{e}")
        st.stop()