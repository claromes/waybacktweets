import datetime
import os
import re

import pandas as pd

from waybacktweets.api.viz_tweets import HTMLTweetsVisualizer


class TweetsExporter:
    """Handles the exporting of parsed archived tweets."""

    def __init__(self, data, username, field_options):
        self.data = data
        self.username = username
        self.field_options = field_options
        self.formatted_datetime = self._datetime_now()
        self.filename = f"{self.username}_tweets_{self.formatted_datetime}"
        self.dataframe = self._create_dataframe(self)

    @staticmethod
    def _datetime_now():
        """Formats datetime."""
        now = datetime.datetime.now()
        formatted_now = now.strftime("%Y%m%d%H%M%S")
        formatted_now = re.sub(r"\W+", "", formatted_now)

        return formatted_now

    @staticmethod
    def _transpose_matrix(data, fill_value=None):
        """
        Transposes a matrix, filling in missing values with a specified fill value
        if needed.
        """
        max_length = max(len(sublist) for sublist in data.values())

        filled_data = {
            key: value + [fill_value] * (max_length - len(value))
            for key, value in data.items()
        }

        data_transposed = [list(row) for row in zip(*filled_data.values())]

        return data_transposed

    def _create_dataframe(self):
        """Creates a DataFrame from the transposed data."""
        data_transposed = self._transpose_matrix(self.data)

        df = pd.DataFrame(data_transposed, columns=self.field_options)

        return df

    def save_to_csv(self):
        """Saves the DataFrame to a CSV file."""
        csv_file_path = f"{self.filename}.csv"
        self.dataframe.to_csv(csv_file_path, index=False)

        print(f"Saved to {csv_file_path}")

    def save_to_json(self):
        """Saves the DataFrame to a JSON file."""
        json_file_path = f"{self.filename}.json"
        self.dataframe.to_json(json_file_path, orient="records", lines=False)

        print(f"Saved to {json_file_path}")

    def save_to_html(self):
        """Saves the DataFrame to an HTML file."""
        json_file_path = f"{self.filename}.json"

        if not os.path.exists(json_file_path):
            self.save_to_json()

        html_file_path = f"{self.filename}.html"

        html = HTMLTweetsVisualizer(json_file_path, html_file_path, self.username)

        html_content = html.generate()
        html.save(html_content)

        print(f"Saved to {html_file_path}")