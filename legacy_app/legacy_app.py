import datetime
import re
from urllib.parse import unquote

import requests
import streamlit as st
import streamlit.components.v1 as components

year = datetime.datetime.now().year

st.set_page_config(
    page_title="Wayback Tweets",
    page_icon="🏛️",
    layout="centered",
    menu_items={
        "About": """
        ## 🏛️ Wayback Tweets

        Tool that displays, via Wayback CDX Server API, multiple archived tweets on Wayback Machine to avoid opening each link manually. Users can apply filters based on specific years and view tweets that do not have the original URL available.

        This tool is a prototype, please feel free to send your [feedbacks](https://github.com/claromes/waybacktweets/issues). Created by [@claromes](https://claromes.com).

        -------
        """,  # noqa: E501
    },
)

# https://discuss.streamlit.io/t/remove-hide-running-man-animation-on-top-of-page/21773/3
hide_streamlit_style = """
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
</style>
"""

st.markdown(hide_streamlit_style, unsafe_allow_html=True)

if "current_handle" not in st.session_state:
    st.session_state.current_handle = ""

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

if "saved_at" not in st.session_state:
    st.session_state.saved_at = (2006, year)

if "count" not in st.session_state:
    st.session_state.count = False


def scroll_into_view():
    js = f"""
    <script>
        window.parent.document.querySelector('section.main').scrollTo(0, 0);
        let update_component = {st.session_state.update_component} // Force component update to generate scroll
    </script>
    """  # noqa: E501

    components.html(js, width=0, height=0)


def clean_tweet(tweet):
    handle = st.session_state.current_handle.lower()
    tweet_lower = tweet.lower()

    pattern = re.compile(r"/status/(\d+)")
    match_lower_case = pattern.search(tweet_lower)
    match_original_case = pattern.search(tweet)

    if match_lower_case and handle in tweet_lower:
        return f"https://twitter.com/{st.session_state.current_handle}/status/{match_original_case.group(1)}"  # noqa: E501
    else:
        return tweet


def clean_link(link):
    handle = st.session_state.current_handle.lower()
    link = link.lower()

    pattern = re.compile(r"/status/(\d+)")
    match = pattern.search(link)

    if match and handle in link:
        return f"https://web.archive.org/web/{timestamp[i]}/https://twitter.com/{st.session_state.current_handle}/status/{match.group(1)}"  # noqa: E501
    else:
        return link


def pattern_tweet(tweet):
    # Reply: /status//
    # Link:  /status///
    # Twimg: /status/https://pbs

    pattern = re.compile(r'/status/"([^"]+)"')

    match = pattern.search(tweet)
    if match:
        return match.group(1).lstrip("/")
    else:
        return tweet


def pattern_tweet_id(tweet):
    # Delete sub-endpoint (/photos, /likes, /retweet...)
    pattern_username = re.compile(r"https://twitter\.com/([^/]+)/status/\d+")
    match_username = pattern_username.match(tweet)

    pattern_id = r"https://twitter.com/\w+/status/(\d+)"
    match_id = re.search(pattern_id, tweet)

    if match_id and match_username:
        tweet_id = match_id.group(1)
        username = match_username.group(1)
        return f"https://twitter.com/{username}/status/{tweet_id}"
    else:
        return tweet


def check_double_status(url_wb, url_tweet):
    if url_wb.count("/status/") == 2 and "twitter.com" not in url_tweet:
        return True

    return False


def embed(tweet):
    try:
        url = f"https://publish.twitter.com/oembed?url={clean_tweet(tweet)}"
        response = requests.get(url)

        regex = r'<blockquote class="twitter-tweet"(?: [^>]+)?><p[^>]*>(.*?)<\/p>.*?&mdash; (.*?)<\/a>'  # noqa: E501
        regex_author = r"^(.*?)\s*\("

        if response.status_code == 200 or response.status_code == 302:
            status_code = response.status_code
            html = response.json()["html"]
            author_name = response.json()["author_name"]

            matches_html = re.findall(regex, html, re.DOTALL)

            tweet_content = []
            user_info = []
            is_RT = []

            for match in matches_html:
                tweet_content_match = re.sub(r"<a[^>]*>|<\/a>", "", match[0].strip())
                tweet_content_match = tweet_content_match.replace("<br>", "\n")

                user_info_match = re.sub(r"<a[^>]*>|<\/a>", "", match[1].strip())
                user_info_match = user_info_match.replace(")", "), ")

                match_author = re.search(regex_author, user_info_match)
                author_tweet = match_author.group(1)

                if tweet_content_match:
                    tweet_content.append(tweet_content_match)
                if user_info_match:
                    user_info.append(user_info_match)

                    is_RT_match = False
                    if author_name != author_tweet:
                        is_RT_match = True

                    is_RT.append(is_RT_match)

            return status_code, tweet_content, user_info, is_RT
        else:
            return False
    except requests.exceptions.Timeout:
        st.error("Connection to web.archive.org timed out.")
    except requests.exceptions.ConnectionError:
        st.error("Failed to establish a new connection with web.archive.org.")
    except UnboundLocalError:
        st.empty()


@st.cache_data(ttl=1800, show_spinner=False)
def tweets_count(handle, saved_at):
    url = f"https://web.archive.org/cdx/search/cdx?url=https://twitter.com/{handle}/status/*&collapse=timestamp:8&output=json&from={saved_at[0]}&to={saved_at[1]}"  # noqa: E501
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
    except UnboundLocalError:
        st.empty()


@st.cache_data(ttl=1800, show_spinner=False)
def query_api(handle, limit, offset, saved_at):
    if not handle:
        st.warning("username, please!")
        st.stop()

    url = f"https://web.archive.org/cdx/search/cdx?url=https://twitter.com/{handle}/status/*&collapse=timestamp:8&output=json&limit={limit}&offset={offset}&from={saved_at[0]}&to={saved_at[1]}"  # noqa: E501
    try:
        response = requests.get(url)
        response.raise_for_status()

        if response.status_code == 200 or response.status_code == 304:
            return response.json()
    except requests.exceptions.Timeout:
        st.error("Connection to web.archive.org timed out.")
    except requests.exceptions.ConnectionError:
        st.error("Failed to establish a new connection with web.archive.org.")
    except UnboundLocalError:
        st.empty()
    except requests.exceptions.HTTPError:
        st.error(
            """
        **Temporarily Offline**

        Internet Archive services are temporarily offline. Please check Internet Archive [Twitter feed](https://twitter.com/internetarchive/) for the latest information.
        """  # noqa: E501
        )
        st.stop()


@st.cache_data(ttl=1800, show_spinner=False)
def parse_links(links):
    parsed_links = []
    timestamp = []
    tweet_links = []
    parsed_mimetype = []

    for link in links[1:]:
        tweet_remove_char = unquote(link[2]).replace("’", "")
        cleaned_tweet = pattern_tweet(tweet_remove_char).strip('"')

        url = f"https://web.archive.org/web/{link[1]}/{tweet_remove_char}"

        parsed_links.append(url)
        timestamp.append(link[1])
        tweet_links.append(cleaned_tweet)
        parsed_mimetype.append(link[3])

    return parsed_links, tweet_links, parsed_mimetype, timestamp


def attr(i):
    original_tweet = pattern_tweet_id(clean_tweet(tweet_links[i]))

    if status:
        original_tweet = pattern_tweet_id(f"https://twitter.com/{tweet_links[i]}")
    elif "://" not in tweet_links[i]:
        original_tweet = pattern_tweet_id(f"https://{tweet_links[i]}")

    st.markdown(
        f'{i+1 + st.session_state.offset}. [**archived url**]({link}) · [**original url**]({original_tweet}) · **MIME Type:** {mimetype[i]} · **Saved at:** {datetime.datetime.strptime(timestamp[i], "%Y%m%d%H%M%S")}'  # noqa: E501
    )


def display_tweet():
    if (
        mimetype[i] == "application/json"
        or mimetype[i] == "text/html"
        or mimetype[i] == "unk"
        or mimetype[i] == "warc/revisit"
    ):
        if is_RT[0] is True:
            st.info("*Retweet*")
        st.write(tweet_content[0])
        st.write(f"**{user_info[0]}**")

        st.divider()
    else:
        st.warning("MIME Type was not parsed.")

        st.divider()


def display_not_tweet():
    original_link = pattern_tweet_id(clean_tweet(tweet_links[i]))

    if status:
        original_link = pattern_tweet_id(f"https://twitter.com/{tweet_links[i]}")
    elif "://" not in tweet_links[i]:
        original_link = pattern_tweet_id(f"https://{tweet_links[i]}")

    response_html = requests.get(original_link)

    if (
        mimetype[i] == "text/html"
        or mimetype[i] == "warc/revisit"
        or mimetype[i] == "unk"
    ):
        if (
            ".jpg" in tweet_links[i] or ".png" in tweet_links[i]
        ) and response_html.status_code == 200:
            components.iframe(tweet_links[i], height=500, scrolling=True)
        elif "/status/" not in original_link:
            st.info("This isn't a status or is not available")
        elif status or f"{st.session_state.current_handle}" not in original_link:
            st.info(f"Replying to {st.session_state.current_handle}")
        else:
            components.iframe(clean_link(link), height=500, scrolling=True)

        st.divider()
    elif mimetype[i] == "application/json":
        try:
            response_json = requests.get(link)

            if response_json.status_code == 200:
                json_data = response_json.json()

                if "data" in json_data:
                    if "text" in json_data["data"]:
                        json_text = json_data["data"]["text"]
                    else:
                        json_text = json_data["data"]
                else:
                    if "text" in json_data:
                        json_text = json_data["text"]
                    else:
                        json_text = json_data

                st.code(json_text)
                st.json(json_data, expanded=False)

                st.divider()
            else:
                st.error(response_json.status_code)

                st.divider()
        except requests.exceptions.Timeout:
            st.error("Connection to web.archive.org timed out.")
            st.divider()
        except requests.exceptions.ConnectionError:
            st.error("Failed to establish a new connection with web.archive.org.")
            st.divider()
        except UnboundLocalError:
            st.empty()
    else:
        st.warning("MIME Type was not parsed.")
        st.divider()


def prev_page():
    st.session_state.offset -= tweets_per_page

    # scroll to top config
    st.session_state.update_component += 1
    scroll_into_view()


def next_page():
    st.session_state.offset += tweets_per_page

    # scroll to top config
    st.session_state.update_component += 1
    scroll_into_view()


# UI
st.title(
    "Wayback Tweets [![Star](https://img.shields.io/github/stars/claromes/waybacktweets?style=social)](https://github.com/claromes/waybacktweets)",  # noqa: E501
    anchor=False,
    help="v0.4.3",
)
st.write(
    "Display multiple archived tweets on Wayback Machine and avoid opening each link manually"  # noqa: E501
)

handle = st.text_input("Username", placeholder="jack")

st.session_state.saved_at = st.slider("Tweets saved between", 2006, year, (2006, year))

not_available = st.checkbox(
    "Original URLs not available",
    help="Due to changes in X, it is possible to find available tweets if you are logged into X",  # noqa: E501
)

query = st.button("Query", type="primary", use_container_width=True)

if handle != st.session_state.current_handle:
    st.session_state.current_handle = handle
    st.session_state.offset = 0

if query or st.session_state.count:
    tweets_per_page = 25

    st.session_state.count = tweets_count(handle, st.session_state.saved_at)

    st.caption(
        "The search optimization uses an 8-digit [collapsing strategy](https://github.com/internetarchive/wayback/blob/master/wayback-cdx-server/README.md?ref=hackernoon.com#collapsing), refining the captures to one per day. The number of tweets per page is set to 25, and this is a fixed value due to the API rate limit."  # noqa: E501
    )
    st.write(f"**{st.session_state.count} URLs have been captured**")

    if st.session_state.count:
        if tweets_per_page > st.session_state.count:
            tweets_per_page = st.session_state.count

    try:
        progress = st.empty()
        links = query_api(
            handle, tweets_per_page, st.session_state.offset, st.session_state.saved_at
        )

        parse = parse_links(links)
        parsed_links = parse[0]
        tweet_links = parse[1]
        mimetype = parse[2]
        timestamp = parse[3]

        if links:
            st.divider()

            st.session_state.current_handle = handle

            return_none_count = 0

            start_index = st.session_state.offset
            end_index = min(st.session_state.count, start_index + tweets_per_page)

            with st.spinner("Fetching..."):
                for i in range(tweets_per_page):
                    try:
                        if tweet_links[i]:
                            link = parsed_links[i]
                            tweet = embed(tweet_links[i])

                            status = check_double_status(link, tweet_links[i])

                            if not not_available:
                                attr(i)

                                if tweet:
                                    status_code = tweet[0]
                                    tweet_content = tweet[1]
                                    user_info = tweet[2]
                                    is_RT = tweet[3]

                                    display_tweet()
                                elif not tweet:
                                    display_not_tweet()

                            if not_available:
                                if not tweet:
                                    return_none_count += 1
                                    attr(i)

                                    display_not_tweet()

                                progress.write(
                                    f"{return_none_count} URLs have been captured in the range {start_index}-{end_index}"  # noqa: E501
                                )

                            if start_index <= 0:
                                st.session_state.prev_disabled = True
                            else:
                                st.session_state.prev_disabled = False

                            if i + 1 == st.session_state.count:
                                st.session_state.next_disabled = True
                            else:
                                st.session_state.next_disabled = False
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

        if not links:
            st.error("Unable to query the Wayback Machine API.")
    except TypeError as e:
        st.error(
            f"""
        {e}. Refresh this page and try again.
        """  # noqa: E501
        )
        st.session_state.offset = 0
