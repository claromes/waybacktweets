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
hide_streamlit_style = """
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
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

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

st.title('Wayback Tweets [![GitHub stars](https://img.shields.io/github/stars/claromes/waybacktweets?style=social)](https://github.com/claromes/waybacktweets)', anchor=False)
st.write('Archived tweets on Wayback Machine')

handle = st.text_input('username', placeholder='username', label_visibility='collapsed')
query = st.button('Query', type='primary', use_container_width=True, key='init')
only_deleted = st.checkbox('Only deleted tweets')

if query or handle:
    with st.spinner(''):
        progress = st.empty()
        links = query_api(handle)
        parsed_links = parse_links(links)[0]
        tweet_links = parse_links(links)[1]
        mimetype = parse_links(links)[2]
        timestamp = parse_links(links)[3]

        if links or stop:
            st.divider()

            return_none_count = 0

            for i, link in enumerate(parsed_links):
                tweet = embed('{}'.format(tweet_links[i]))

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

                        progress.write('{}/{} URLs have been captured'.format(return_none_count, len(parsed_links)))

        if not links:
            st.error('Unable to query the Wayback Machine API.')
