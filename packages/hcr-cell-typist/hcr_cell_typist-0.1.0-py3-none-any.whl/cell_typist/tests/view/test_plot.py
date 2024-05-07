""" Unit tests for the cell_typist.view.plot module. """
# pylint: disable=protected-access
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring

from cell_typist.view.plot import plot_expression, plot_results
from cell_typist.core.datatypes import ResultType
from matplotlib import pyplot as plt
import pytest
import pandas as pd
import numpy as np


# Define a fixture for the mock HCRexperiment
@pytest.fixture
def mock_experiment():
    class MockHCRexperiment:
        are_channels_defined = True
        detections = type(
            "obj",
            (object,),
            {
                "dataframe": pd.DataFrame(
                    {
                        "gene1": np.random.rand(10),
                        "gene2": np.random.rand(10),
                        "file": ["file1", "file2"] * 5,
                    }
                )
            },
        )
    return MockHCRexperiment()

def test_plot_expression_single_gene(mock_experiment):
    """
    Test the plot_expression function with a single gene.
    """
    fig = plot_expression(mock_experiment, "gene1")
    assert isinstance(fig, plt.Figure)


def test_plot_expression_multiple_genes(mock_experiment):
    """
    Test the plot_expression function with multiple genes.
    """
    fig = plot_expression(mock_experiment, ["gene1", "gene2"])
    assert isinstance(fig, plt.Figure)


def test_plot_expression_unsupported_kind(mock_experiment):
    """
    Test the plot_expression function with unsupported kind.
    """
    with pytest.raises(ValueError):
        plot_expression(mock_experiment, "gene1", kind="unsupported")


def test_plot_expression_undefined_channels(mock_experiment):
    """
    Test the plot_expression function with undefined channels.
    """
    mock_experiment.are_channels_defined = False
    with pytest.raises(ValueError):
        plot_expression(mock_experiment, "gene1")

def test_plot_expression_automatic_threshold(mock_experiment):
    """
    Test the plot_expression function with automatic threshold.
    """
    plot_expression(mock_experiment, "gene1", automatic_treshold=True)

def test_plot_expression_with_figsize(mock_experiment):
    """
    Test the plot_expression function with figsize.
    """
    fig = plot_expression(mock_experiment, "gene1", figsize=(10, 10))
    assert isinstance(fig, plt.Figure)
    assert fig.get_size_inches()[0] == 10
    assert fig.get_size_inches()[1] == 10


@pytest.fixture
def mock_results():
    class MockResult:
        name = "Test Result"
        data = pd.DataFrame(
            {
                "x": ["group1", "group2"] * 5,
                "gene1": np.random.rand(10),
                "gene2": np.random.rand(10),
            }
        )
        type = ResultType.PERCENTAGE

    return MockResult()


def test_plot_results_single_gene(mock_results):
    """
    Test the plot_results function with a single gene.
    """
    fig = plot_results(mock_results, "x", "gene1")
    assert isinstance(fig, plt.Figure)


def test_plot_results_multiple_genes(mock_results):
    """
    Test the plot_results function with multiple genes.
    """
    fig = plot_results(mock_results, "x", ["gene1", "gene2"])
    assert isinstance(fig, plt.Figure)


def test_plot_results_with_hue(mock_results):
    """
    Test the plot_results function with hue.
    """
    mock_results.data["hue"] = ["hue1", "hue2"] * 5
    fig = plot_results(mock_results, "x", "gene1", hue="hue")
    assert isinstance(fig, plt.Figure)


def test_plot_results_with_labels(mock_results):
    """
    Test the plot_results function with x_label and y_label.
    """
    fig = plot_results(mock_results, "x", "gene1", x_label="X Label", y_label="Y Label")
    assert isinstance(fig, plt.Figure)
    assert fig.axes[0].get_xlabel() == "X Label"
    assert fig.axes[0].get_ylabel() == "Y Label"


def test_plot_results_with_ylim(mock_results):
    """
    Test the plot_results function with y_lim.
    """
    fig = plot_results(mock_results, "x", "gene1", y_lim=(0, 1))
    assert isinstance(fig, plt.Figure)
    assert fig.axes[0].get_ylim() == (0, 1)


def test_plot_results_with_fig_title_single(mock_results):
    """
    Test the plot_results function with fig_title.
    """
    fig = plot_results(mock_results, "x", "gene1", fig_title="Figure Title")
    assert isinstance(fig, plt.Figure)
    assert fig.axes[0].get_title() == "Figure Title"


def test_plot_results_with_fig_title_multi(mock_results):
    """
    Test the plot_results function with fig_title.
    """
    fig = plot_results(mock_results, "x", ["gene1", "gene2"], fig_title="Figure Title")
    assert isinstance(fig, plt.Figure)
    assert fig.get_suptitle() == "Figure Title"