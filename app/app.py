import base64
from datetime import datetime, timedelta

import streamlit as st

from waybacktweets.api.export import TweetsExporter
from waybacktweets.api.parse import TweetsParser
from waybacktweets.api.request import WaybackTweets
from waybacktweets.api.visualize import HTMLTweetsVisualizer
from waybacktweets.config import FIELD_OPTIONS, config

# ------ Initial Settings ------ #

PAGE_ICON = "assets/parthenon.png"
TITLE = "assets/waybacktweets.png"
DOWNLOAD = "assets/download.svg"

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
    [![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/claromes/waybacktweets?include_prereleases)](https://github.com/claromes/waybacktweets/releases) [![License](https://img.shields.io/github/license/claromes/waybacktweets)](https://github.com/claromes/waybacktweets/blob/main/LICENSE.md) [![Star](https://img.shields.io/github/stars/claromes/waybacktweets?style=social)](https://github.com/claromes/waybacktweets)

    The application is a prototype hosted on Streamlit Cloud, serving as an alternative to the command line tool.

    © 2023 - {end_date.year}, [Claromes](https://claromes.com)

    ---
""",  # noqa: E501
        "Report a bug": "https://github.com/claromes/waybacktweets/issues",
    },
)

# ------ Set States ------ #

if "current_username" not in st.session_state:
    st.session_state.current_username = ""

if "count" not in st.session_state:
    st.session_state.count = False

if "archived_timestamp_filter" not in st.session_state:
    st.session_state.archived_timestamp_filter = (start_date, end_date)

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

# ------ Requestings ------ #


@st.cache_data(ttl=600, show_spinner=False)
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


# ------ User Interface Settings ------ #

st.info(
    "🥳 [**Pre-release 1.0a5: Python module, CLI, and new Streamlit app**](https://github.com/claromes/waybacktweets/releases/tag/v1.0a5)"  # noqa: E501
)

st.image(TITLE, use_column_width="never")
st.caption(
    "[![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/claromes/waybacktweets?include_prereleases)](https://github.com/claromes/waybacktweets/releases) [![Star](https://img.shields.io/github/stars/claromes/waybacktweets?style=social)](https://github.com/claromes/waybacktweets)"  # noqa: E501
)
st.write(
    "Retrieves archived tweets CDX data in HTML (for easy viewing of the tweets using the `iframe` tag), CSV, and JSON formats."  # noqa: E501
)

st.write(
    "This application uses the Wayback Tweets Python package, which can be used either as a module or as a standalone command-line tool. [Read the documentation](https://claromes.github.io/waybacktweets) for more information.."  # noqa: E501
)

st.write(
    "To access the legacy version of Wayback Tweets, [click here](https://waybacktweets-legacy.streamlit.app)."  # noqa: E501
)

st.divider()

# -- Filters -- #

username = st.text_input("Username *", key="username", placeholder="Without @")

with st.expander("Filtering"):

    st.session_state.archived_timestamp_filter = st.date_input(
        "Tweets saved between",
        (start_date, end_date),
        min_date,
        end_date,
        format="YYYY/MM/DD",
        help="Using the `from` and `to` filters. Format: YYYY/MM/DD",
    )
    st.caption(
        ":orange[note: large date range takes a long time to process, and the app's resources may not be sufficient. Try to perform searches with smaller ranges to get faster results.]"  # noqa: E501
    )

    col1, col2 = st.columns(2)

    with col1:
        limit = st.text_input(
            "Limit",
            key="limit",
            help="Query result limits",
        )

    with col2:
        offset = st.text_input(
            "Offset",
            key="offset",
            help="Allows for a simple way to scroll through the results",
        )

    unique = st.checkbox(
        "Only unique Wayback Machine URLs",
        key="unique",
        help="Filtering by the collapse option using the `urlkey` field and the URL Match Scope `prefix`",  # noqa: E501
    )
    st.caption(
        ":orange[note: according to the official documentation of the Wayback CDX Server API, the query to retrieve unique URLs may be slow at the moment.]"  # noqa: E501
    )


query = st.button("Query", type="primary", use_container_width=True)

# ------ Results ------ #

if username != st.session_state.current_username:
    st.session_state.current_username = username

if query or st.session_state.count:
    if unique:
        collapse = "urlkey"
        matchtype = "prefix"

    try:
        with st.spinner(
            f"Waybacking @{st.session_state.current_username}'s archived tweets"
        ):
            wayback_tweets = wayback_tweets(
                st.session_state.current_username,
                collapse,
                st.session_state.archived_timestamp_filter[0],
                st.session_state.archived_timestamp_filter[1],
                limit,
                offset,
                matchtype,
            )

        if not wayback_tweets:
            st.error("No data was saved due to an empty response.")
            st.stop()

        with st.spinner(
            f"Parsing @{st.session_state.current_username}'s archived tweets"
        ):
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

        if csv_data and json_data and html_content:
            st.session_state.count = len(df)
            st.write(f"**{st.session_state.count} URLs have been captured**")

            # -- HTML -- #

            st.header("HTML", divider="gray")
            st.write(
                f"Visualize tweets more efficiently through `iframes`. Download the @{st.session_state.current_username}'s archived tweets in HTML."  # noqa: E501
            )

            col5, col6 = st.columns([1, 18])

            with col5:
                st.image(DOWNLOAD, width=22)

            with col6:
                b64_html = base64.b64encode(html_content.encode()).decode()
                href_html = f"data:text/html;base64,{b64_html}"

                st.markdown(
                    f'<a href="{href_html}" download="{file_name}.html" title="Download {file_name}.html">{file_name}.html</a>',  # noqa: E501
                    unsafe_allow_html=True,
                )

            # -- CSV -- #

            st.header("CSV", divider="gray")
            st.write(
                "Check the data returned in the dataframe below and download the file."
            )

            col7, col8 = st.columns([1, 18])

            with col7:
                st.image(DOWNLOAD, width=22)

            with col8:
                b64_csv = base64.b64encode(csv_data.encode()).decode()
                href_csv = f"data:file/csv;base64,{b64_csv}"

                st.markdown(
                    f'<a href="{href_csv}" download="{file_name}.csv" title="Download {file_name}.csv">{file_name}.csv</a>',  # noqa: E501
                    unsafe_allow_html=True,
                )

            st.dataframe(df, use_container_width=True)

            # -- JSON -- #

            st.header("JSON", divider="gray")
            st.write(
                "Check the data returned in JSON format below and download the file."
            )

            col9, col10 = st.columns([1, 18])

            with col9:
                st.image(DOWNLOAD, width=22)

            with col10:
                b64_json = base64.b64encode(json_data.encode()).decode()
                href_json = f"data:file/json;base64,{b64_json}"

                st.markdown(
                    f'<a href="{href_json}" download="{file_name}.json" title="Download {file_name}.json">{file_name}.json</a>',  # noqa: E501
                    unsafe_allow_html=True,
                )

            st.json(json_data, expanded=False)
    except TypeError as e:
        st.error(
            f"""
        {e}. Refresh this page and try again.

        If the problem persists [open an issue](https://github.com/claromes/waybacktweets/issues)."""  # noqa: E501
        )
        st.stop()
    except Exception as e:
        st.error(str(e))
        st.stop()
