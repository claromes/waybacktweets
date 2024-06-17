"""
Exports the parsed archived tweets.
"""

import datetime
import os
import re
from typing import Any, Dict, List, Optional

import pandas as pd

from waybacktweets.api.visualize import HTMLTweetsVisualizer


class TweetsExporter:
    """
    Class responsible for exporting parsed archived tweets.

    Args:
        data (Dict[str, List[Any]]): The parsed archived tweets data.
        username (str): The username associated with the tweets.
        field_options (List[str]): The fields to be included in the exported data. For more details on each option, visit :ref:`field_options`.
    """  # noqa: E501

    def __init__(
        self, data: Dict[str, List[Any]], username: str, field_options: List[str]
    ):
        self.data = data
        self.username = username
        self.field_options = field_options
        self.formatted_datetime = self._datetime_now()
        self.filename = f"{self.username}_tweets_{self.formatted_datetime}"
        self.dataframe = self._create_dataframe()

    @staticmethod
    def _datetime_now() -> str:
        """
        Returns the current datetime, formatted as a string.

        Returns:
            The current datetime.
        """
        now = datetime.datetime.now()
        formatted_now = now.strftime("%Y%m%d%H%M%S")
        formatted_now = re.sub(r"\W+", "", formatted_now)

        return formatted_now

    @staticmethod
    def _transpose_matrix(
        data: Dict[str, List[Any]], fill_value: Optional[Any] = None
    ) -> List[List[Any]]:
        """
        Transposes a matrix, filling in missing values with a specified fill value if needed.

        Args:
            data (Dict[str, List[Any]]): The matrix to be transposed.
            fill_value (Optional[Any]): The value to fill in missing values with.

        Returns:
            The transposed matrix.
        """  # noqa: E501
        max_length = max(len(sublist) for sublist in data.values())

        filled_data = {
            key: value + [fill_value] * (max_length - len(value))
            for key, value in data.items()
        }

        data_transposed = [list(row) for row in zip(*filled_data.values())]

        return data_transposed

    def _create_dataframe(self) -> pd.DataFrame:
        """
        Creates a DataFrame from the transposed data.

        Returns:
            The DataFrame representation of the data.
        """
        data_transposed = self._transpose_matrix(self.data)

        df = pd.DataFrame(data_transposed, columns=self.field_options)

        return df

    def save_to_csv(self) -> None:
        """
        Saves the DataFrame to a CSV file.
        """
        csv_file_path = f"{self.filename}.csv"
        self.dataframe.to_csv(csv_file_path, index=False)

        print(f"Saved to {csv_file_path}")

    def save_to_json(self) -> None:
        """
        Saves the DataFrame to a JSON file.
        """
        json_file_path = f"{self.filename}.json"
        self.dataframe.to_json(json_file_path, orient="records", lines=False)

        print(f"Saved to {json_file_path}")

    def save_to_html(self) -> None:
        """
        Saves the DataFrame to an HTML file.
        """
        json_file_path = f"{self.filename}.json"

        if not os.path.exists(json_file_path):
            self.save_to_json()

        html_file_path = f"{self.filename}.html"

        html = HTMLTweetsVisualizer(json_file_path, html_file_path, self.username)

        html_content = html.generate()
        html.save(html_content)

        print(f"Saved to {html_file_path}")
