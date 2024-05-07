# Remove F821 error from ruff

# flake8: noqa: F821

from abc import ABC
from typing import Union
from enum import Enum
from dataclasses import dataclass, field
from collections import Counter
import json

import pandas as pd


class MeasurementTable(ABC):
    """
    Abstract class for handling the measurement tables.
    """

    def __init__(self, dataframe: pd.DataFrame):
        self.dataframe = self._clean_dataframe(dataframe)

    def __len__(self):
        return len(self.dataframe)

    def _clean_dataframe(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        return dataframe

    def get_values(self, column_name: str) -> list:
        """
        Get the values from a specific column in the dataframe.

        Args:
            column_name (str): The name of the column.

        Returns:
            list: A list of values from the specified column.
        """
        return self.dataframe[column_name].tolist()

    def get_series(self, column_name: str) -> pd.Series:
        """
        Get the values from a specific column in the dataframe.

        Args:
            column_name (str): The name of the column.

        Returns:
            pd.Series: A pandas series of values from the specified column.
        """
        return self.dataframe[column_name]

    def add_column(self, column_name: str, values: list) -> None:
        """
        Add a column to the dataframe.

        Args:
            column_name (str): The name of the column.
            values (list): A list of values to add to the column.
        """
        self.dataframe[column_name] = values

    def add_series(self, column_name: str, series: pd.Series) -> None:
        """
        Add a column to the dataframe.

        Args:
            column_name (str): The name of the column.
            series (pd.Series): A pandas series of values to add to the column.
        """
        self.dataframe[column_name] = series

    @property
    def columns(self):
        """
        Returns:
            list: A list of column names.
        """
        return self.dataframe.columns


class AnnotationTable(MeasurementTable):
    """
    Class for handling the annotation table.
    """

    def __init__(self, dataframe: pd.DataFrame):
        self._required_columns = ["Name", "ROI", "Area µm^2"]
        super().__init__(dataframe)

    def _clean_dataframe(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        if not self._check_requirements(dataframe):
            raise ValueError(
                f"Annotation table must contain the following columns: {self._required_columns}"
            )
        # removing line selections from database and keeping only polygons
        dataframe = dataframe.loc[dataframe.ROI == "Polygon"]
        # FIXME: this gets mangled later at some point. Maybe extracting?
        # dataframe["annotation"] = dataframe.Name

        if "PathCellObject" in dataframe.Name.unique():
            dataframe = dataframe.loc[dataframe.Name != "PathCellObject"]
            print("WARNING: PathCellObject removed from annotation table.")
            print("This is likely due to the presence of detections not belonging to any annotation.")
        
        if "PathAnnotationObject" in dataframe.Name.unique():
            dataframe = dataframe.loc[dataframe.Name != "PathAnnotationObject"]
            print("PathAnnotationObject removed from annotation table.")
        
        dataframe["annotation"] = dataframe.Name

        dataframe["region"] = dataframe.Name
        dataframe["area"] = dataframe["Area µm^2"] / 1000000

        return dataframe

    def _check_requirements(self, dataframe: pd.DataFrame) -> bool:
        return all(column in dataframe.columns for column in self._required_columns)


class DetectionTable(MeasurementTable):
    """
    Class for handling the detection table.
    """

    def __init__(self, dataframe: pd.DataFrame):
        # TODO: expand required columns
        self._required_columns = ["Name", "Nucleus: Area"]
        super().__init__(dataframe)

    def _clean_dataframe(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        if not self._check_requirements(dataframe):
            raise ValueError(
                f"Detection table must contain the following columns: {self._required_columns}"
            )
        dataframe = dataframe[dataframe[self._required_columns[1]].notna()]
        if "Image" in dataframe.Parent.unique():
            dataframe = dataframe.loc[dataframe.Parent != "Image"]
            print("'Image' removed from detection table.")
        return dataframe

    def _check_requirements(self, dataframe: pd.DataFrame) -> bool:
        return all(column in dataframe.columns for column in self._required_columns)


class ResultType(Enum):
    """
    Enumeration representing different types of results.
    
    Attributes:
        PERCENTAGE (str): Represents percentage results.
        DENSITY (str): Represents density results.
    """
    
    PERCENTAGE = "percentage"
    DENSITY = "density"


class Result:
    """
    Represents a result from an experiment.

    Attributes:
        name (str): The name of the result.
        experiment (str or list[str]): The name(s) of the experiment(s) associated with the result.
        groupby (list[str]): The columns to group the data by.
        measurements (list[str]): The measurements recorded in the result.
        data (pd.DataFrame): The data associated with the result.
    """

    def __init__(
        self,
        name: str,
        experiment: str | list[str],
        groupby: list[str],
        measurements: list[str],
        data: pd.DataFrame,
    ):
        self.name = name
        if isinstance(experiment, str):
            experiment = [experiment]
        self._experiment = experiment
        self.groupby = groupby
        self.measurements = measurements
        self.data = data

        if "experiment" not in self.groupby:
            if len(self._experiment) == 1:
                self.data["experiment"] = self._experiment[0]
            self.groupby.append("experiment")

        try:
            self._type = ResultType[self.name.upper()]
        except KeyError:
            self._type = None

    def __repr__(self):
        result_type = "percentages" if self.type == ResultType.PERCENTAGE else "densities"
        repr_str = f"Cell {result_type} from the experiment '{self.experiment}'\n"
        repr_str += f"Data grouped by {self.groupby}\n"
        repr_str += f"With measuremnts and metadata {self.measurements}\n"
        return repr_str
    
    def __len__(self):
        return len(self.data)

    def __len__(self):
        return len(self.data)

    def __add__(self, other: Union["Result", list["Result"]]) -> "Result":
        """
        Merge the result with another result.

        Args:
            other (Result | list[Result]): The other result to merge with.

        Raises:
            TypeError: If `other` is not a Result object or a list of Result objects.

        Returns:
            Result: The merged result.
        """
        return self._merge_results(other)

    @property
    def experiment(self) -> Union[str, list[str]]:
        """
        Returns the experiment(s) associated with the object.
        
        If there is only one experiment, it is returned as a single object.
        If there are multiple experiments, they are returned as a list.
        
        Returns:
            str | list[str]: The experiment(s) associated with the object.
        """
        if len(self._experiment) == 1:
            return self._experiment[0]
        return self._experiment

    @experiment.setter
    def experiment(self, name: Union[str, list[str]]) -> None:
        """
        Set the experiment name or list of experiment names.

        Args:
            name (str | list[str]): The name of the experiment or a list of experiment names.

        Raises:
            ValueError: If `name` is a string and there are already multiple experiments defined.

        """
        if isinstance(name, str) and len(self._experiment) == 1:
            self._experiment = [name]
        elif isinstance(name, str) and len(self._experiment) > 1:
            raise ValueError(
                f"Experiment is a list of experiments: {self._experiment}."
            )
        else:
            self._experiment = name

    @property
    def type(self) -> ResultType | None:
        '''
        Returns the type of the result.

        Returns:
            ResultType: The type of the result.
        '''
        return self._type

    @type.setter
    def type(self, value: ResultType) -> None:
        """
            Set the type of the object.

            Args:
                value (ResultType): The type of the object.

            Returns:
                None
            """
        self._type = value

    def head(self, n: int = 5) -> pd.DataFrame:
        """
        Return the first n rows of the data.

        Args:
            n (int, optional): The number of rows to return. Defaults to 5.

        Returns:
            pd.DataFrame: The first n rows of the data.
        """
        return self.data.head(n)

    def tail(self, n: int = 5) -> pd.DataFrame:
        """
        Return the last n rows of the data.

        Args:
            n (int, optional): The number of rows to return. Defaults to 5.

        Returns:
            pd.DataFrame: The last n rows of the data.
        """
        return self.data.tail(n)

    def to_excel(self, path: str) -> None:
        """
        Save the result to an Excel file.

        Args:
            path (str): The path to the Excel file.
        """
        self.data.to_excel(path)

    def to_csv(self, path: str) -> None:
        """
        Save the result to a CSV file.

        Args:
            path (str): The path to the CSV file.
        """
        self.data.to_csv(path)

    def to_graphpad(self, path: str, grouping_column: str, values: str) -> None:
        """
        Save the result to an Excel table suited for GraphPad Prism.

        Args:
            path (str): The path to the GraphPad Prism file.
            grouping_column (str): The name of the column to use for grouping.
            values (str): The name of the column to use for values.

        Raises:
            ValueError: If the grouping_column or values column is not found in the data.

        Returns:
            None
        """
        # FIXME: confirm whether pivot_table is the right method to use here
        if grouping_column not in self.groupby:
            exception_message = (
                f"Grouping {grouping_column} not found in groupby {self.groupby}."
            )
            raise ValueError(exception_message)
        if values not in self.measurements:
            exception_message = (
                f"Values {values} not found in measurements {self.measurements}."
            )
            raise ValueError(exception_message)
        df_graphpad = self.data.pivot_table(columns=grouping_column, values=values)
        df_graphpad.to_excel(path)
    
    def append(self, other: Union["Result", list["Result"]]) -> "Result":
        """
        Append the result with another result.

        Args:
            other (Result | list[Result]): The other result to append with.

        Raises:
            TypeError: If `other` is not a Result object or a list of Result objects.

        Returns:
            Result: The appended result.
        """
        return self._merge_results(other)

    def _merge_results(self, other: Union["Result", list["Result"]]) -> "Result":
        """
        Merge the result with another result.

        Args:
            other (Result | list[Result]): The other result to merge with.

        Raises:
            TypeError: If `other` is not a Result object or a list of Result objects.

        Returns:
            Result: The merged result.
        """
        if isinstance(other, Result):
            other = [other]
        elif not isinstance(other, list):
            raise TypeError(
                f"Expected Result or list of Result objects, got {type(other)}."
            )

        experiments = self._experiment.copy()

        dataframe = self.data.copy()

        # TODO: check that groupby and measurements are the same
        self._validate_matching_lists([self.groupby] + [result.groupby for result in other])
        self._validate_matching_lists([self.measurements] + [result.measurements for result in other])

        all_names = [self.name] + [result.name for result in other]
        new_name = " + ".join(all_names)

        for result in other:
            if isinstance(result.experiment, str):
                other_experiment = [result.experiment]
            else:
                other_experiment = result.experiment
            experiments.extend(other_experiment)
            dataframe = pd.concat([dataframe, result.data], ignore_index=True)

        return Result(
            name=new_name,
            experiment=experiments,
            groupby=self.groupby,
            measurements=self.measurements,
            data=dataframe,
        )

    def _validate_matching_lists(self, lists: list[list]) -> None:
        """
        Validates that the given lists have matching elements.

        Args:
            lists (list[list]): The lists to be validated.

        Raises:
            ValueError: If the lists do not have matching elements.
        """
        reference = Counter(lists[0])
        if not all(Counter(lst) == reference for lst in lists):
            common_elements = set.intersection(*[set(lst) for lst in lists])
            extra_elements = set.difference(*[set(lst) for lst in lists])

            exception_message = (
                f"Lists do not match. Common elements: {common_elements}. Extra elements: {extra_elements}."
            )
            raise ValueError(exception_message)

    def serialize(self) -> tuple[str, str]:
        json_data = {
            "name": self.name,
            "experiment": self.experiment,
            "groupby": self.groupby,
            "measurements": self.measurements,
        }

        csv_data = self.data.to_csv()
        return json.dumps(json_data), csv_data

    @staticmethod
    def deserialize(json_data: str, df: pd.DataFrame) -> "Result":
        json_data = json.loads(json_data)
        return Result(
            name=json_data["name"],
            experiment=json_data["experiment"],
            groupby=json_data["groupby"],
            measurements=json_data["measurements"],
            data=df,
        )


@dataclass
class MarkerSelection:
    """
    Class for defining custom combinations of markers.

    Attributes:
        name (str): The name of the marker selection.
        positive_selection (list): A list of markers that should be positive.
        negative_selection (list): A list of markers that should be negative.

    Examples:
        selection = MarkerSelection(
            name="MySelection",
            positive_selection=["Marker1", "Marker2"],
            negative_selection=["Marker3"]
        )
    """

    name: str
    positive_selection: list
    negative_selection: list = field(default_factory=list)

    def __post_init__(self):
        if isinstance(self.positive_selection, str):
            self.positive_selection = [self.positive_selection]
        if isinstance(self.negative_selection, str):
            self.negative_selection = [self.negative_selection]

    def validate(self, experiment: "HCRexperiment") -> bool:
        """
        Validate the marker selection.

        Args:
            experiment (HCRexperiment): An instance of the HCRexperiment class.

        Returns:
            bool: True if the selection is valid, False otherwise.
        """
        channels = experiment.channel_names
        for marker in self.positive_selection + self.negative_selection:
            if marker not in channels:
                return False
        return True
