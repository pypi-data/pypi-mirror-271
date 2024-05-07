""" Tests for cell_typist.core.datatypes """
# pylint: disable=redefined-outer-name
# pylint: disable=line-too-long
# pylint: disable=protected-access
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=useless-super-delegation

import json
import pytest
import pandas as pd

from cell_typist.core.datatypes import (
    MeasurementTable,
    AnnotationTable,
    DetectionTable,
    ResultType,
    Result,
    MarkerSelection,
)


class ConcreteMeasurementTable(MeasurementTable):
    def __init__(self, dataframe: pd.DataFrame):
        super().__init__(dataframe)


@pytest.fixture
def concrete_measurement_table():
    df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
    return ConcreteMeasurementTable(df)


def test_measurement_table_len(concrete_measurement_table):
    assert len(concrete_measurement_table) == 3


def test_measurement_table_get_values(concrete_measurement_table):
    assert concrete_measurement_table.get_values("A") == [1, 2, 3]


def test_measurement_table_get_series(concrete_measurement_table):
    assert concrete_measurement_table.get_series("A").equals(pd.Series([1, 2, 3]))


def test_measurement_table_add_column(concrete_measurement_table):
    concrete_measurement_table.add_column("C", [7, 8, 9])
    assert "C" in concrete_measurement_table.columns
    assert concrete_measurement_table.get_values("C") == [7, 8, 9]


def test_measurement_table_add_series(concrete_measurement_table):
    series = pd.Series([10, 11, 12], name="D")
    concrete_measurement_table.add_series("D", series)
    assert "D" in concrete_measurement_table.columns
    assert concrete_measurement_table.get_series("D").equals(series)


def test_measurement_table_columns(concrete_measurement_table):
    assert list(concrete_measurement_table.columns) == ["A", "B"]


@pytest.fixture
def concrete_annotation_table():
    df = pd.DataFrame(
        {
            "Name": ["a", "b", "c"],
            "ROI": ["Polygon", "Line", "Polygon"],
            "Area µm^2": [1, 2, 3],
        }
    )
    return AnnotationTable(df)


def test_annotation_table_init(concrete_annotation_table):
    assert isinstance(concrete_annotation_table, AnnotationTable)


def test_annotation_table_clean_dataframe(concrete_annotation_table):
    cleaned_df = concrete_annotation_table._clean_dataframe(
        concrete_annotation_table.dataframe
    )
    assert "annotation" in cleaned_df.columns
    assert "area" in cleaned_df.columns


def test_annotation_table_check_requirements():
    with pytest.raises(ValueError):
        bad_df = pd.DataFrame(
            {"Name": ["a", "b", "c"], "ROI": ["Polygon", "Line", "Polygon"]}
        )
        AnnotationTable(bad_df)


@pytest.fixture
def concrete_detection_table():
    df = pd.DataFrame({"Name": ["a", "b", "c"], "Nucleus: Area": [1, 2, 3], "Parent": ["A", "B", "C"]})
    return DetectionTable(df)


def test_detection_table_init(concrete_detection_table):
    assert isinstance(concrete_detection_table, DetectionTable)


def test_detection_table_clean_dataframe(concrete_detection_table):
    df = concrete_detection_table.dataframe
    cleaned_df = concrete_detection_table._clean_dataframe(df)
    assert "Name" in cleaned_df.columns
    assert "Nucleus: Area" in cleaned_df.columns


def test_detection_table_check_requirements():
    with pytest.raises(ValueError):
        bad_df = pd.DataFrame(pd.DataFrame({"Name": ["a", "b", "c"]}))
        DetectionTable(bad_df)


@pytest.fixture
def result_data():
    df = pd.DataFrame(
        {
            "group1": ["A", "B", "A", "B"],
            "group2": ["X", "X", "Y", "Y"],
            "measurement1": [1, 2, 3, 4],
            "measurement2": [5, 6, 7, 8],
        }
    )
    return Result(
        name="Test Result",
        experiment="Test Experiment",
        groupby=["group1", "group2"],
        measurements=["measurement1", "measurement2"],
        data=df,
    )


def test_result_init_single_experiment(result_data):
    assert result_data.name == "Test Result"
    assert result_data._experiment == ["Test Experiment"]
    assert result_data.groupby == ["group1", "group2", "experiment"]
    assert result_data.measurements == ["measurement1", "measurement2"]
    assert "experiment" in result_data.data.columns
    assert result_data.data["experiment"].equals(
        pd.Series(
            ["Test Experiment", "Test Experiment", "Test Experiment", "Test Experiment"]
        )
    )


def test_result_init_multiple_experiments():
    df = pd.DataFrame(
        {
            "group1": ["A", "B", "A", "B"],
            "group2": ["X", "X", "Y", "Y"],
            "measurement1": [1, 2, 3, 4],
            "measurement2": [5, 6, 7, 8],
            "experiment": [
                "Test Experiment 1",
                "Test Experiment 1",
                "Test Experiment 2",
                "Test Experiment 2",
            ],
        }
    )
    result = Result(
        name="Test Result",
        experiment=["Test Experiment 1", "Test Experiment 2"],
        groupby=["group1", "group2"],
        measurements=["measurement1", "measurement2"],
        data=df,
    )
    assert result.name == "Test Result"
    assert result._experiment == ["Test Experiment 1", "Test Experiment 2"]
    assert result.groupby == ["group1", "group2", "experiment"]
    assert result.measurements == ["measurement1", "measurement2"]
    assert "experiment" in result.data.columns
    assert result.data["experiment"].equals(
        pd.Series(
            [
                "Test Experiment 1",
                "Test Experiment 1",
                "Test Experiment 2",
                "Test Experiment 2",
            ]
        )
    )


# def test_annotation_table_len(concrete_annotation_table):
#     assert (
#         len(concrete_annotation_table) == 3
#     ), "Length of AnnotationTable is not correct"


# def test_detection_table_len(concrete_detection_table):
#     assert len(concrete_detection_table) == 3, "Length of DetectionTable is not correct"


def test_result_add(result_data):
    # Create another Result object to add to the existing one
    df2 = pd.DataFrame(
        {
            "group1": ["C", "D", "C", "D"],
            "group2": ["Z", "Z", "W", "W"],
            "measurement1": [9, 10, 11, 12],
            "measurement2": [13, 14, 15, 16],
        }
    )
    result_data2 = Result(
        name="Test Result 2",
        experiment="Test Experiment 2",
        groupby=["group1", "group2"],
        measurements=["measurement1", "measurement2"],
        data=df2,
    )

    # Add the two Result objects
    merged_result = result_data + result_data2

    # Check if the merged Result object has the correct properties
    assert merged_result.name == f"{result_data.name} + {result_data2.name}"
    assert merged_result._experiment == ["Test Experiment", "Test Experiment 2"]
    assert merged_result.groupby == ["group1", "group2", "experiment"]
    assert merged_result.measurements == ["measurement1", "measurement2"]
    assert "experiment" in merged_result.data.columns
    assert len(merged_result.data) == len(result_data.data) + len(result_data2.data)

    # Check if a TypeError is raised when the `other` argument is not a Result object or a list of Result objects
    with pytest.raises(TypeError):
        result_data + "not a Result object"


def test_result_len(result_data):
    assert len(result_data) == 4, "Length of Result is not correct"


def test_result_experiment_single(result_data):
    result_data._experiment = ["Test Experiment"]
    assert (
        result_data.experiment == "Test Experiment"
    ), "Experiment property does not return correct value for single experiment"


def test_result_experiment_multiple(result_data):
    result_data._experiment = ["Test Experiment 1", "Test Experiment 2"]
    assert result_data.experiment == [
        "Test Experiment 1",
        "Test Experiment 2",
    ], "Experiment property does not return correct value for multiple experiments"


def test_result_experiment_setter_single_to_single(result_data):
    result_data.experiment = "New Experiment"
    assert result_data._experiment == [
        "New Experiment"
    ], "Experiment setter does not correctly set single experiment"


def test_result_experiment_setter_single_to_multiple(result_data):
    result_data.experiment = ["New Experiment 1", "New Experiment 2"]
    assert result_data._experiment == [
        "New Experiment 1",
        "New Experiment 2",
    ], "Experiment setter does not correctly set multiple experiments"


def test_result_experiment_setter_multiple_to_single(result_data):
    result_data._experiment = ["Test Experiment 1", "Test Experiment 2"]
    with pytest.raises(ValueError):
        result_data.experiment = "New Experiment"


def test_result_type(result_data):
    # Check if the `type` property returns the correct `_type` attribute
    assert result_data.type == result_data._type

def test_result_type_setter(result_data):
    result_data.type = ResultType.PERCENTAGE
    assert result_data._type == ResultType.PERCENTAGE


def test_result_head_default(result_data):
    head = result_data.head()
    assert (
        len(head) == 5 - 1
    ), "Head does not return correct number of rows for default n"
    assert head.equals(
        result_data.data.head()
    ), "Head does not return correct rows for default n"


def test_result_head_custom(result_data):
    head = result_data.head(3)
    assert len(head) == 3, "Head does not return correct number of rows for custom n"
    assert head.equals(
        result_data.data.head(3)
    ), "Head does not return correct rows for custom n"


def test_result_tail_default(result_data):
    tail = result_data.tail()
    assert (
        len(tail) == 5 - 1
    ), "Tail does not return correct number of rows for default n"
    assert tail.equals(
        result_data.data.tail()
    ), "Tail does not return correct rows for default n"


def test_result_tail_custom(result_data):
    tail = result_data.tail(3)
    assert len(tail) == 3, "Tail does not return correct number of rows for custom n"
    assert tail.equals(
        result_data.data.tail(3)
    ), "Tail does not return correct rows for custom n"


def test_result_save_excel(result_data, tmp_path):
    file_path = tmp_path / "result.xlsx"
    result_data.to_excel(file_path)
    assert file_path.exists()


def test_result_save_csv(result_data, tmp_path):
    file_path = tmp_path / "result.csv"
    result_data.to_csv(file_path)
    assert file_path.exists()


def test_result_to_graphpad(result_data, tmp_path):
    file_path = tmp_path / "result.xlsx"
    result_data.to_graphpad(file_path, "group1", "measurement1")
    assert file_path.exists()


def test_result_to_graphpad_raises_for_invalid_grouping(result_data, tmp_path):
    file_path = tmp_path / "result.xlsx"
    with pytest.raises(ValueError):
        result_data.to_graphpad(file_path, "invalid_group", "measurement1")


def test_result_to_graphpad_raises_for_invalid_measurement(result_data, tmp_path):
    file_path = tmp_path / "result.xlsx"
    with pytest.raises(ValueError):
        result_data.to_graphpad(file_path, "group1", "invalid_measurement")


def test_result_validate_matching_lists(result_data):
    # Test with matching lists
    matching_lists = [[1, 2, 3], [1, 3, 2], [3, 2, 1]]
    assert result_data._validate_matching_lists(matching_lists) is None

    # Test with non-matching lists
    non_matching_lists = [[1, 2, 3], [1, 2, 4], [1, 2, 5]]
    with pytest.raises(ValueError):
        result_data._validate_matching_lists(non_matching_lists)


def test_result_merge_results(result_data):
    # Create another Result object to merge with the existing one
    df = pd.DataFrame(
        {
            "group1": ["C", "D", "C", "D"],
            "group2": ["Z", "Z", "W", "W"],
            "measurement1": [5, 6, 7, 8],
            "measurement2": [9, 10, 11, 12],
        }
    )
    other_result = Result(
        name="Other Result",
        experiment="Other Experiment",
        groupby=["group1", "group2"],
        measurements=["measurement1", "measurement2"],
        data=df,
    )

    # Merge the two Result objects
    merged_result = result_data._merge_results(other_result)

    # Check the properties of the merged Result object
    assert merged_result.name == "Test Result + Other Result"
    assert merged_result._experiment == ["Test Experiment", "Other Experiment"]
    assert merged_result.groupby == ["group1", "group2", "experiment"]
    assert merged_result.measurements == ["measurement1", "measurement2"]
    assert len(merged_result.data) == len(result_data.data) + len(other_result.data)


def test_result_add_multiple_experiments(result_data):
    # Create another Result object with multiple experiments to add to the existing one
    df2 = pd.DataFrame(
        {
            "group1": ["C", "D", "C", "D"],
            "group2": ["Z", "Z", "W", "W"],
            "measurement1": [9, 10, 11, 12],
            "measurement2": [13, 14, 15, 16],
        }
    )
    result_data2 = Result(
        name="Test Result 2",
        experiment=["Test Experiment 2", "Test Experiment 3"],
        groupby=["group1", "group2"],
        measurements=["measurement1", "measurement2"],
        data=df2,
    )

    # Add the two Result objects
    merged_result = result_data + result_data2

    # Check if the merged Result object has the correct properties
    assert merged_result.name == "Test Result + Test Result 2"
    assert merged_result._experiment == [
        "Test Experiment",
        "Test Experiment 2",
        "Test Experiment 3",
    ]
    assert merged_result.groupby == ["group1", "group2", "experiment"]
    assert merged_result.measurements == ["measurement1", "measurement2"]
    assert "experiment" in merged_result.data.columns
    assert len(merged_result.data) == len(result_data.data) + len(result_data2.data)

    # Check if a TypeError is raised when the `other` argument is not a Result object or a list of Result objects
    with pytest.raises(TypeError):
        result_data + "not a Result object"


@pytest.fixture
def marker_selection():
    return MarkerSelection(
        name="TestSelection",
        positive_selection=["Marker1", "Marker2"],
        negative_selection=["Marker3"],
    )


def test_marker_selection_init(marker_selection):
    assert marker_selection.name == "TestSelection"
    assert marker_selection.positive_selection == ["Marker1", "Marker2"]
    assert marker_selection.negative_selection == ["Marker3"]


def test_marker_selection_post_init_string_input():
    marker_selection = MarkerSelection(
        name="TestSelection", positive_selection="Marker1", negative_selection="Marker2"
    )
    assert marker_selection.positive_selection == ["Marker1"]
    assert marker_selection.negative_selection == ["Marker2"]


@pytest.fixture
def hcr_experiment():
    # Assuming HCRexperiment has an attribute channel_names
    class HCRexperiment:
        channel_names = ["Marker1", "Marker2", "Marker3", "Marker4"]

    return HCRexperiment()


def test_marker_selection_validate(marker_selection, hcr_experiment):
    assert marker_selection.validate(hcr_experiment) is True


def test_marker_selection_validate_invalid_marker(marker_selection, hcr_experiment):
    marker_selection.positive_selection.append("InvalidMarker")
    assert marker_selection.validate(hcr_experiment) is False


def test_result_serialize(result_data):
    json_data, csv_data = result_data.serialize()
    expected_json_data = {
        "name": "Test Result",
        "experiment": "Test Experiment",
        "groupby": ["group1", "group2", "experiment"],
        "measurements": ["measurement1", "measurement2"],
    }
    expected_csv_data = result_data.data.to_csv()

    assert json.loads(json_data) == expected_json_data
    assert csv_data == expected_csv_data


def test_result_deserialize(result_data):
    json_data = json.dumps(
        {
            "name": "Test Result",
            "experiment": ["Test Experiment"],
            "groupby": ["group1", "group2"],
            "measurements": ["measurement1", "measurement2"],
        }
    )
    df = pd.DataFrame(
        {
            "group1": ["A", "B", "A", "B"],
            "group2": ["X", "X", "Y", "Y"],
            "measurement1": [1, 2, 3, 4],
            "measurement2": [5, 6, 7, 8],
            "experiment": [
                "Test Experiment",
                "Test Experiment",
                "Test Experiment",
                "Test Experiment",
            ],
        }
    )
    result = Result.deserialize(json_data, df)
    assert result.name == "Test Result"
    assert result._experiment == ["Test Experiment"]
    assert result.groupby == ["group1", "group2", "experiment"]
    assert result.measurements == ["measurement1", "measurement2"]
    assert result.data.equals(df)
