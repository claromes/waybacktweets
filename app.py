import requests
import datetime
import streamlit as st
import streamlit.components.v1 as components

__version__ = '0.0.1'

st.set_page_config(
    page_title='Wayback Tweets',
    page_icon='🏛️',
    layout='centered'
)

def embed(tweet):
    api = 'https://publish.twitter.com/oembed?url={}'.format(tweet)
    response = requests.get(api)

    if response.status_code == 200 or response.status_code == 304:
        return response.json()['html']
    else:
        return None

def query_api(handle):
    if not handle:
        st.error("Type Twitter's handle")
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
    {}. [Wayback Machine link]({})

    **MIME Type:** {}

    **From:** {}

    [Tweet link]({})
    '''.format(i+1, link, mimetype[i], datetime.datetime.strptime(timestamp[i], "%Y%m%d%H%M%S"), tweet_links[i]))

    st.markdown('**Preview:**')

st.title('Wayback Tweets', anchor=False)
st.write('Archived tweets on Wayback Machine')

handle = st.text_input('Type Twitter handle', placeholder='Type Twitter handle', label_visibility='collapsed')

query = st.button('Query', type='primary', use_container_width=True)


if query:
    links = query_api(handle)
    parsed_links = parse_links(links)[0]
    tweet_links = parse_links(links)[1]
    mimetype = parse_links(links)[2]
    timestamp = parse_links(links)[3]

    if links:
        only_deleted = st.checkbox('Only deleted tweets')

        st.write('{} URLs have been captured'.format(len(parsed_links)))

        st.divider()

        for i, link in enumerate(parsed_links):
            tweet = embed('{}'.format(tweet_links[i]))

            if not only_deleted:
                attr(i)

                if tweet == None:
                    st.error('Tweet has been deleted.')
                    st.markdown('<iframe src="{}" height=700 width=550></iframe>'.format(link), unsafe_allow_html=True)
                    st.divider()
                else:
                    components.html(tweet, height=700, scrolling=True)
                    st.divider()

            if only_deleted:
                if tweet == None:
                    attr(i)

                    st.error('Tweet has been deleted.')
                    st.markdown('<iframe src="{}" height=700 width=550></iframe>'.format(link), unsafe_allow_html=True)
                    st.divider()
                else: st.empty()

    if not links:
        st.error('Unable to query the Wayback Machine API.')
