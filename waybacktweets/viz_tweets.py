"""
Generates an HTML file to visualize the parsed data.
"""

import json


def read_json(json_file_path):
    """Reads and loads JSON data from a specified file path."""
    with open(json_file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def generate_html(json_content, username):
    """Generates an HTML file."""
    html = f'<html>\n<head>\n<title>@{username} archived tweets</title>\n'
    html += '<style>\n'
    html += 'body { font-family: monospace; background-color: #f5f8fa; color: #1c1e21; margin: 0; padding: 20px; }\n'
    html += '.container { display: flex; flex-wrap: wrap; gap: 20px; }\n'
    html += '.tweet { flex: 0 1 calc(33.33% - 20px); background-color: #fff; border: 1px solid #e1e8ed; border-radius: 10px; padding: 15px; overflow-wrap: break-word; margin: auto; }\n'
    html += '.tweet strong { font-weight: bold; }\n'
    html += '.tweet a { color: #1da1f2; text-decoration: none; }\n'
    html += '.tweet a:hover { text-decoration: underline; }\n'
    html += 'h1 { text-align: center; }\n'
    html += '</style>\n'
    html += '</head>\n<body>\n'
    html += f'<h1>@{username} archived tweets</h1>\n'
    html += '<div class="container">\n'

    for tweet in json_content:
        html += '<div class="tweet">\n'
        html += f'<p><strong>Archived Timestamp:</strong> {tweet["archived_timestamp"]}</p>\n'
        html += f'<p><strong>Archived URL Key:</strong> {tweet["archived_urlkey"]}</p>\n'
        html += f'<p><strong>Tweet:</strong> <a href="{tweet["tweet"]}">{tweet["tweet"]}</a></p>\n'
        html += f'<p><strong>Archived Tweet:</strong> <a href="{tweet["archived_tweet"]}">{tweet["archived_tweet"]}</a></p>\n'
        html += f'<p><strong>Parsed Tweet:</strong> <a href="{tweet["parsed_tweet"]}">{tweet["parsed_tweet"]}</a></p>\n'
        html += f'<p><strong>Parsed Tweet Mimetype JSON:</strong> {tweet["parsed_tweet_mimetype_json"]}</p>\n'
        html += f'<p><strong>Parsed Archived Tweet:</strong> <a href="{tweet["parsed_archived_tweet"]}">{tweet["parsed_archived_tweet"]}</a></p>\n'
        html += f'<p><strong>Archived Mimetype:</strong> {tweet["archived_mimetype"]}</p>\n'
        html += f'<p><strong>Archived Statuscode:</strong> {tweet["archived_statuscode"]}</p>\n'
        html += f'<p><strong>Archived Digest:</strong> {tweet["archived_digest"]}</p>\n'
        html += f'<p><strong>Archived Length:</strong> {tweet["archived_length"]}</p>\n'
        html += f'<p><strong>Available Tweet Content:</strong> {tweet["available_tweet_content"]}</p>\n'
        html += f'<p><strong>Available Tweet Is Retweet:</strong> {tweet["available_tweet_is_RT"]}</p>\n'
        html += f'<p><strong>Available Tweet Username:</strong> {tweet["available_tweet_username"]}</p>\n'
        html += '</div>\n'

    html += '</div>\n'
    html += '</body>\n</html>'

    return html


def save_html(html_file_path, html_content):
    """Saves the generated HTML."""
    with open(html_file_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
