from urllib.parse import unquote
from utils import *


def parse_archived_tweets(archived_tweets_response, username):
    archived_urlkey = []
    archived_timestamp = []
    tweet = []
    archived_tweet = []
    parsed_tweet = []
    parsed_archived_tweet = []
    archived_mimetype = []
    archived_statuscode = []
    archived_digest = []
    archived_length = []

    for response in archived_tweets_response[1:]:
        tweet_remove_char = unquote(response[2]).replace('’', '')
        cleaned_tweet = pattern_tweet(tweet_remove_char).strip('"')

        wayback_machine_url = f'https://web.archive.org/web/{response[1]}/{tweet_remove_char}'

        original_tweet = delete_tweet_pathnames(
            clean_tweet(cleaned_tweet, username))

        parsed_wayback_machine_url = f'https://web.archive.org/web/{response[1]}/{original_tweet}'

        double_status = check_double_status(wayback_machine_url,
                                            original_tweet)

        if double_status:
            original_tweet = delete_tweet_pathnames(
                f'https://twitter.com/{original_tweet}')

        elif not '://' in original_tweet:
            original_tweet = delete_tweet_pathnames(
                f'https://{original_tweet}')

        encoded_tweet = semicolon_parse(response[2])
        encoded_archived_tweet = semicolon_parse(wayback_machine_url)
        encoded_parsed_tweet = semicolon_parse(original_tweet)
        encoded_parsed_archived_tweet = semicolon_parse(
            parsed_wayback_machine_url)

        archived_urlkey.append(response[0])
        archived_timestamp.append(response[1])
        tweet.append(encoded_tweet)
        archived_tweet.append(encoded_archived_tweet)
        parsed_tweet.append(encoded_parsed_tweet)
        parsed_archived_tweet.append(encoded_parsed_archived_tweet)
        archived_mimetype.append(response[3])
        archived_statuscode.append(response[4])
        archived_digest.append(response[5])
        archived_length.append(response[6])

    return archived_urlkey, archived_timestamp, tweet, archived_tweet, parsed_tweet, parsed_archived_tweet, archived_mimetype, archived_statuscode, archived_digest, archived_length


# def embed(tweet):
#     try:
#         url = f'https://publish.twitter.com/oembed?url={clean_tweet(tweet)}'
#         response = requests.get(url)

#         regex = r'<blockquote class="twitter-tweet"(?: [^>]+)?><p[^>]*>(.*?)<\/p>.*?&mdash; (.*?)<\/a>'
#         regex_author = r'^(.*?)\s*\('

#         if response.status_code == 200 or response.status_code == 302:
#             status_code = response.status_code
#             html = response.json()['html']
#             author_name = response.json()['author_name']

#             matches_html = re.findall(regex, html, re.DOTALL)

#             tweet_content = []
#             user_info = []
#             is_RT = []

#             for match in matches_html:
#                 tweet_content_match = re.sub(r'<a[^>]*>|<\/a>', '',
#                                              match[0].strip())
#                 tweet_content_match = tweet_content_match.replace('<br>', '\n')

#                 user_info_match = re.sub(r'<a[^>]*>|<\/a>', '',
#                                          match[1].strip())
#                 user_info_match = user_info_match.replace(')', '), ')

#                 match_author = re.search(regex_author, user_info_match)
#                 author_tweet = match_author.group(1)

#                 if tweet_content_match:
#                     tweet_content.append(tweet_content_match)
#                 if user_info_match:
#                     user_info.append(user_info_match)

#                     is_RT_match = False
#                     if author_name != author_tweet:
#                         is_RT_match = True

#                     is_RT.append(is_RT_match)

#             return status_code, tweet_content, user_info, is_RT
#         else:
#             return False
#     except requests.exceptions.Timeout as e:
#         print(f'{e}.\nConnection to web.archive.org timed out.')
#     except requests.exceptions.ConnectionError as e:
#         print(
#             f'{e}.\nFailed to establish a new connection with web.archive.org.'
#         )
#     except UnboundLocalError as e:
#         print(e)

# def display_tweet():
#     if mimetype[i] == 'application/json' or mimetype[
#             i] == 'text/html' or mimetype[i] == 'unk' or mimetype[
#                 i] == 'warc/revisit':
#         if is_RT[0] == True:
#             st.info('*Retweet*')
#         st.write(tweet_content[0])
#         st.write(f'**{user_info[0]}**')

#         st.divider()
#     else:
#         st.warning('MIME Type was not parsed.')

#         st.divider()

# def display_not_tweet():
#     original_link = delete_tweet_pathnames(clean_tweet(tweet_links[i]))

#     if status:
#         original_link = delete_tweet_pathnames(
#             f'https://twitter.com/{tweet_links[i]}')
#     elif not '://' in tweet_links[i]:
#         original_link = delete_tweet_pathnames(f'https://{tweet_links[i]}')

#     response_html = requests.get(original_link)

#     if mimetype[i] == 'text/html' or mimetype[i] == 'warc/revisit' or mimetype[
#             i] == 'unk':
#         if ('.jpg' in tweet_links[i] or '.png'
#                 in tweet_links[i]) and response_html.status_code == 200:
#             components.iframe(tweet_links[i], height=500, scrolling=True)
#         elif '/status/' not in original_link:
#             st.info("This isn't a status or is not available")
#         elif status or f'{st.session_state.current_handle}' not in original_link:
#             st.info(f'Replying to {st.session_state.current_handle}')
#         else:
#             components.iframe(clean_link(link), height=500, scrolling=True)

#     elif mimetype[i] == 'application/json':
#         try:
#             response_json = requests.get(link)

#             if response_json.status_code == 200:
#                 json_data = response_json.json()

#                 if 'data' in json_data:
#                     if 'text' in json_data['data']:
#                         json_text = json_data['data']['text']
#                     else:
#                         json_text = json_data['data']
#                 else:
#                     if 'text' in json_data:
#                         json_text = json_data['text']
#                     else:
#                         json_text = json_data

#                 st.code(json_text)
#                 st.json(json_data, expanded=False)

#                 st.divider()
#             else:
#                 st.error(response_json.status_code)

#                 st.divider()
#         except requests.exceptions.Timeout:
#             st.error('Connection to web.archive.org timed out.')
#             st.divider()
#         except requests.exceptions.ConnectionError:
#             st.error(
#                 'Failed to establish a new connection with web.archive.org.')
#             st.divider()
#         except UnboundLocalError:
#             st.empty()
#     else:
#         st.warning('MIME Type was not parsed.')
#         st.divider()

# try:
#     links = query_api(handle, saved_at)

#     parse = parse_links(links)
#     parsed_links = parse[0]
#     tweet_links = parse[1]
#     mimetype = parse[2]
#     timestamp = parse[3]

#     if links:
#         for i in range(tweets_per_page):

#             if tweet_links[i]:
#                 link = parsed_links[i]
#                 tweet = embed(tweet_links[i])

#                 status = check_double_status(link, tweet_links[i])

#                 if not not_available:
#                     attr(i)

#                     if tweet:
#                         status_code = tweet[0]
#                         tweet_content = tweet[1]
#                         user_info = tweet[2]
#                         is_RT = tweet[3]

#                         display_tweet()
#                     elif not tweet:
#                         display_not_tweet()

#                 if not_available:
#                     if not tweet:
#                         return_none_count += 1
#                         attr(i)

#                         display_not_tweet()

#     if not links:
#         print('Unable to query the Wayback Machine API.')
# except TypeError as e:
#     print(
#         f'{e}.\nRefresh this page and try again. If the problem persists [open an issue](https://github.com/claromes/waybacktweets/issues).'
#     )
