import pandas as pd
import re
import datetime


def datetime_now():
    now = datetime.datetime.now()

    formatted_now = now.strftime("%Y%m%d%H%M%S")

    formatted_now = re.sub(r'\W+', '', formatted_now)

    return formatted_now


def response_tweets_csv(data, username):
    data_transposed = list(zip(*data))

    formatted_datetime = datetime_now()
    filename = f'{username}_tweets_{formatted_datetime}'

    df = pd.DataFrame(data_transposed,
                      columns=[
                          'archived_urlkey', 'archived_timestamp', 'tweet',
                          'archived_tweet', 'parsed_tweet',
                          'parsed_archived_tweet', 'archived_mimetype',
                          'archived_statuscode', 'archived_digest',
                          'archived_length'
                      ])

    csv_file_path = f'{filename}.csv'
    df.to_csv(csv_file_path, index=False)

    json_file_path = f'{filename}.json'
    df.to_json(json_file_path, orient='records', lines=False)

    print(f'Done. Check the files {filename}.csv and {filename}.json')
