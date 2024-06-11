import datetime

import requests
import streamlit as st
import streamlit.components.v1 as components

from waybacktweets.export_tweets import TweetsExporter
from waybacktweets.parse_tweets import TweetsParser
from waybacktweets.request_tweets import WaybackTweets
from waybacktweets.utils import check_double_status

# Initial Settings

LOGO = "app/assets/parthenon.svg"

st.set_page_config(
    page_title="Wayback Tweets",
    page_icon=LOGO,
    layout="centered",
    menu_items={
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
        scale: 3;
        padding-left: 10px;
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

start_date = datetime.datetime(2006, 3, 1)
end_date = datetime.datetime.now()

if "archived_timestamp_filter" not in st.session_state:
    st.session_state.archived_timestamp_filter = (start_date, end_date)


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
def tweets_count(username, archived_timestamp_filter):
    url = f"https://web.archive.org/cdx/search/cdx?url=https://twitter.com/{username}/status/*&collapse=timestamp:8&output=json&from={archived_timestamp_filter[0]}&to={archived_timestamp_filter[1]}"  # noqa: E501

    try:
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            if data and len(data) > 1:
                total_tweets = len(data) - 1
                return total_tweets
            else:
                return 0
    except requests.exceptions.Timeout:
        st.error("Connection to web.archive.org timed out.")
        st.stop()
    except requests.exceptions.ConnectionError:
        st.error("Failed to establish a new connection with web.archive.org.")
        st.stop()
    except UnboundLocalError:
        st.empty()


# Interface Settings


st.logo(LOGO)

st.success(
    """**New Feature: CLI**

You can now retrieve archived tweets using the Wayback Tweets command line tool.
Download the archived tweets' CDX data in CSV, JSON, and HTML formats.

For more details, [read the documentation](https://github.com/claromes/waybacktweets)."""  # noqa: E501
)

st.title(
    "Wayback Tweets",
    anchor=False,
)
st.caption(
    "[![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/claromes/waybacktweets?include_prereleases)](https://github.com/claromes/waybacktweets/releases) [![Star](https://img.shields.io/github/stars/claromes/waybacktweets?style=social)](https://github.com/claromes/waybacktweets)"  # noqa: E501
)
st.caption("Display multiple archived tweets on Wayback Machine")

username = st.text_input("Username", placeholder="Without @")

start_date = datetime.datetime(2006, 3, 1)
end_date = datetime.datetime.now()

st.session_state.archived_timestamp_filter = st.date_input(
    "Tweets saved between",
    (start_date, end_date),
    start_date,
    end_date,
    format="YYYY/MM/DD",
    help="YYYY/MM/DD",
)

not_available = st.checkbox("Only tweets not available")

unique = st.checkbox(
    "Only unique URLs",
    help="Filtering by the collapse option using the urlkey field",
)

query = st.button("Query", type="primary", use_container_width=True)

# Tweet Listing Settings


if username != st.session_state.current_username:
    st.session_state.current_username = username
    st.session_state.offset = 0

if query or st.session_state.count:
    tweets_per_page = 25

    st.session_state.count = tweets_count(
        username, st.session_state.archived_timestamp_filter
    )

    st.caption(
        "The search optimization uses an 8-digit [collapsing strategy](https://github.com/internetarchive/wayback/blob/master/wayback-cdx-server/README.md?ref=hackernoon.com#collapsing), refining the captures to one per day. The number of tweets per page is set to 25, and this is a fixed value due to the API rate limit."  # noqa: E501
    )
    st.write(f"**{st.session_state.count} URLs have been captured**")

    if st.session_state.count:
        if tweets_per_page > st.session_state.count:
            tweets_per_page = st.session_state.count

    try:
        progress = st.empty()

        # Tweet Listing Processing

        response = WaybackTweets(
            username,
            unique,
            st.session_state.archived_timestamp_filter[0],
            st.session_state.archived_timestamp_filter[1],
            tweets_per_page,
        )
        archived_tweets = response.get()

        with st.spinner("Parsing..."):
            if archived_tweets:
                field_options = [
                    "archived_urlkey",
                    "archived_timestamp",
                    "original_tweet_url",
                    "archived_tweet_url",
                    "parsed_tweet_url",
                    "parsed_archived_tweet_url",
                    "parsed_tweet_text_mimetype_json",
                    "available_tweet_text",
                    "available_tweet_is_RT",
                    "available_tweet_info",
                    "archived_mimetype",
                    "archived_statuscode",
                ]

                parser = TweetsParser(archived_tweets, username, field_options)
                parsed_tweets = parser.parse()

                exporter = TweetsExporter(parsed_tweets, username, field_options)
                df = exporter.dataframe

                # file_path = "claromes_tweets_20240610210338.csv"
                # df = pd.read_csv(file_path)
                # df = df.fillna("")

                archived_urlkey = df["archived_urlkey"]
                archived_timestamp = df["archived_timestamp"]
                original_tweet_url = df["original_tweet_url"]
                archived_tweet_url = df["archived_tweet_url"]
                parsed_tweet_url = df["parsed_tweet_url"]
                parsed_archived_tweet_url = df["parsed_archived_tweet_url"]
                parsed_tweet_text_mimetype_json = df["parsed_tweet_text_mimetype_json"]
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
                        if original_tweet_url[i]:

                            # Display all tweets
                            if not not_available:
                                st.markdown(
                                    f'{i+1 + st.session_state.offset}. [**archived url ↗**]({archived_tweet_url[i]}) · [**tweet url ↗**]({original_tweet_url[i]}) · **MIME type:** {archived_mimetype[i]} · **archived timestamp:** {datetime.datetime.strptime(str(archived_timestamp[i]), "%Y%m%d%H%M%S")} · **archived status code:** {archived_statuscode[i]}'  # noqa: E501
                                )

                                # Display available tweets
                                if available_tweet_text[i]:
                                    if available_tweet_is_RT[i]:
                                        st.info("*Retweet*")

                                    st.write(available_tweet_text[i])
                                    st.write(f"**{available_tweet_info[i]}**")

                                    st.divider()

                                # Display tweets not available with text/html, unk, warc/revisit return # noqa: E501
                                elif (
                                    archived_mimetype[i] != "application/json"
                                    and not available_tweet_text[i]
                                ):
                                    if (
                                        ".jpg" in original_tweet_url[i]
                                        or ".png" in original_tweet_url[i]
                                    ) and (400 <= archived_statuscode[i] <= 511):
                                        components.iframe(
                                            archived_tweet_url[i],
                                            height=500,
                                            scrolling=True,
                                        )
                                    elif "/status/" not in original_tweet_url[i]:
                                        st.info(
                                            "This isn't a status or is not available"
                                        )
                                    elif (
                                        check_double_status(
                                            archived_tweet_url[i], original_tweet_url[i]
                                        )
                                        or f"{st.session_state.current_username}"
                                        not in original_tweet_url[i]
                                    ):
                                        st.info(
                                            f"Replying to {st.session_state.current_username}"  # noqa: E501
                                        )
                                    else:
                                        components.iframe(
                                            archived_tweet_url[i],
                                            height=500,
                                            scrolling=True,
                                        )

                                    st.divider()

                                # Display tweets not available with application/json return # noqa: E501
                                elif (
                                    archived_mimetype[i] == "application/json"
                                    and not available_tweet_text[i]
                                ):
                                    st.code(parsed_tweet_text_mimetype_json[i])
                                    # st.json(json_data, expanded=False)

                                    st.divider()

                            # Display only tweets not available
                            if not_available:
                                return_none_count += 1

                                st.markdown(
                                    f'{i+1 + st.session_state.offset}. [**archived url ↗**]({archived_tweet_url[i]}) · [**tweet url ↗**]({original_tweet_url[i]}) · **MIME type:** {archived_mimetype[i]} · **archived timestamp:** {datetime.datetime.strptime(str(archived_timestamp[i]), "%Y%m%d%H%M%S")} · **archived status code:** {archived_statuscode[i]}'  # noqa: E501
                                )

                                # Display tweets not available with text/html, unk, warc/revisit return # noqa: E501
                                if (
                                    archived_mimetype[i] != "application/json"
                                    and not available_tweet_text[i]
                                ):
                                    if (
                                        ".jpg" in original_tweet_url[i]
                                        or ".png" in original_tweet_url[i]
                                    ) and (400 <= archived_statuscode[i] <= 511):
                                        components.iframe(
                                            archived_tweet_url[i],
                                            height=500,
                                            scrolling=True,
                                        )
                                    elif "/status/" not in original_tweet_url[i]:
                                        st.info(
                                            "This isn't a status or is not available"
                                        )
                                    elif (
                                        check_double_status(
                                            archived_tweet_url[i], original_tweet_url[i]
                                        )
                                        or f"{st.session_state.current_username}"
                                        not in original_tweet_url[i]
                                    ):
                                        st.info(
                                            f"Replying to {st.session_state.current_username}"  # noqa: E501
                                        )
                                    else:
                                        components.iframe(
                                            archived_tweet_url[i],
                                            height=500,
                                            scrolling=True,
                                        )

                                    st.divider()

                                # Display tweets not available with application/json return # noqa: E501
                                elif (
                                    archived_mimetype[i] == "application/json"
                                    and not available_tweet_text[i]
                                ):
                                    st.code(parsed_tweet_text_mimetype_json[i])
                                    # st.json(json_data, expanded=False)

                                    st.divider()

                                progress.write(
                                    f"{return_none_count} URLs have been captured in the range {start_index}-{end_index}"  # noqa: E501
                                )
                        pass
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

        if not archived_tweets:
            st.error("Unable to query the Wayback Machine API.")
    except TypeError as e:
        st.error(
            f"""
        {e}. Refresh this page and try again.

        If the problem persists [open an issue](https://github.com/claromes/waybacktweets/issues)."""  # noqa: E501
        )
        st.session_state.offset = 0
