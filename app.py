import requests
import datetime
import streamlit as st
import streamlit.components.v1 as components

__version__ = '0.0.2'

st.set_page_config(
    page_title='Wayback Tweets',
    page_icon='🏛️',
    layout='centered'
)

# https://discuss.streamlit.io/t/remove-hide-running-man-animation-on-top-of-page/21773/3
hide_streamlit_style = '''
<style>
    div[data-testid="stToolbar"] {
    visibility: hidden;
    height: 0%;
    position: fixed;
    }
    div[data-testid="stDecoration"] {
    visibility: hidden;
    height: 0%;
    position: fixed;
    }
    div[data-testid="stStatusWidget"] {
    visibility: hidden;
    height: 0%;
    position: fixed;
    }
    #MainMenu {
    visibility: hidden;
    height: 0%;
    }
    header {
    visibility: hidden;
    height: 0%;
    }
    footer {
    visibility: hidden;
    height: 0%;
    }
</style>
'''

#st.markdown(hide_streamlit_style, unsafe_allow_html=True)

if 'current_index' not in st.session_state:
    st.session_state.current_index = 0

if 'current_query' not in st.session_state:
    st.session_state.current_query = ''

if 'current_handle' not in st.session_state:
    st.session_state.current_handle = ''

if 'disabled_next' not in st.session_state:
    st.session_state.disabled_next = False

if 'disabled_prev' not in st.session_state:
    st.session_state.disabled_prev = False

def scroll_into_view():
    js = '''
    <script>
        window.parent.document.getElementById('wayback-tweets').scrollIntoView();
    </script>
    '''

    st.components.v1.html(js)

def embed(tweet):
    api = 'https://publish.twitter.com/oembed?url={}'.format(tweet)
    response = requests.get(api)

    if response.status_code == 200 or response.status_code == 304:
        return response.json()['html']
    else:
        return None

@st.cache_data(show_spinner=False)
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

@st.cache_data(show_spinner=False)
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
    {}. **Wayback Machine:** [link]({}) | **MIME Type:** {} | **From:** {} | **Tweet:** [link]({})
    '''.format(i+1, link, mimetype[i], datetime.datetime.strptime(timestamp[i], "%Y%m%d%H%M%S"), tweet_links[i]))

st.title('Wayback Tweets [![Fork me on GitHub](https://img.shields.io/badge/-Fork%20me%20on%20GitHub-ededed?logo=github&style=social)](https://github.com/claromes/waybacktweets)', anchor=False)
st.write('Archived tweets on Wayback Machine')

handle = st.text_input('username', placeholder='username', label_visibility='collapsed')
query = st.button('Query', type='primary', use_container_width=True)



if query or handle:
    if handle != st.session_state.current_handle:
        st.session_state.current_index = 0

    if query != st.session_state.current_query:
        st.session_state.current_index = 0

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
            tweets_per_page = 2

            start_index = st.session_state.current_index
            end_index = min(len(parsed_links), start_index + tweets_per_page)

            for i in range(start_index, end_index):
                link = parsed_links[i]
                tweet = embed(tweet_links[i])

                if not only_deleted:
                    attr(i)

                    if tweet == None:
                        st.error('Tweet has been deleted.')
                        st.markdown('<iframe src="{}" height=700 width=700 scrolling="no"></iframe>'.format(link), unsafe_allow_html=True)
                        st.divider()
                    else:
                        components.html(tweet,width=700, height=700, scrolling=True)
                        st.divider()

                    progress.write('{}/{} URLs have been captured'.format(i + 1, len(parsed_links)))

                if only_deleted:
                    if tweet == None:
                        return_none_count += 1
                        attr(i)

                        st.error('Tweet has been deleted.')
                        st.markdown('<iframe src="{}" height=700 width=700 scrolling="no"></iframe>'.format(link), unsafe_allow_html=True)
                        st.divider()

                        progress.write('{}/{}-{} URLs have been captured'.format(return_none_count, start_index, end_index))

                if start_index == 0:
                    st.session_state.disabled_prev = True
                else:
                    st.session_state.disabled_prev = False

                if i + 1 == len(parsed_links):
                    st.session_state.disabled_next = True
                else:
                    st.session_state.disabled_next = False

            print(start_index, end_index)

            prev, _ , next = st.columns([3, 4, 3])

            if prev.button('Previous', disabled=st.session_state.disabled_prev, type='primary', use_container_width=True):
                scroll_into_view()
                st.session_state.current_index -= tweets_per_page

            if next.button('Next', disabled=st.session_state.disabled_next, type='primary', use_container_width=True):
                scroll_into_view()
                st.session_state.current_index += tweets_per_page

            # if st.session_state.current_index >= len(parsed_links):
            #     st.session_state.current_index = 0

        if not links:
            st.error('Unable to query the Wayback Machine API.')
