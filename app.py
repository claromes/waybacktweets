import requests
import datetime
import streamlit as st
import streamlit.components.v1 as components

__version__ = '0.1.4-beta'

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

        This tool is experimental, please feel free to send your [feedbacks](https://github.com/claromes/waybacktweets/issues).

        Copyright © {}, [claromes.gitlab.io](https://claromes.gitlab.io).

        -------
        '''.format(year),
        'Report a bug': 'https://github.com/claromes/waybacktweets/issues'
    }
)

if 'current_index' not in st.session_state:
    st.session_state.current_index = 0

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

def scroll_into_view():
    js = '''
    <script>
        window.parent.document.querySelector('section.main').scrollTo(0, 0);
        let update_component = {} // Force component update to generate scroll
    </script>
    '''.format(st.session_state.update_component)

    components.html(js, width=0, height=0)

@st.cache_data(ttl=3600, show_spinner=False)
def embed(tweet):
    api = 'https://publish.twitter.com/oembed?url={}'.format(tweet)
    response = requests.get(api)

    if response.status_code == 200 or response.status_code == 304:
        return response.json()['html']
    else:
        return None

@st.cache_data(ttl=3600, show_spinner=False)
def query_api(handle):
    if not handle:
        st.warning('username, please!')
        st.stop()

    url = 'https://web.archive.org/cdx/search/cdx?url=https://twitter.com/{}/status/*&output=json'.format(handle)
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

@st.cache_data(ttl=3600, show_spinner=False)
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

@st.cache_data(ttl=3600, show_spinner=False)
def attr(i):
    st.markdown('''
    {}. **Wayback Machine:** [link]({}) | **MIME Type:** {} | **From:** {} | **Tweet:** [link]({})
    '''.format(i+1, link, mimetype[i], datetime.datetime.strptime(timestamp[i], "%Y%m%d%H%M%S"), tweet_links[i]))

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
        st.session_state.current_index = 0

    if query != st.session_state.current_query:
        st.session_state.current_index = 0

    try:
        with st.spinner(''):
            progress = st.empty()
            links = query_api(handle)
            parsed_links = parse_links(links)[0]
            tweet_links = parse_links(links)[1]
            mimetype = parse_links(links)[2]
            timestamp = parse_links(links)[3]

            only_deleted = st.checkbox('Only deleted tweets')

            if links:
                st.divider()

                st.session_state.current_handle = handle
                st.session_state.current_query = query

                return_none_count = 0
                tweets_per_page = 50

                def prev_page():
                    st.session_state.current_index -= tweets_per_page

                    #scroll to top config
                    st.session_state.update_component += 1
                    scroll_into_view()

                def next_page():
                    st.session_state.current_index += tweets_per_page

                    #scroll to top config
                    st.session_state.update_component += 1
                    scroll_into_view()

                start_index = st.session_state.current_index
                end_index = min(len(parsed_links), start_index + tweets_per_page)

                for i in range(start_index, end_index):
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

                        if i + 1 == end_index:
                            progress.write('{} of {} URLs have been captured'.format(i + 1, len(parsed_links)))
                        else:
                            progress.write('{} to {} of {} URLs have been captured'.format(i + 1, end_index, len(parsed_links)))


                    if only_deleted:
                        if tweet == None:
                            return_none_count += 1
                            attr(i)

                            st.error('Tweet has been deleted.')
                            components.iframe(src=link, width=700, height=1000, scrolling=True)
                            st.divider()

                        progress.write('{} URLs have been captured in the range {}-{} of {}'.format(return_none_count, start_index, end_index, len(parsed_links)))

                    if start_index <= 0:
                        st.session_state.prev_disabled = True
                    else:
                        st.session_state.prev_disabled = False

                    if i + 1 == len(parsed_links):
                        st.session_state.next_disabled = True
                    else:
                        st.session_state.next_disabled = False

                prev, _ , next = st.columns([3, 4, 3])

                prev.button('Previous', disabled=st.session_state.prev_disabled, key='prev_button_key', on_click=prev_page, type='primary', use_container_width=True)
                next.button('Next', disabled=st.session_state.next_disabled, key='next_button_key', on_click=next_page, type='primary', use_container_width=True)

            if not links:
                st.error('Unable to query the Wayback Machine API.')
    except TypeError as e:
        st.error('''
        {}. Refresh this page and try again.

        If the problem persists [open an issue](https://github.com/claromes/waybacktweets/issues) or send me a [tweet](https://twitter.com/compose/tweet?text=@claromes).
        '''.format(e))
        st.session_state.current_index = 0
