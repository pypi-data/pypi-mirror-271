""" Test the measure module."""
# pylint: disable=redefined-outer-name
# pylint: disable=line-too-long

from pathlib import Path
import pytest
import cell_typist as ct
from cell_typist.core.experiment import HCRexperiment
from cell_typist.core.datatypes import MarkerSelection, Result
from cell_typist.preprocess.feature_extraction import (
    parse_file_names,
    define_channel_names,
)
from cell_typist.measure.measure import (
    threshold_expression,
    threshold_expression_interactive,
    calculate_percentages,
    calculate_densities,
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
    experiment = parse_file_names(
        experiment,
        template="strain_age_tissue_experiment_staining_magnification_timepoint_fish",
        separator="_",
    )
    experiment = define_channel_names(
        experiment, template="Ollineage-cldnk", separator="-"
    )
    return experiment


@pytest.fixture
def thresholded_experiment(experiment):
    """
    Fixture that returns an instance of the experiment with thresholds for testing.
    """
    thresholds = {"cldnk": 5, "Ollineage": 3}
    return threshold_expression(experiment, thresholds)


@pytest.fixture
def thresholds():
    """
    Fixture that returns a dictionary of thresholds for testing.
    """
    return {"cldnk": 5, "Ollineage": 3}


@pytest.fixture
def custom_selections():
    """
    Fixture that returns a list of MarkerSelection objects for testing.
    """
    return [MarkerSelection("selection1", ["Ollineage"], ["cldnk"])]


def test_threshold_expression_with_valid_inputs(
    experiment, thresholds, custom_selections
):
    """
    Test the threshold_expression function with valid inputs.
    """
    result = threshold_expression(experiment, thresholds, custom_selections)
    assert isinstance(result, HCRexperiment)
    assert len(result.detections.dataframe.columns) == len(
        experiment.detections.dataframe.columns
    ) + len(thresholds) + len(custom_selections)


def test_threshold_expression_with_inplace_true(
    experiment, thresholds, custom_selections
):
    """
    Test the threshold_expression function with inplace set to True.
    """
    threshold_expression(experiment, thresholds, custom_selections, inplace=True)
    assert all(ch for ch in thresholds if f"{ch}_pos" in experiment.data)


def test_threshold_expression_with_inplace_false(
    experiment, thresholds, custom_selections
):
    """
    Test the threshold_expression function with inplace set to False.
    """
    result = threshold_expression(
        experiment, thresholds, custom_selections, inplace=False
    )
    assert all(ch for ch in thresholds if f"{ch}_pos" not in experiment.data)
    assert all(ch for ch in thresholds if f"{ch}_pos" in result.data)


def test_threshold_expression_with_invalid_thresholds(experiment, custom_selections):
    """
    Test the threshold_expression function with invalid thresholds.
    """
    invalid_thresholds = {"invalid": 5}
    with pytest.raises(ValueError):
        threshold_expression(experiment, invalid_thresholds, custom_selections)


def test_threshold_expression_with_no_custom_selections(experiment, thresholds):
    """
    Test the threshold_expression function with no custom selections.
    """
    result = threshold_expression(experiment, thresholds)
    assert isinstance(result, HCRexperiment)
    assert len(result.detections.dataframe.columns) == len(
        experiment.detections.dataframe.columns
    ) + len(thresholds)


def test_threshold_expression_with_list_thresholds(experiment, custom_selections):
    """
    Test the threshold_expression function with list thresholds.
    """
    list_thresholds = [5, 3]
    result = threshold_expression(experiment, list_thresholds, custom_selections)
    assert isinstance(result, HCRexperiment)
    assert len(result.detections.dataframe.columns) == len(
        experiment.detections.dataframe.columns
    ) + len(list_thresholds) + len(custom_selections)


def test_threshold_expression_with_mismatched_thresholds_and_channels(
    experiment, custom_selections
):
    """
    Test the threshold_expression function with mismatched thresholds and channels.
    """
    mismatched_thresholds = {"channel1": 5, "channel2": 3, "channel3": 2}
    with pytest.raises(ValueError):
        threshold_expression(experiment, mismatched_thresholds, custom_selections)


def test_threshold_expression_with_negative_selection(experiment, thresholds):
    """
    Test the threshold_expression function with negative selection.
    """
    negative_selections = [MarkerSelection("selection1", [], ["Ollineage"])]
    result = threshold_expression(experiment, thresholds, negative_selections)
    assert isinstance(result, HCRexperiment)
    assert len(result.detections.dataframe.columns) == len(
        experiment.detections.dataframe.columns
    ) + len(thresholds) + len(negative_selections)
    assert all(ch for ch in thresholds if f"{ch}_pos" in result.data)
    assert "selection1_pos" in result.data


def test_threshold_expression_interactive_with_valid_inputs(
    monkeypatch, experiment, custom_selections
):
    """
    Test the threshold_expression_interactive function with valid inputs.
    """
    # Simulate user input for the thresholds
    monkeypatch.setattr("builtins.input", lambda _: "5")
    result = threshold_expression_interactive(experiment, custom_selections)
    assert isinstance(result, HCRexperiment)
    assert len(result.detections.dataframe.columns) == len(
        experiment.detections.dataframe.columns
    ) + len(experiment.channel_names) + len(custom_selections)


def test_threshold_expression_interactive_with_no_custom_selections(
    monkeypatch, experiment
):
    """
    Test the threshold_expression_interactive function with no custom selections.
    """
    # Simulate user input for the thresholds
    monkeypatch.setattr("builtins.input", lambda _: "5")
    result = threshold_expression_interactive(experiment)
    assert isinstance(result, HCRexperiment)
    assert len(result.detections.dataframe.columns) == len(
        experiment.detections.dataframe.columns
    ) + len(experiment.channel_names)


def test_threshold_expression_interactive_with_invalid_input(
    monkeypatch, experiment, custom_selections
):
    """
    Test the threshold_expression_interactive function with invalid input.
    """
    # Simulate user input for the thresholds
    monkeypatch.setattr("builtins.input", lambda _: "invalid")
    with pytest.raises(ValueError):
        threshold_expression_interactive(experiment, custom_selections)


def test_calculate_percentages_with_valid_inputs(thresholded_experiment):
    """
    Test the calculate_percentages function with valid inputs.
    """
    groupby = ["age", "fish"]
    result = calculate_percentages(thresholded_experiment, groupby)
    assert isinstance(result, Result)
    assert result.experiment == thresholded_experiment.name
    assert result.groupby == groupby
    assert all(col in result.data.columns for col in groupby)
    assert all(
        col.replace("_pos", "") in result.measurements
        for col in thresholded_experiment.data
        if "_pos" in col
    )


def test_calculate_percentages_with_missing_columns(thresholded_experiment):
    """
    Test the calculate_percentages function with missing columns in the dataframe.
    """
    groupby = ["MissingColumn"]
    with pytest.raises(ValueError):
        calculate_percentages(thresholded_experiment, groupby)


def test_calculate_percentages_with_no_thresholds(experiment):
    """
    Test the calculate_percentages function with no thresholds.
    """
    groupby = ["age", "fish"]
    with pytest.raises(ValueError):
        calculate_percentages(experiment, groupby)


def test_calculate_densities_with_valid_inputs(thresholded_experiment):
    """
    Test the calculate_densities function with valid inputs.
    """
    groupby = ["age", "fish"]
    result = calculate_densities(thresholded_experiment, groupby)
    assert isinstance(result, Result)
    assert "density" in result.name
    assert thresholded_experiment.name in result.experiment
    assert groupby == result.groupby
    assert all(col in result.data.columns for col in groupby)
    assert "area" in result.data.columns
    assert all("_density" in col for col in result.measurements)


def test_calculate_densities_with_missing_columns(thresholded_experiment):
    """
    Test the calculate_densities function with missing columns.
    """
    groupby = ["NonexistentColumn"]
    with pytest.raises(ValueError):
        calculate_densities(thresholded_experiment, groupby)


def test_calculate_densities_with_no_thresholds(experiment):
    """
    Test the calculate_densities function with no thresholds.
    """
    groupby = ["age", "fish"]
    with pytest.raises(ValueError):
        calculate_densities(experiment, groupby)


def test_calculate_densities_with_single_column(thresholded_experiment):
    """
    Test the calculate_densities function with a single column.
    """
    groupby = "age"
    result = calculate_densities(thresholded_experiment, groupby)
    assert isinstance(result, Result)
    assert "density" in result.name
    assert thresholded_experiment.name in result.experiment
    assert [groupby] + ["experiment"] == result.groupby
    assert groupby in result.data.columns
    assert "area" in result.data.columns
    assert all("_density" in col for col in result.measurements)
