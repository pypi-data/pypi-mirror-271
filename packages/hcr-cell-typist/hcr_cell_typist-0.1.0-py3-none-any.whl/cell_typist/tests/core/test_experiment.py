""" Tests for the Experiment class. """
# pylint: disable=redefined-outer-name
# pylint: disable=line-too-long
# pylint: disable=protected-access
# pylint: disable=missing-function-docstring

import tempfile
from pathlib import Path
import pandas as pd
import pytest
import cell_typist as ct
from cell_typist.core.experiment import HCRexperiment
from cell_typist.core.datatypes import AnnotationTable, DetectionTable
from cell_typist.preprocess.feature_extraction import (
    parse_file_names,
    define_channel_names,
)
from cell_typist.measure.measure import threshold_expression


@pytest.fixture
def annotation_data_mock():
    # Create a temporary file
    with tempfile.NamedTemporaryFile(suffix=".tsv", delete=False) as tf:
        # Create a small DataFrame
        df = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
        # Write the DataFrame to the temporary file
        df.to_csv(tf.name, sep="\t", index=False)
    # Return the path to the temporary file
    return tf.name


@pytest.fixture
def detection_data_mock():
    # Create a temporary file
    with tempfile.NamedTemporaryFile(suffix=".tsv", delete=False) as tf:
        # Create a small DataFrame
        df = pd.DataFrame({"C": [5, 6], "D": [7, 8]})
        # Write the DataFrame to the temporary file
        df.to_csv(tf.name, sep="\t", index=False)
    # Return the path to the temporary file
    return tf.name


@pytest.fixture
def base_experiment():
    """
    Fixture that returns an instance of the experiment for testing.
    """
    annotation_data = Path("cell_typist/tests/sample_data/annotation").absolute()
    detection_data = Path("cell_typist/tests/sample_data/detection").absolute()

    experiment = ct.load_qupath(
        experiment_name="Experiment",
        annotation_data=str(annotation_data),
        detection_data=str(detection_data),
    )
    return experiment


@pytest.fixture
def experiment_with_metadata(base_experiment):
    experiment = parse_file_names(
        base_experiment,
        template="strain_age_tissue_experiment_staining_magnification_timepoint_fish",
        separator="_",
    )
    experiment = define_channel_names(
        experiment, template="Ollineage-cldnk", separator="-"
    )
    return experiment


def test_HCRexperiment_creation():
    experiment = HCRexperiment("test")
    assert isinstance(experiment, HCRexperiment), "HCRexperiment object not created"
    assert experiment.name == "test", "HCRexperiment name not set correctly"


def test_HCRexperiment_load_qupath_mock(annotation_data_mock, detection_data_mock):
    with pytest.raises(Exception):
        experiment = HCRexperiment("test")
        experiment.load_qupath(annotation_data_mock, detection_data_mock)


def test_HCRexperiment_init(base_experiment):
    assert isinstance(base_experiment.name, str), "Name not initialized correctly"
    assert isinstance(
        base_experiment._annotations, (type(None), AnnotationTable)
    ), "_annotations not initialized correctly"
    assert isinstance(
        base_experiment._detections, (type(None), DetectionTable)
    ), "_detections not initialized correctly"
    assert isinstance(
        base_experiment.channels, (type(None), list)
    ), "Channels not initialized correctly"
    assert isinstance(
        base_experiment._channel_names, (type(None), list)
    ), "_channel_names not initialized correctly"
    assert isinstance(
        base_experiment._original_channel_names, (type(None), list)
    ), "_original_channel_names not initialized correctly"
    assert isinstance(
        base_experiment._metadata, (type(None), list)
    ), "_metadata not initialized correctly"
    assert isinstance(
        base_experiment._thresholds, (type(None), dict)
    ), "_thresholds not initialized correctly"
    assert isinstance(
        base_experiment._raw_data, (type(None), dict)
    ), "_raw_data not initialized correctly"
    assert isinstance(
        base_experiment.data, (type(None), dict)
    ), "Data not initialized correctly"


def test_HCRexperiment_repr_no_data(base_experiment):
    base_experiment.name = "test"
    base_experiment._annotations = None
    base_experiment._detections = None
    base_experiment._metadata = None
    base_experiment._channel_names = None
    base_experiment._thresholds = None
    expected_repr = "HCR experiment called test\n"
    assert (
        str(base_experiment) == expected_repr
    ), "__repr__ not returning correct string for no data"


def test_HCRexperiment_repr_with_data(base_experiment):
    base_experiment.name = "test"
    base_experiment._annotations = [1, 2, 3]
    base_experiment._detections = [1, 2]
    base_experiment._metadata = ["meta1", "meta2"]
    base_experiment._channel_names = ["channel1", "channel2"]
    base_experiment._thresholds = {"channel1": 0.5, "channel2": 0.7}
    expected_repr = (
        "HCR experiment called test\n"
        "test has 3 annotations\n"
        "test has 2 detections\n"
        "test has the following metadata:\n"
        " - meta1\n"
        " - meta2\n"
        "test has the following channels:\n"
        " - channel1\n"
        " - channel2\n"
        "test has the following thresholds:\n"
        " - channel1: 0.5\n"
        " - channel2: 0.7\n"
    )
    assert (
        str(base_experiment) == expected_repr
    ), "__repr__ not returning correct string for data"


def test_HCRexperiment_getitem_data(base_experiment):
    base_experiment.data = {"test_key": pd.Series([1, 2, 3])}
    expected_output = pd.Series([1, 2, 3])
    assert base_experiment["test_key"].equals(
        expected_output
    ), "__getitem__ not returning correct data for key in data"


def test_HCRexperiment_getitem_raw_data(base_experiment):
    base_experiment._raw_data = {"test_key": pd.Series([4, 5, 6])}
    expected_output = pd.Series([4, 5, 6])
    assert base_experiment["test_key"].equals(
        expected_output
    ), "__getitem__ not returning correct data for key in _raw_data"


def test_HCRexperiment_getitem_metadata(experiment_with_metadata):
    result = experiment_with_metadata["age"]
    pd.testing.assert_series_equal(result, experiment_with_metadata._detections.dataframe["age"], check_names=False)


def test_HCRexperiment_getitem_key_error(base_experiment):
    with pytest.raises(KeyError):
        base_experiment["non_existent_key"]


def test_HCRexperiment_annotations_property(base_experiment):
    # Test that the annotations property returns an AnnotationTable or None
    assert isinstance(
        base_experiment.annotations, (type(None), AnnotationTable)
    ), "Annotations property not returning correct type"


def test_HCRexperiment_annotations_property_value(base_experiment):
    # Test that the annotations property returns the correct value
    assert (
        base_experiment.annotations == base_experiment._annotations
    ), "Annotations property not returning correct value"


def test_HCRexperiment_detections_property(base_experiment):
    # Test that the detections property returns a DetectionTable or None
    assert isinstance(
        base_experiment.detections, (type(None), DetectionTable)
    ), "Detections property not returning correct type"


def test_HCRexperiment_detections_property_value(base_experiment):
    # Test that the detections property returns the correct value
    assert (
        base_experiment.detections == base_experiment._detections
    ), "Detections property not returning correct value"


def test_HCRexperiment_channel_names_property(base_experiment):
    # Test that the channel_names property returns a list or None
    assert isinstance(
        base_experiment.channel_names, (type(None), list)
    ), "channel_names property not returning correct type"


def test_HCRexperiment_channel_names_property_value(base_experiment):
    # Test that the channel_names property returns the correct value
    assert (
        base_experiment.channel_names == base_experiment._channel_names
    ), "channel_names property not returning correct value"


def test_HCRexperiment_original_channel_names_property(base_experiment):
    # Test that the original_channel_names property returns a list or None
    assert isinstance(
        base_experiment.original_channel_names, (type(None), list)
    ), "original_channel_names property not returning correct type"


def test_HCRexperiment_metadata_property(base_experiment):
    # Test that the metadata property returns a list or None
    assert isinstance(
        base_experiment.metadata, (type(None), list)
    ), "metadata property not returning correct type"
    base_experiment._metadata = ["test1", "test2"]
    assert (
        base_experiment.metadata == base_experiment._metadata
    ), "metadata property not returning correct value"


def test_HCRexperiment_metadata_setter(base_experiment):
    # Test that the metadata setter sets the correct type
    base_experiment.metadata = ["test1", "test2"]
    assert isinstance(
        base_experiment._metadata, list
    ), "Metadata setter not setting correct type"


def test_HCRexperiment_metadata_setter_value(base_experiment):
    # Test that the metadata setter sets the correct value
    base_experiment.metadata = ["test1", "test2"]
    assert base_experiment._metadata == [
        "test1",
        "test2",
    ], "Metadata setter not setting correct value"


def test_HCRexperiment_metadata_setter_type_check(base_experiment):
    # Test that the metadata setter raises a TypeError when setting a non-list value
    with pytest.raises(TypeError):
        base_experiment.metadata = "test"


def test_HCRexperiment_original_channel_names_property_value(base_experiment):
    # Test that the original_channel_names property returns the correct value
    assert (
        base_experiment.original_channel_names
        == base_experiment._original_channel_names
    ), "original_channel_names property not returning correct value"


def test_HCRexperiment_thresholds_property(base_experiment):
    # Test that the thresholds property returns a dict or None
    assert isinstance(
        base_experiment.thresholds, (type(None), dict)
    ), "thresholds property not returning correct type"
    base_experiment._thresholds = {"test1": 1.0, "test2": 2.0}
    assert (
        base_experiment.thresholds == base_experiment._thresholds
    ), "thresholds property not returning correct value"


def test_HCRexperiment_thresholds_setter(base_experiment):
    # Test that the thresholds setter sets the correct type
    base_experiment.thresholds = {"test1": 1.0, "test2": 2.0}
    assert isinstance(
        base_experiment._thresholds, dict
    ), "Thresholds setter not setting correct type"


def test_HCRexperiment_thresholds_setter_value(base_experiment):
    # Test that the thresholds setter sets the correct value
    base_experiment.thresholds = {"test1": 1.0, "test2": 2.0}
    assert base_experiment._thresholds == {
        "test1": 1.0,
        "test2": 2.0,
    }, "Thresholds setter not setting correct value"


def test_HCRexperiment_thresholds_setter_type_check(base_experiment):
    # Test that the thresholds setter raises a TypeError when setting a non-dict value
    with pytest.raises(TypeError):
        base_experiment.thresholds = "test"


def test_HCRexperiment_set_channel_names(base_experiment):
    # Test that the set_channel_names method sets the correct type
    base_experiment.set_channel_names(["test1", "test2"])
    assert isinstance(
        base_experiment._channel_names, list
    ), "set_channel_names method not setting correct type"


def test_HCRexperiment_set_channel_names_value(base_experiment):
    # Test that the set_channel_names method sets the correct value
    base_experiment.set_channel_names(["test1", "test2"])
    assert base_experiment._channel_names == [
        "test1",
        "test2",
    ], "set_channel_names method not setting correct value"


def test_HCRexperiment_set_channel_names_type_check(base_experiment):
    # Test that the set_channel_names method raises a TypeError when setting a non-list value
    with pytest.raises(TypeError):
        base_experiment.set_channel_names("test")


def test_HCRexperiment_set_channel_names_length_check(base_experiment):
    # Test that the set_channel_names method raises a ValueError when setting a list of incorrect length
    with pytest.raises(ValueError):
        base_experiment.set_channel_names(["test1", "test2", "test3"])


def test_HCRexperiment_are_channels_defined_property(base_experiment):
    # Test that the are_channels_defined property returns a bool
    assert isinstance(
        base_experiment.are_channels_defined, bool
    ), "are_channels_defined property not returning correct type"


def test_HCRexperiment_are_channels_defined_property_value_when_channels_are_not_defined(
    base_experiment,
):
    # Test that the are_channels_defined property returns False when channels are not defined
    base_experiment._channel_names = None
    assert (
        base_experiment.are_channels_defined == False
    ), "are_channels_defined property not returning correct value when channels are not defined"


def test_HCRexperiment_are_channels_defined_property_value_when_channels_are_defined(
    base_experiment,
):
    # Test that the are_channels_defined property returns True when channels are defined
    base_experiment._channel_names = ["test1", "test2"]
    assert (
        base_experiment.are_channels_defined == True
    ), "are_channels_defined property not returning correct value when channels are defined"


def test_HCRexperiment_is_expression_thresholded_property(experiment_with_metadata):
    # Test that the is_expression_thresholded property returns a boolean
    assert isinstance(
        experiment_with_metadata.is_expression_thresholded, bool
    ), "is_expression_thresholded property not returning correct type"


def test_HCRexperiment_is_expression_thresholded_property_value_when_false(
    experiment_with_metadata,
):
    # Test that the is_expression_thresholded property returns False when no column ends with "_pos"
    experiment_with_metadata.data = {"column1": [], "column2": []}
    assert (
        experiment_with_metadata.is_expression_thresholded == False
    ), "is_expression_thresholded property not returning correct value when no column ends with '_pos'"


def test_HCRexperiment_is_expression_thresholded_property_value_when_true(
    experiment_with_metadata,
):
    # Test that the is_expression_thresholded property returns True when at least one column ends with "_pos"
    experiment_with_metadata.data = {"column1": [], "column2_pos": []}
    assert (
        experiment_with_metadata.is_expression_thresholded == True
    ), "is_expression_thresholded property not returning correct value when at least one column ends with '_pos'"


def test_HCRexperiment_set_original_channel_names_method(experiment_with_metadata):
    # Test that the set_original_channel_names method sets the _original_channel_names attribute correctly
    original_channel_names = ["channel1", "channel2"]
    experiment_with_metadata._channel_names = ["channel1", "channel2"]
    experiment_with_metadata.set_original_channel_names(original_channel_names)
    assert (
        experiment_with_metadata._original_channel_names == original_channel_names
    ), "set_original_channel_names method not setting _original_channel_names attribute correctly"


def test_HCRexperiment_set_original_channel_names_method_raises_type_error(
    experiment_with_metadata,
):
    # Test that the set_original_channel_names method raises a TypeError when the input is not a list
    with pytest.raises(TypeError):
        experiment_with_metadata.set_original_channel_names("not a list")


def test_HCRexperiment_set_original_channel_names_method_raises_value_error(
    experiment_with_metadata,
):
    # Test that the set_original_channel_names method raises a ValueError when the length of the input list does not match the length of the _channel_names attribute
    with pytest.raises(ValueError):
        experiment_with_metadata._channel_names = ["channel1", "channel2"]
        experiment_with_metadata.set_original_channel_names(["channel1"])


def test_HCRexperiment_add_detection_column_method(experiment_with_metadata):
    # Test that the add_detection_column method adds a column to the detections dataframe
    column_name = "new_column"
    values = list(range(len(experiment_with_metadata._detections.dataframe)))
    experiment_with_metadata.add_detection_column(column_name, values)
    assert (
        column_name in experiment_with_metadata._detections.dataframe.columns
    ), "add_detection_column method not adding column to detections dataframe"
    assert (
        list(experiment_with_metadata._detections.dataframe[column_name]) == values
    ), "add_detection_column method not adding correct values to new column"


def test_HCRexperiment_add_detection_column_method_raises_value_error(
    experiment_with_metadata,
):
    # Test that the add_detection_column method raises a ValueError when the length of the values list does not match the length of the detections dataframe
    with pytest.raises(ValueError):
        column_name = "new_column"
        values = list(range(len(experiment_with_metadata._detections.dataframe) + 1))
        experiment_with_metadata.add_detection_column(column_name, values)


def test_HCRexperiment_add_annotation_column_method(experiment_with_metadata):
    # Test that the add_annotation_column method adds a column to the annotations dataframe
    column_name = "new_column"
    values = list(range(len(experiment_with_metadata._annotations.dataframe)))
    experiment_with_metadata.add_annotation_column(column_name, values)
    assert (
        column_name in experiment_with_metadata._annotations.dataframe.columns
    ), "add_annotation_column method not adding column to annotations dataframe"
    assert (
        list(experiment_with_metadata._annotations.dataframe[column_name]) == values
    ), "add_annotation_column method not adding correct values to new column"


def test_HCRexperiment_add_annotation_column_method_raises_value_error(
    experiment_with_metadata,
):
    # Test that the add_annotation_column method raises a ValueError when the length of the values list does not match the length of the annotations dataframe
    with pytest.raises(ValueError):
        column_name = "new_column"
        values = list(range(len(experiment_with_metadata._annotations.dataframe) + 1))
        experiment_with_metadata.add_annotation_column(column_name, values)


def test_HCRexperiment_parse_path_method_directory(experiment_with_metadata, tmp_path):
    # Test that the _parse_path method correctly parses a directory path
    # Create a temporary directory and file
    file_path = tmp_path / "test_file.txt"
    file_path.write_text("test content")
    # Call the _parse_path method and check the result
    result = experiment_with_metadata._parse_path(str(tmp_path))
    assert (
        len(result) == 1
    ), "_parse_path method not returning correct number of file paths for directory"
    assert (
        result[0] == file_path
    ), "_parse_path method not returning correct file paths for directory"


def test_HCRexperiment_parse_path_method_file(experiment_with_metadata, tmp_path):
    # Test that the _parse_path method correctly parses a file path
    # Create a temporary file
    file_path = tmp_path / "test_file.txt"
    file_path.write_text("test content")
    # Call the _parse_path method and check the result
    result = experiment_with_metadata._parse_path(str(file_path))
    assert (
        len(result) == 1
    ), "_parse_path method not returning correct number of file paths for file"
    assert (
        result[0] == file_path
    ), "_parse_path method not returning correct file paths for file"


def test_HCRexperiment_parse_path_method_raises_file_not_found_error(
    experiment_with_metadata,
):
    # Test that the _parse_path method raises a FileNotFoundError when the path does not exist
    with pytest.raises(FileNotFoundError):
        experiment_with_metadata._parse_path("nonexistent_path")


def test_HCRexperiment_read_dataframes_method(
    experiment_with_metadata, annotation_data_mock, detection_data_mock
):
    # Test that the _read_dataframes method reads the data correctly and returns a list of pandas DataFrames
    paths = [Path(annotation_data_mock), Path(detection_data_mock)]
    dataframes = experiment_with_metadata._read_dataframes(paths)
    assert (
        len(dataframes) == 2
    ), "_read_dataframes method not returning correct number of dataframes"
    assert all(
        isinstance(df, pd.DataFrame) for df in dataframes
    ), "_read_dataframes method not returning dataframes"
    assert all(
        "file" in df.columns for df in dataframes
    ), "_read_dataframes method not adding file column to dataframes"
    assert all(
        df["file"][0] == path.name for df, path in zip(dataframes, paths)
    ), "_read_dataframes method not adding correct file names to file column"


def test_HCRexperiment_read_dataframes_method_raises_file_not_found_error(
    experiment_with_metadata,
):
    # Test that the _read_dataframes method raises a FileNotFoundError when the given files do not exist
    with pytest.raises(FileNotFoundError):
        paths = [Path("nonexistent_file1.csv"), Path("nonexistent_file2.csv")]
        experiment_with_metadata._read_dataframes(paths)


def test_HCRexperiment_read_dataframes_method_raises_wrong_extension_error(
    experiment_with_metadata,
):
    # Test that the _read_dataframes method raises a WrongExtensionError when the given files do not have the correct extension
    with pytest.raises(KeyError):
        paths = [Path("nonexistent_file1.jpg"), Path("nonexistent_file2.jpg")]
        experiment_with_metadata._read_dataframes(paths)


def test_HCRexperiment_concatenate_data_method(experiment_with_metadata):
    # Test that the _concatenate_data method correctly concatenates a list of pandas DataFrames
    # Create a list of small DataFrames
    dfs = [
        pd.DataFrame({"A": [1, 2], "B": [3, 4]}),
        pd.DataFrame({"A": [5, 6], "B": [7, 8]}),
    ]
    # Call the _concatenate_data method and check the result
    result = experiment_with_metadata._concatenate_data(dfs)
    assert isinstance(
        result, pd.DataFrame
    ), "_concatenate_data method not returning a DataFrame"
    assert (
        len(result) == 4
    ), "_concatenate_data method not concatenating DataFrames correctly"
    assert list(result.columns) == [
        "A",
        "B",
    ], "_concatenate_data method not preserving DataFrame columns"
    assert list(result["A"]) == [
        1,
        2,
        5,
        6,
    ], "_concatenate_data method not preserving DataFrame data"
    assert list(result["B"]) == [
        3,
        4,
        7,
        8,
    ], "_concatenate_data method not preserving DataFrame data"


def test_HCRexperiment_extract_original_channel_names_method(experiment_with_metadata):
    # Test that the _extract_original_channel_names method correctly extracts the original channel names
    # Create a DataFrame with some columns that match the pattern and some that don't
    df = pd.DataFrame(
        columns=["1: Num spots estimated", "2: Num spots estimated", "A", "B"]
    )
    # Call the _extract_original_channel_names method and check the result
    result = experiment_with_metadata._extract_original_channel_names(df)
    assert isinstance(
        result, list
    ), "_extract_original_channel_names method not returning a list"
    assert (
        len(result) == 2
    ), "_extract_original_channel_names method not returning correct number of channel names"
    assert result == [
        "1: Num spots estimated",
        "2: Num spots estimated",
    ], "_extract_original_channel_names method not returning correct channel names"


def test_HCRexperiment_extract_original_channel_names_method_no_matches(
    experiment_with_metadata,
):
    # Test that the _extract_original_channel_names method returns an empty list when there are no matches
    # Create a DataFrame with no columns that match the pattern
    df = pd.DataFrame(columns=["A", "B"])
    # Call the _extract_original_channel_names method and check the result
    result = experiment_with_metadata._extract_original_channel_names(df)
    assert isinstance(
        result, list
    ), "_extract_original_channel_names method not returning a list for no matches"
    assert (
        result == []
    ), "_extract_original_channel_names method not returning an empty list for no matches"


def test_HCRexperiment_head_detections(base_experiment):
    base_experiment._detections.dataframe = pd.DataFrame(
        {"C": range(20), "D": range(20)}
    )
    result = base_experiment.head(n=5, dataset="detections")
    assert (
        len(result) == 5
    ), "Head method does not return correct number of rows for detections"
    assert list(result.columns) == [
        "C",
        "D",
    ], "Head method does not return correct columns for detections"


def test_HCRexperiment_head_annotations(base_experiment):
    base_experiment._annotations.dataframe = pd.DataFrame(
        {"A": range(20), "B": range(20)}
    )
    result = base_experiment.head(n=5, dataset="annotations")
    assert (
        len(result) == 5
    ), "Head method does not return correct number of rows for annotations"
    assert list(result.columns) == [
        "A",
        "B",
    ], "Head method does not return correct columns for annotations"


def test_HCRexperiment_head_unsupported_dataset(base_experiment):
    with pytest.raises(ValueError):
        base_experiment.head(n=5, dataset="unsupported")
