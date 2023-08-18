import requests
import datetime
import streamlit as st
import streamlit.components.v1 as components
import json
import re

year = datetime.datetime.now().year

st.set_page_config(
    page_title='Wayback Tweets',
    page_icon='🏛️',
    layout='centered',
    menu_items={

        'About': '''
        ## 🏛️ Wayback Tweets

        [![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/claromes/waybacktweets?include_prereleases)](https://github.com/claromes/waybacktweets/releases) [![License](https://img.shields.io/github/license/claromes/waybacktweets)](https://github.com/claromes/waybacktweets/blob/main/LICENSE.md)

        Tool that displays multiple archived tweets on Wayback Machine to avoid opening each link manually.

        - 30 tweets per page
        - Filtering by only deleted tweets

        This tool is experimental, please feel free to send your [feedbacks](https://github.com/claromes/waybacktweets/issues).

        -------
        '''.format(year),
        'Report a bug': 'https://github.com/claromes/waybacktweets/issues'
    }
)

# https://discuss.streamlit.io/t/remove-hide-running-man-animation-on-top-of-page/21773/3
hide_streamlit_style = '''
<style>
    header[data-testid="stHeader"] {
        opacity: 0.5;
    }
    iframe {
        background-color: #dddddd;
        border-radius: 0.5rem;
    }
</style>
'''

st.markdown(hide_streamlit_style, unsafe_allow_html=True)

if 'current_query' not in st.session_state:
    st.session_state.current_query = ''

if 'current_handle' not in st.session_state:
    st.session_state.current_handle = ''

if 'prev_disabled' not in st.session_state:
    st.session_state.prev_disabled = False

if 'next_disabled' not in st.session_state:
    st.session_state.next_disabled = False

if 'next_button' not in st.session_state:
    st.session_state.next_button = False

if 'prev_button' not in st.session_state:
    st.session_state.prev_button = False

if 'update_component' not in st.session_state:
    st.session_state.update_component = 0

if 'offset' not in st.session_state:
    st.session_state.offset = 0

def scroll_into_view():
    js = '''
    <script>
        window.parent.document.querySelector('section.main').scrollTo(0, 0);
        let update_component = {} // Force component update to generate scroll
    </script>
    '''.format(st.session_state.update_component)

    components.html(js, width=0, height=0)

def embed(tweet):
    try:
        url = 'https://publish.twitter.com/oembed?url={}'.format(tweet)
        response = requests.get(url)

        regex = r'<blockquote class="twitter-tweet"(?: [^>]+)?><p[^>]*>(.*?)<\/p>.*?&mdash; (.*?)<\/a>'
        regex_author = r'^(.*?)\s*\('

        if response.status_code == 200 or response.status_code == 302:
            status_code = response.status_code
            html = response.json()['html']
            author_name = response.json()['author_name']

            matches_html = re.findall(regex, html, re.DOTALL)

            tweet_content = []
            user_info = []
            is_RT = []

            for match in matches_html:
                tweet_content_match = re.sub(r'<a[^>]*>|<\/a>', '', match[0].strip())
                tweet_content_match = tweet_content_match.replace('<br>', '\n')

                user_info_match = re.sub(r'<a[^>]*>|<\/a>', '', match[1].strip())
                user_info_match = user_info_match.replace(')', '), ')

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
        st.error('Connection to publish.twitter.com timed out.')



@st.cache_data(ttl=1800, show_spinner=False)
def tweets_count(handle):
    url = 'https://web.archive.org/cdx/search/cdx?url=https://twitter.com/{}/status/*&output=json'.format(handle)
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
        st.error('Connection to web.archive.org timed out.')


@st.cache_data(ttl=1800, show_spinner=False)
def query_api(handle, limit, offset):
    if not handle:
        st.warning('username, please!')
        st.stop()

    url = 'https://web.archive.org/cdx/search/cdx?url=https://twitter.com/{}/status/*&output=json&limit={}&offset={}'.format(handle, limit, offset)
    try:
        response = requests.get(url)

        if response.status_code == 200 or response.status_code == 304:
            return response.json()
    except requests.exceptions.Timeout:
        st.error('Connection to web.archive.org timed out.')

@st.cache_data(ttl=1800, show_spinner=False)
def parse_links(links):
    parsed_links = []
    timestamp = []
    tweet_links = []
    parsed_mimetype = []

    for link in links[1:]:
        url = 'https://web.archive.org/web/{}/{}'.format(link[1], link[2])

        parsed_links.append(url)
        timestamp.append(link[1])
        tweet_links.append(link[2])
        parsed_mimetype.append(link[3])

    return parsed_links, tweet_links, parsed_mimetype, timestamp

def attr(i):
    st.markdown('''
    {}. **Wayback Machine:** [link]({}) | **MIME Type:** {} | **Created at:** {} | **Tweet:** [link]({})
    '''.format(i+1 + st.session_state.offset, link, mimetype[i], datetime.datetime.strptime(timestamp[i], "%Y%m%d%H%M%S"), tweet_links[i]))

# UI
st.title('''
Wayback Tweets [![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/claromes/waybacktweets?include_prereleases)](https://github.com/claromes/waybacktweets/releases)
''', anchor=False)
st.write('''
Display multiple archived tweets on Wayback Machine and avoid opening each link manually

*via Wayback CDX Server API*
''')

handle = st.text_input('username', placeholder='username', label_visibility='collapsed')
query = st.button('Query', type='primary', use_container_width=True)

bar = st.empty()

if query or handle:
    if handle != st.session_state.current_handle:
        st.session_state.offset = 0

    if query != st.session_state.current_query:
        st.session_state.offset = 0

    count = tweets_count(handle)

    st.write('**{} URLs have been captured**'.format(count))

    tweets_per_page = 30

    only_deleted = st.checkbox('Only deleted tweets')

    try:
        bar.progress(0)
        progress = st.empty()
        links = query_api(handle, tweets_per_page, st.session_state.offset)

        parse = parse_links(links)
        parsed_links = parse[0]
        tweet_links = parse[1]
        mimetype = parse[2]
        timestamp = parse[3]

        if links:
            st.divider()

            st.session_state.current_handle = handle
            st.session_state.current_query = query

            return_none_count = 0

            def prev_page():
                st.session_state.offset -= tweets_per_page

                #scroll to top config
                st.session_state.update_component += 1
                scroll_into_view()

            def next_page():
                st.session_state.offset += tweets_per_page

                #scroll to top config
                st.session_state.update_component += 1
                scroll_into_view()

            def display_tweet():
                if is_RT[0] == True:
                    st.info('*Retweet*')
                st.write(tweet_content[0])
                st.write(user_info[0])

                st.divider()

            def display_not_tweet():
                if mimetype[i] == 'application/json':
                    st.error('Tweet has been deleted.')
                    response_json = requests.get(link)
                    json_data = response_json.json()
                    json_text = response_json.json()['text']

                    st.code(json_text)
                    st.json(json_data, expanded=False)

                    st.divider()
                if mimetype[i] == 'text/html':
                    st.error('Tweet has been deleted.')

                    components.iframe(link, height=500, scrolling=True)

                    st.divider()
                if mimetype[i] == 'warc/revisit':
                    st.warning('''MIME Type was not parsed.''')

                    st.divider()
                if mimetype[i] == 'text/plain':
                    st.warning('''MIME Type was not parsed.''')

                    st.divider()

            start_index = st.session_state.offset
            end_index = min(count, start_index + tweets_per_page)

            for i in range(tweets_per_page):
                try:
                    bar.progress((i*3) + 13)

                    link = parsed_links[i]
                    tweet = embed(tweet_links[i])

                    if not only_deleted:
                        attr(i)

                        if tweet:
                            status_code = tweet[0]
                            tweet_content = tweet[1]
                            user_info = tweet[2]
                            is_RT = tweet[3]

                            if mimetype[i] == 'application/json':
                                display_tweet()

                            if mimetype[i] == 'text/html':
                                display_tweet()
                        elif not tweet:
                            display_not_tweet()

                    if only_deleted:
                        if not tweet:
                            return_none_count += 1
                            attr(i)

                            display_not_tweet()

                        progress.write('{} URLs have been captured in the range {}-{}'.format(return_none_count, start_index, end_index))

                    if start_index <= 0:
                        st.session_state.prev_disabled = True
                    else:
                        st.session_state.prev_disabled = False

                    if i + 1 == count:
                        st.session_state.next_disabled = True
                    else:
                        st.session_state.next_disabled = False
                # TODO
                except IndexError:
                    if start_index <= 0:
                        st.session_state.prev_disabled = True
                    else:
                        st.session_state.prev_disabled = False

                    st.session_state.next_disabled = True

            prev, _ , next = st.columns([3, 4, 3])

            prev.button('Previous', disabled=st.session_state.prev_disabled, key='prev_button_key', on_click=prev_page, type='primary', use_container_width=True)
            next.button('Next', disabled=st.session_state.next_disabled, key='next_button_key', on_click=next_page, type='primary', use_container_width=True)

        if not links:
            st.error('Unable to query the Wayback Machine API.')
    except TypeError as e:
        st.error('''
        {}. Refresh this page and try again.

        If the problem persists [open an issue](https://github.com/claromes/waybacktweets/issues).
        '''.format(e))
        st.session_state.offset = 0
