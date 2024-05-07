"""
Module for testing the feature extraction functions in the preprocess.feature_extraction module.
"""
# pylint: disable=redefined-outer-name
# pylint: disable=line-too-long

from pathlib import Path
import copy
import pytest
import pandas as pd
import cell_typist as ct
from cell_typist.preprocess.feature_extraction import (
    parse_file_names,
    define_channel_names,
    split_columns,
    merge_columns,
    replace_in_column,
)


@pytest.fixture
def experiment():
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


def test_parse_file_names_type_error():
    """
    Test case to check if a TypeError is raised when the input is not an HCRexperiment object.
    """
    with pytest.raises(TypeError):
        parse_file_names("not an HCRexperiment", "template")


def test_parse_file_names_value_error(experiment):
    """
    Test case to check if a ValueError is raised when the template contains an invalid separator.
    """
    with pytest.raises(ValueError):
        parse_file_names(experiment, "template", separator=".")


def test_parse_file_names_parsing(experiment):
    """
    Test case to check if the file names are parsed correctly and the corresponding columns are added to the experiment.
    """
    experiment = parse_file_names(experiment, "condition_age_timepoint")
    assert "condition" in experiment.detections.columns
    assert "age" in experiment.detections.columns
    assert "timepoint" in experiment.detections.columns


def test_parse_file_names_annotation(experiment):
    """
    Test case to check if the 'annotation' column is added to the experiment after parsing the file names.
    """
    experiment = parse_file_names(experiment, "condition_age_timepoint")
    assert "annotation" in experiment.detections.columns


def test_parse_file_names_parsing_inplace(experiment):
    """
    Test case to check if the file names are parsed correctly and the corresponding columns are added to the experiment when inplace=True.
    """
    parse_file_names(experiment, "condition_age_timepoint", inplace=True)
    assert "condition" in experiment.detections.columns
    assert "age" in experiment.detections.columns
    assert "timepoint" in experiment.detections.columns


def test_parse_file_names_not_inplace(experiment):
    """
    Test case to check if the file names are parsed correctly and the corresponding columns added only to the returned experiment when inplace=False.
    """
    returned_experiment = parse_file_names(experiment, "condition_age_timepoint")
    assert "condition" in returned_experiment.detections.columns
    assert "age" in returned_experiment.detections.columns
    assert "timepoint" in returned_experiment.detections.columns
    assert "condition" not in experiment.detections.columns
    assert "age" not in experiment.detections.columns
    assert "timepoint" not in experiment.detections.columns


def test_parse_file_names_parsing_empty_template(experiment):
    """
    Test case to check if a ValueError is raised when an empty template is provided for parsing file names.
    """
    with pytest.raises(ValueError):
        parse_file_names(experiment, "")


def test_hcrexperiment_add_annotation_column_wrong_values_length(experiment):
    """
    Test case to check if a ValueError is raised when the length of the values list is not equal to the number of rows in the experiment.
    """
    with pytest.raises(ValueError):
        experiment.add_annotation_column("new_column", [1, 2])


def test_define_channel_names_type_error():
    """
    Test case to check if a TypeError is raised when the input is not an HCRexperiment object.
    """
    with pytest.raises(TypeError):
        define_channel_names("not an HCRexperiment", "template")


def test_define_channel_names_value_error_no_separator(experiment):
    """
    Test case to check if a ValueError is raised when the template contains no separator.
    """
    with pytest.raises(ValueError):
        define_channel_names(experiment, "template", separator=".")


def test_define_channel_names_value_error_mismatched_channels(experiment):
    """
    Test case to check if a ValueError is raised when the number of channels in the template does not match the number of channels in the experiment.
    """
    with pytest.raises(ValueError):
        define_channel_names(experiment, "condition-age-timepoint", separator="-")


def test_define_channel_names_successful_run(experiment):
    """
    Test case to check if the channel names are defined correctly and added to the experiment.
    """
    experiment = define_channel_names(
        experiment, "condition-age", separator="-", verbose=True
    )
    assert "condition" in experiment.detections.columns
    assert "age" in experiment.detections.columns


def test_define_channel_names_successful_run_inplace_true(experiment):
    """
    Test case to check if the channel names are defined correctly and added to the experiment when inplace=True.
    """
    define_channel_names(
        experiment, "condition-age", separator="-", verbose=True, inplace=True
    )
    assert "condition" in experiment.detections.columns
    assert "age" in experiment.detections.columns


def test_define_channel_names_successful_run_inplace_false(experiment):
    """
    Test case to check if the channel names are defined correctly and added to the experiment when inplace=False.
    """
    returned_experiment = define_channel_names(
        experiment, "condition-age", separator="-", verbose=True
    )
    assert "condition" in returned_experiment.detections.columns
    assert "age" in returned_experiment.detections.columns
    assert "condition" not in experiment.detections.columns
    assert "age" not in experiment.detections.columns


def test_split_columns_type_error():
    """
    Test case to check if a TypeError is raised when the input is not an HCRexperiment object.
    """
    with pytest.raises(TypeError):
        split_columns("not an HCRexperiment", "column_name")


def test_split_columns_value_error_no_column(experiment):
    """
    Test case to check if a ValueError is raised when the specified column does not exist in the experiment.
    """
    with pytest.raises(ValueError):
        split_columns(experiment, "non_existent_column")


def test_split_columns_value_error_mismatched_template(experiment):
    """
    Test case to check if a ValueError is raised when the template does not match the specified column.
    """
    with pytest.raises(ValueError):
        split_columns(
            experiment,
            "condition-age-timepoint",
            template="condition-age",
            separator="-",
        )


def test_split_columns_value_error_columns_not_present(experiment):
    """
    Test case to check if a ValueError is raised when the columns specified in the template are not present in the experiment.
    """
    with pytest.raises(ValueError):
        split_columns(
            experiment,
            "condition-age-timepoint",
            template="condition-age-timepoint",
            separator="-",
        )


def test_split_columns_successful_run_no_template(experiment):
    """
    Test case to check if columns are split successfully when no template is provided.
    """
    experiment.metadata = []
    num_columns = len(experiment.detections.columns)
    experiment = split_columns(experiment, "Image", separator=".", verbose=True)
    assert len(experiment.detections.columns) > num_columns


def test_split_columns_with_template_mismatch(experiment):
    """
    Test case to check if a ValueError is raised when the template does not match the specified column.
    """
    with pytest.raises(ValueError):
        experiment = split_columns(
            experiment,
            "Image",
            template="a.b.c",
            separator=".",
            verbose=True,
        )


def test_split_columns_successful_run_with_template(experiment):
    """
    Test case to check if columns are split successfully using a template.
    """
    experiment.metadata = []
    num_columns = len(experiment.detections.columns)
    experiment = split_columns(
        experiment,
        "Image",
        template="condition.age",
        separator=".",
        verbose=True,
    )
    assert "condition" in experiment.detections.columns
    assert "age" in experiment.detections.columns
    assert "condition" in experiment.metadata
    assert "age" in experiment.metadata 


def test_split_columns_successful_with_inplace_true(experiment):
    """
    Test case to check if columns are split successfully when inplace=True.
    """
    experiment.metadata = []
    num_columns = len(experiment.detections.columns)
    split_columns(
        experiment,
        "Image",
        template="condition.age",
        separator=".",
        verbose=True,
        inplace=True,
    )
    assert "condition" in experiment.detections.columns
    assert "age" in experiment.detections.columns
    assert len(experiment.detections.columns) > num_columns


def test_split_columns_successful_with_inplace_false(experiment):
    """
    Test case to check if columns are split successfully when inplace=False.
    """
    experiment.metadata = []
    num_columns = len(experiment.detections.columns)
    returned_experiment = split_columns(
        experiment,
        "Image",
        template="condition.age",
        separator=".",
        verbose=True,
    )
    assert "condition" in returned_experiment.detections.columns
    assert "age" in returned_experiment.detections.columns
    assert len(returned_experiment.detections.columns) > num_columns
    assert "condition" not in experiment.detections.columns
    assert "age" not in experiment.detections.columns


def test_merge_columns_type_error():
    """
    Test case to check if a TypeError is raised when the input is not an HCRexperiment object.
    """
    with pytest.raises(TypeError):
        merge_columns("not an HCRexperiment", ["column1", "column2"], "new_column")


def test_merge_columns_value_error_missing_column(experiment):
    """
    Test case to check if a ValueError is raised when one of the specified columns is not present in the experiment.
    """
    with pytest.raises(ValueError):
        merge_columns(experiment, ["non_existent_column", "column2"], "new_column")


def test_merge_columns_successful_merge(experiment):
    """
    Test case to check if the specified columns are merged successfully into a new column.
    """
    experiment = merge_columns(
        experiment, ["Image", "Parent"], "Image-Parent", verbose=True
    )
    assert "Image-Parent" in experiment.detections.columns
    assert "Image-Parent" in experiment.annotations.columns


def test_merge_columns_successful_merge_inplace_true(experiment):
    """
    Test case to check if the specified columns are merged successfully into a new column when inplace=True.
    """
    merge_columns(
        experiment, ["Image", "Parent"], "Image-Parent", verbose=True, inplace=True
    )
    assert "Image-Parent" in experiment.detections.columns
    assert "Image-Parent" in experiment.annotations.columns


def test_merge_columns_successful_merge_inplace_false(experiment):
    """
    Test case to check if the specified columns are merged successfully into a new column when inplace=False.
    """
    returned_experiment = merge_columns(
        experiment, ["Image", "Parent"], "Image-Parent", verbose=True
    )
    assert "Image-Parent" in returned_experiment.detections.columns
    assert "Image-Parent" in returned_experiment.annotations.columns
    assert "Image-Parent" not in experiment.detections.columns
    assert "Image-Parent" not in experiment.annotations.columns


def test_merge_columns_successful_merge_check_values(experiment):
    """
    Test case to check if the values in the new column are correct after merging.
    """
    experiment = merge_columns(
        experiment, ["Image", "Parent"], "Image-Parent", verbose=True
    )
    for _, row in experiment.detections.dataframe.iterrows():
        assert row["Image-Parent"] == f"{row['Image']}-{row['Parent']}"
    for _, row in experiment.annotations.dataframe.iterrows():
        assert row["Image-Parent"] == f"{row['Image']}-{row['Parent']}"


def test_merge_columns_keep_old_false(experiment):
    """
    Test case to check if the original columns are dropped when keep_old is set to False.
    """
    experiment = merge_columns(
        experiment, ["Image", "Parent"], "Image-Parent", keep_old=False, verbose=True
    )
    assert "Image-Parent" in experiment.detections.columns
    assert "Image-Parent" in experiment.annotations.columns
    assert "Image" not in experiment.detections.columns
    assert "Parent" not in experiment.detections.columns
    assert "Image" not in experiment.annotations.columns
    assert "Parent" not in experiment.annotations.columns


def test_replace_in_column_type_error():
    """
    Test case to check if a TypeError is raised when the experiment object is not of type HCRexperiment.
    """
    with pytest.raises(TypeError):
        replace_in_column(
            "not an HCRexperiment", "column_name", "old_value", "new_value"
        )


def test_replace_in_column_value_error(experiment):
    """
    Test case to check if a ValueError is raised when the specified column is not present in the dataframe.
    """
    with pytest.raises(ValueError):
        replace_in_column(experiment, "non_existent_column", "old_value", "new_value")


def test_replace_in_column_successful_run(experiment):
    """
    Test case to check if the function correctly replaces the old value with the new value in the specified column of the experiment dataframe.
    """
    experiment.detections.add_series(
        "test_column",
        pd.Series("other_value", index=experiment.detections.dataframe.index),
    )
    experiment.detections.dataframe["test_column"].iloc[0] = "old_value"

    experiment.annotations.add_series(
        "test_column",
        pd.Series("other_value", index=experiment.annotations.dataframe.index),
    )
    experiment.annotations.dataframe["test_column"].iloc[0] = "old_value"

    experiment = replace_in_column(experiment, "test_column", "old_value", "new_value")
    assert experiment.detections.dataframe["test_column"].iloc[0] == "new_value"
    assert experiment.annotations.dataframe["test_column"].iloc[0] == "new_value"
    assert experiment.detections.dataframe["test_column"].unique().size == 2
    assert experiment.annotations.dataframe["test_column"].unique().size == 2


def test_replace_in_column_inplace_true(experiment):
    """
    Test case to check if the function correctly replaces the old value with the new value in the specified column of the experiment dataframe when inplace=True.
    """
    experiment.detections.add_series(
        "test_column",
        pd.Series("other_value", index=experiment.detections.dataframe.index),
    )
    experiment.detections.dataframe["test_column"].iloc[0] = "old_value"

    experiment.annotations.add_series(
        "test_column",
        pd.Series("other_value", index=experiment.annotations.dataframe.index),
    )
    experiment.annotations.dataframe["test_column"].iloc[0] = "old_value"

    replace_in_column(experiment, "test_column", "old_value", "new_value", inplace=True)
    assert experiment.detections.dataframe["test_column"].iloc[0] == "new_value"
    assert experiment.annotations.dataframe["test_column"].iloc[0] == "new_value"
    assert experiment.detections.dataframe["test_column"].unique().size == 2
    assert experiment.annotations.dataframe["test_column"].unique().size == 2
