""" This module contains the HCRexperiment class, which represents an HCR experiment."""
# pylint: disable=line-too-long

from pathlib import Path

import pandas as pd

from cell_typist.core.datatypes import AnnotationTable, DetectionTable


DATA_EXTENSIONS = {
    ".csv": pd.read_csv,
    ".xlsx": pd.read_excel,
    ".xls": pd.read_excel,
    ".tsv": pd.read_csv,
    ".txt": pd.read_csv,
}

SEPARATORS = {
    ".csv": ",",
    ".tsv": "\t",
    ".txt": "\t",
}


class HCRexperiment:
    """
    A class representing an HCR experiment.

    Attributes:
    name (str): The name of the experiment.
    annotations (AnnotationTable): The annotations of the experiment.
    detections (DetectionTable): The detections of the experiment.
    channel_names (list[str]): The channel names of the experiment.
    original_channel_names (list[str]): The original channel names of the experiment.
    """

    def __init__(
        self,
        name: str,
    ):
        self.name: str = name

        self._annotations: AnnotationTable = None
        self._detections: DetectionTable = None

        self.channels: list[str] = None
        self._channel_names: list[str] = None
        self._original_channel_names: list[str] = None

        self._metadata: list[str] = None

        self._thresholds: dict[str, float] = None

        self._raw_data: dict[pd.Series] = {}
        self.data: dict[pd.Series] = {}

    def __repr__(self) -> str:
        # TODO: update repr
        repr_str = f"HCR experiment called {self.name}\n"
        if self._annotations is not None:
            repr_str += f"{self.name} has {len(self._annotations)} annotations\n"
        if self._detections is not None:
            repr_str += f"{self.name} has {len(self._detections)} detections\n"

        if self._metadata:
            repr_str += f"{self.name} has the following metadata:\n"
            for meta in self._metadata:
                repr_str += f" - {meta}\n"

        if self._channel_names:
            repr_str += f"{self.name} has the following channels:\n"
            for channel in self._channel_names:
                repr_str += f" - {channel}\n"
        
        if self._thresholds:
            repr_str += f"{self.name} has the following thresholds:\n"
            for channel, threshold in self._thresholds.items():
                repr_str += f" - {channel}: {threshold}\n"

        return repr_str

    # TODO: evaluate whether this is a good idea
    # maybe better to access dataframes directly?
    def __getitem__(self, key) -> pd.Series | pd.DataFrame:
        """
        Returns the data for the given key.

        Parameters:
        key (str): The key to return the data for.

        Returns:
        pd.Series | pd.DataFrame: The data for the given key.
        """
        if key in self.data:
            return self.data[key]
        elif key in self._raw_data:
            return self._raw_data[key]
        elif isinstance(self._metadata, list) and key in self._metadata:
            return self._detections.get_series(key)
        else:
            raise KeyError(f"Key {key} not found.")

    # TODO: deprecate access?
    @property
    def annotations(self) -> AnnotationTable:
        """Returns the annotations of the experiment.

        Returns:
        AnnotationTable: The annotations of the experiment.
        """
        return self._annotations

    @property
    # TODO: deprecate access?
    def detections(self) -> DetectionTable:
        """Returns the detections of the experiment.

        Returns:
        DetectionTable: The detections of the experiment.
        """
        return self._detections

    @property
    def channel_names(self) -> list[str]:
        """Returns the channel names of the experiment.

        Returns:
        list[str]: The channel names of the experiment.
        """
        return self._channel_names

    @property
    def original_channel_names(self) -> list[str]:
        """Returns the original channel names of the experiment.

        Returns:
        list[str]: The original channel names of the experiment.
        """
        return self._original_channel_names

    @property
    def metadata(self) -> list[str]:
        """Returns the metadata of the experiment.

        Returns:
        list[str]: The metadata of the experiment.
        """
        return self._metadata

    @metadata.setter
    def metadata(self, metadata: list[str]) -> None:
        """
        Sets the metadata of the experiment.

        Parameters:
        metadata (list[str]): A list of metadata.
        """
        if not isinstance(metadata, list):
            raise TypeError(
                f"Expected metadata to be of type list, got {type(metadata)}"
            )
        self._metadata = metadata

    @property
    def thresholds(self) -> dict[str, float]:
        """Returns the thresholds of the experiment.

        Returns:
        dict[str, float]: The thresholds of the experiment.
        """
        return self._thresholds

    @thresholds.setter
    def thresholds(self, thresholds: dict[str, float]) -> None:
        """
        Sets the thresholds of the experiment.

        Parameters:
        thresholds (dict[str, float]): A dictionary of thresholds.
        """
        if not isinstance(thresholds, dict):
            raise TypeError(
                f"Expected thresholds to be of type dict, got {type(thresholds)}"
            )
        self._thresholds = thresholds

    def set_channel_names(self, channel_names: list[str]) -> None:
        """
        Sets the channel names for the experiment.

        Parameters:
        channel_names (list[str]): A list of channel names.
        """
        if not isinstance(channel_names, list):
            raise TypeError(
                f"Expected channel_names to be of type list, got {type(channel_names)}"
            )

        if len(channel_names) != len(self._original_channel_names):
            exception_str = f"Expected {len(self._original_channel_names)} channel names, got {len(channel_names)}"
            raise ValueError(exception_str)

        self._channel_names = channel_names

    @property
    def are_channels_defined(self) -> bool:
        """Returns whether the channels are defined.

        Returns:
        bool: Whether the channels are defined.
        """
        return self._channel_names is not None

    @property
    def is_expression_thresholded(self) -> bool:
        """Returns whether the expression is thresholded.

        Returns:
        bool: Whether the expression is thresholded.
        """
        return any(col for col in self.data if col.endswith("_pos"))

    def set_original_channel_names(self, original_channel_names: list[str]) -> None:
        """
        Sets the original channel names for the experiment.

        Parameters:
        original_channel_names (list[str]): A list of original channel names.
        """
        if not isinstance(original_channel_names, list):
            raise TypeError(
                f"Expected original_channel_names to be of type list, got {type(original_channel_names)}"
            )

        if len(original_channel_names) != len(self._channel_names):
            exception_str = f"Expected {len(self._channel_names)} original channel names, got {len(original_channel_names)}"
            raise ValueError(exception_str)

        self._original_channel_names = original_channel_names

    def add_detection_column(
        self, column_name: str, values: list, is_annotation: bool = False
    ) -> None:
        """
        Adds a column to the detections dataframe.

        Parameters:
        column_name (str): The name of the column.
        values (list): A list of values to add to the column.
        is_annotation (bool, optional): Specifies whether the column contains only annotation data. Defaults to False.

        Raises:
        ValueError: If the length of the values list does not match the length of the detections dataframe.

        Returns:
        None
        """
        if len(values) != len(self._detections):
            raise ValueError(
                f"Expected {len(self._detections)} values, got {len(values)}"
            )
        series = pd.Series(
            values, index=self._detections.dataframe.index, name=column_name
        )
        self._detections.add_series(column_name, series)
        if not is_annotation:
            self.data[column_name] = values

    def add_annotation_column(self, column_name: str, values: list) -> None:
        """
        Adds a column to the annotations dataframe.

        Parameters:
        column_name (str): The name of the column.
        values (list): A list of values to add to the column.

        Returns:
        None
        """
        self._annotations.add_column(column_name, values)
    
    def head(self, n: int = 10, dataset:str = "detections") -> pd.DataFrame:
        """
        Returns the first n rows of the detections or annotations dataframe.

        Parameters:
        n (int, optional): The number of rows to return. Defaults to 10.
        dataset (str, optional): The dataset to return the rows from. Defaults to "detections".

        Returns:
        pd.DataFrame: The first n rows of the detections or annotations dataframe.
        """
        if dataset == "detections":
            return self._detections.dataframe.head(n)
        elif dataset == "annotations":
            return self._annotations.dataframe.head(n)
        else:
            raise ValueError(f"Dataset {dataset} not supported. Choose from 'detections' and 'annotations'.")

    def load_qupath(self, annotation_data: str, detection_data: str) -> None:
        """
        Loads the data from the given annotation and detection files.

        Parameters:
        annotation_data (str): The path to the annotation data.
        detection_data (str): The path to the detection data.
        """
        annotation_data = self._parse_path(annotation_data)
        detection_data = self._parse_path(detection_data)

        df_annotations = self._concatenate_data(self._read_dataframes(annotation_data))
        df_detections = self._concatenate_data(self._read_dataframes(detection_data))

        for column in df_annotations.columns:
            self._raw_data[column] = df_annotations[column]

        self._annotations = AnnotationTable(df_annotations)
        self._detections = DetectionTable(df_detections)
        self._original_channel_names = self._extract_original_channel_names(
            self._detections.dataframe
        )

        # NOT NEEDED FOR NOW
        # new_columns = [
        #     column
        #     for column in self._detections.dataframe.columns
        #     if not column in df_detections.columns
        # ]
        # for column in new_columns:
        #     self.data[column] = self._detections.get_values(column)

    def _parse_path(self, path: str) -> list[Path]:
        """
        Parses the given path and returns a list of file paths.

        If the given path is a directory, returns a list of all file paths.
        If the given path is a file, returns a list containing only this file path.
        If the given path does not exist, raises a FileNotFoundError.

        Parameters:
        path (str): The path to parse. This can be a directory or a file.

        Returns:
        list[Path]: A list of file paths.

        Raises:
        FileNotFoundError: If the given path does not exist.
        """
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"Path {path} does not exist.")
        if path.is_dir():
            return [
                p for p in path.iterdir() if p.is_file() and p.suffix in DATA_EXTENSIONS
            ]
        else:
            return [path]

    def _read_dataframes(self, paths: list[Path]) -> list[pd.DataFrame]:
        """
        Reads the data from the given list of file paths and returns a list of pandas DataFrames.

        Parameters:
        paths (list[Path]): A list of file paths.

        Returns:
        list[pd.DataFrame]: A list of pandas DataFrames.
        """
        dataframes = []
        for file in paths:
            new_df = DATA_EXTENSIONS[file.suffix](file, sep=SEPARATORS[file.suffix])
            new_df["file"] = file.name
            dataframes.append(new_df)
        return dataframes

    def _concatenate_data(self, dataframes: list[pd.DataFrame]) -> pd.DataFrame:
        """
        Concatenates the given list of pandas DataFrames and returns the result.

        Parameters:
        dataframes (list[pd.DataFrame]): A list of pandas DataFrames.

        Returns:
        pd.DataFrame: The concatenated pandas DataFrame.
        """
        return pd.concat(dataframes, ignore_index=True)

    def _extract_original_channel_names(self, df: pd.DataFrame) -> list[str]:
        """
        Extracts the original channel names from the given pandas DataFrame.

        Parameters:
        df (pd.DataFrame): A pandas DataFrame.

        Returns:
        list[str]: A list of original channel names.
        """
        matches = df.columns.str.contains(r"\d: Num spots estimated")
        return df.columns[matches].to_list()


def load_qupath(
    experiment_name: str, annotation_data: str, detection_data: str
) -> HCRexperiment:
    """
    Loads the data from the given annotation and detection files.
    """
    experiment = HCRexperiment(name=experiment_name)
    experiment.load_qupath(annotation_data, detection_data)

    return experiment
