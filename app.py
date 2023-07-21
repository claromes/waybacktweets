import requests
import datetime
import streamlit as st
import streamlit.components.v1 as components

__version__ = '0.1.4'

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

        - 30 embedded tweets per page
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

@st.cache_data(ttl=1800, show_spinner=False)
def embed(tweet):
    api = 'https://publish.twitter.com/oembed?url={}'.format(tweet)
    response = requests.get(api)

    if response.status_code == 200 or response.status_code == 304:
        return response.json()['html']
    else:
        return None

@st.cache_data(ttl=1800, show_spinner=False)
def tweets_count(handle):
    url = 'https://web.archive.org/cdx/search/cdx?url=https://twitter.com/{}/status/*&output=json'.format(handle)
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data and len(data) > 1:
            total_tweets = len(data) - 1
            return total_tweets
        else:
            return 0
    else:
        return None

@st.cache_data(ttl=1800, show_spinner=False)
def query_api(handle, limit, offset):
    if not handle:
        st.warning('username, please!')
        st.stop()

    url = 'https://web.archive.org/cdx/search/cdx?url=https://twitter.com/{}/status/*&output=json&limit={}&offset={}'.format(handle, limit, offset)
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

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
        with st.spinner(''):
            progress = st.empty()
            links = query_api(handle, tweets_per_page, st.session_state.offset)
            parsed_links = parse_links(links)[0]
            tweet_links = parse_links(links)[1]
            mimetype = parse_links(links)[2]
            timestamp = parse_links(links)[3]


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

                start_index = st.session_state.offset
                end_index = min(count, start_index + tweets_per_page)

                for i in range(tweets_per_page):
                    try:
                        link = parsed_links[i]
                        tweet = embed(tweet_links[i])

                        if not only_deleted:
                            attr(i)

                            if tweet == None:
                                st.error('Tweet has been deleted.')
                                components.iframe(src=link, width=700, height=1000, scrolling=True)
                                st.divider()
                            else:
                                components.html(tweet, width=700, height=1000, scrolling=True)
                                st.divider()

                        if only_deleted:
                            if tweet == None:
                                return_none_count += 1
                                attr(i)

                                st.error('Tweet has been deleted.')
                                components.iframe(src=link, width=700, height=1000, scrolling=True)
                                st.divider()

                            progress.write('{} URLs have been captured in the range {}-{}'.format(return_none_count, start_index, end_index))

                        if start_index <= 0:
                            st.session_state.prev_disabled = True
                        else:
                            st.session_state.prev_disabled = False

                        if i + 1 == count:
                            st.session_state.next_disabled = True
                        else:
                            st.session_state.next_disabled = False
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
