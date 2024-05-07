import json
import zipfile
from dataclasses import fields
from io import StringIO

import pandas as pd

from cell_typist.core.datatypes import Result


class ResultSerializer:
    """
    A class for serializing and deserializing Result objects.
    """

    def save(self, result: Result, path: str) -> None:
        """
        Save a Result object to a zip file.

        Args:
            result (Result): The Result object to be saved.
            path (str): The path to the zip file.

        Returns:
            None
        """
        if not path.endswith(".zip"):
            path += ".zip"

        json_data, csv_data = result.serialize()

        with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as zip_file:
            zip_file.writestr("result.json", json.dumps(json_data))
            zip_file.writestr("result.csv", csv_data)

    @staticmethod
    def load(path: str) -> Result:
        """
        Load a Result object from a zip file.

        Args:
            path (str): The path to the zip file.

        Returns:
            Result: The loaded Result object.
        """
        if not path.endswith(".zip"):
            raise ValueError("Path must be a zip file")

        with zipfile.ZipFile(path, "r") as zip_file:
            if (
                "result.json" not in zip_file.namelist()
                or "result.csv" not in zip_file.namelist()
            ):
                exception_message = (
                    "Zip file must contain 'result.json' and 'result.csv' files"
                )
                exception_message += f"\nFound: {zip_file.namelist()}"
                exception_message += "Is this a valid result file?"
                raise ValueError(exception_message)

            json_data = json.loads(zip_file.read("result.json"))
            with zip_file.open("result.csv") as csv_file:
                csv_data = StringIO(csv_file.read().decode("utf-8"))
                df = pd.read_csv(csv_data, index_col=0)
            return Result.deserialize(json_data, df)


def save_results(result: Result, path: str) -> None:
    """
    Save a Result object to a zip file.

    Args:
        result (Result): The Result object to be saved.
        path (str): The path to the zip file.

    Returns:
        None
    """
    ResultSerializer().save(result, path)


def load_results(path: str) -> Result:
    """
    Load a Result object from a zip file.

    Args:
        path (str): The path to the zip file.

    Returns:
        Result: The loaded Result object.
    """
    return ResultSerializer.load(path)
