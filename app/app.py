from datetime import datetime, timedelta

import streamlit as st
import streamlit.components.v1 as components

from waybacktweets.api.export import TweetsExporter
from waybacktweets.api.parse import TweetsParser
from waybacktweets.api.request import WaybackTweets
from waybacktweets.api.visualize import HTMLTweetsVisualizer
from waybacktweets.config import config

# ------ Initial Settings ------ #

PAGE_ICON = "assets/parthenon.png"
TITLE = "assets/waybacktweets.png"
FIELD_OPTIONS = [
    "archived_urlkey",
    "archived_timestamp",
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
    "archived_digest",
    "archived_length",
]

collapse = None
matchtype = None
start_date = datetime.now() - timedelta(days=30 * 6)
end_date = datetime.now()
min_date = datetime(2006, 1, 1)

# ------ Verbose Mode Configuration ------ #

config.verbose = False

# ------ Page Configuration ------ #

st.set_page_config(
    page_title="Wayback Tweets",
    page_icon=PAGE_ICON,
    layout="centered",
    menu_items={
        "About": f"""
© 2023-{end_date.year} [Claromes](https://claromes.com). Licensed under the [GPL-3.0](https://raw.githubusercontent.com/claromes/waybacktweets/refs/heads/main/LICENSE.md). Icon by The Doodle Library. Title font by Google, licensed under the Open Font License (OFL).

---
""",  # noqa: E501
        "Report a bug": "https://github.com/claromes/waybacktweets/issues",
    },
)

# ------ Set States and Params ------ #

if "current_username" not in st.session_state:
    st.session_state.current_username = ""

if "count" not in st.session_state:
    st.session_state.count = False

if "archived_timestamp_filter" not in st.session_state:
    st.session_state.archived_timestamp_filter = (start_date, end_date)

if "username_value" not in st.session_state:
    st.session_state.username_value = ""

if "expanded_value" not in st.session_state:
    st.session_state.expanded_value = False

if "query" not in st.session_state:
    st.session_state.query = False

if "update_component" not in st.session_state:
    st.session_state.update_component = 0

if "username" not in st.query_params:
    st.query_params["username"] = ""

# ------ Add Custom CSS Style ------ #

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
        button[data-testid="StyledFullScreenButton"] {
            display: none;
        }
        div[class="st-emotion-cache-1v0mbdj e115fcil1"] {
            max-width: 100%;
        }
    </style>
    """
)

# ------ Functions ------ #


@st.cache_data(ttl=600, show_spinner=False)
def wayback_tweets(
    username,
    collapse,
    timestamp_from,
    timestamp_to,
    limit,
    matchtype,
):
    response = WaybackTweets(
        username,
        collapse,
        timestamp_from,
        timestamp_to,
        limit,
        matchtype,
    )
    archived_tweets = response.get()

    return archived_tweets


@st.cache_data(ttl=600, show_spinner=False)
def tweets_parser(archived_tweets, username, field_options):
    parser = TweetsParser(archived_tweets, username, field_options)
    parsed_tweets = parser.parse()

    return parsed_tweets


@st.cache_data(ttl=600, show_spinner=False)
def tweets_exporter(parsed_tweets, username, field_options):
    exporter = TweetsExporter(parsed_tweets, username, field_options)

    df = exporter.dataframe
    file_name = exporter.filename

    return df, file_name


# ------ Custom JavaScript ------ #


def scroll_page():
    js = f"""
    <script>
        window.parent.document.querySelector('section.main').scrollTo(700, 700);
        let update_component = {st.session_state.update_component} // Force component update to generate scroll
    </script>
    """  # noqa: E501

    components.html(js, width=0, height=0)


# ------ Query Param ------ #

if st.query_params.username != "":
    st.session_state.username_value = st.query_params.username
    st.session_state.expanded_value = True
    st.session_state.query = True

    st.session_state.update_component += 1
    scroll_page()

# ------ UI Settings ------ #

st.image(TITLE, use_container_width="never")
st.write(
    "Retrieves archived tweets CDX data in HTML, CSV, and JSON formats."  # noqa: E501
)

st.write(
    "This application is a prototype based on the Python package and does not include all available features. To explore the package, including CLI and Module usage, visit the [GitHub repository](https://github.com/claromes/waybacktweets)."  # noqa: E501
)

st.divider()

# -- Filters -- #

username = st.text_input(
    "Username",
    value=st.session_state.username_value,
    key="username",
    placeholder="Without @",
)

st.session_state.archived_timestamp_filter = st.date_input(
    "Tweets saved between",
    (start_date, end_date),
    min_date,
    end_date,
    format="YYYY/MM/DD",
    help="Using the `from` and `to` filters. Format: YYYY/MM/DD",
)
st.caption(
    ":gray[Note: Large date ranges may take longer to process and exceed the app's resource limits. Use smaller ranges for faster results.]"  # noqa: E501
)

limit = st.text_input(
    "Limit",
    key="limit",
    help="Query result limits",
)

unique = st.checkbox(
    "Only unique Wayback Machine URLs",
    key="unique",
    help="Filtering by the collapse option using the `urlkey` field and the URL Match Scope `prefix`",  # noqa: E501
)
st.caption(
    ":gray[Note: As noted in the official Wayback CDX Server API documentation, retrieving unique URLs may experience slow performance at this time.]"  # noqa: E501
)


query = st.button("Go", type="primary", use_container_width=True)

if st.query_params.username == "":
    st.query_params.clear()
    st.session_state.query = query

# ------ Results ------ #

if username != st.session_state.current_username:
    st.session_state.current_username = username

if (st.session_state.query and username) or st.session_state.count:
    if unique:
        collapse = "urlkey"
        matchtype = "prefix"

    try:
        with st.spinner(f"Retrieving @{st.session_state.current_username}..."):
            wayback_tweets = wayback_tweets(
                st.session_state.current_username,
                collapse,
                st.session_state.archived_timestamp_filter[0],
                st.session_state.archived_timestamp_filter[1],
                limit,
                matchtype,
            )

        if not wayback_tweets:
            st.error("No data was saved due to an empty response.")
            st.stop()

        with st.spinner(f"Parsing @{st.session_state.current_username}..."):
            parsed_tweets = tweets_parser(
                wayback_tweets, st.session_state.current_username, FIELD_OPTIONS
            )

            df, file_name = tweets_exporter(
                parsed_tweets, st.session_state.current_username, FIELD_OPTIONS
            )

        csv_data = df.to_csv(index=False)
        json_data = df.to_json(orient="records", lines=False)
        html = HTMLTweetsVisualizer(username, json_data)
        html_content = html.generate()

        # -- Rendering -- #

        st.session_state.count = len(df)
        st.caption(f"{st.session_state.count} URLs have been captured.")

        tab1, tab2, tab3 = st.tabs(["HTML", "CSV", "JSON"])

        # -- HTML -- #
        with tab1:
            st.download_button(
                label=f"Download @{st.session_state.current_username} in HTML",
                data=html_content,
                file_name=f"{file_name}.html",
                mime="text/html",
                icon=":material/download:",
            )

            st.caption("Note: The iframes are best viewed in Firefox.")

            # -- CSV -- #
        with tab2:
            st.download_button(
                label=f"Download @{st.session_state.current_username} in CSV",
                data=csv_data,
                file_name=f"{file_name}.csv",
                mime="text/csv",
                icon=":material/download:",
            )

            st.caption("Preview:")
            st.dataframe(df, use_container_width=True)

            # -- JSON -- #
        with tab3:
            st.download_button(
                label=f"Download @{st.session_state.current_username} in JSON",
                data=json_data,
                file_name=f"{file_name}.json",
                mime="application/json",
                icon=":material/download:",
            )

            st.caption("Preview:")
            st.json(json_data, expanded=1)
    except TypeError as e:
        st.error(
            f"""
        {e}. Refresh this page and try again.

        If the problem persists [open an issue](https://github.com/claromes/waybacktweets/issues)."""  # noqa: E501
        )
        st.stop()
    except IndexError:
        st.error("Please check if you have entered a date range in the filter.")
        st.stop()
    except Exception as e:
        st.error(str(e))
        st.stop()
