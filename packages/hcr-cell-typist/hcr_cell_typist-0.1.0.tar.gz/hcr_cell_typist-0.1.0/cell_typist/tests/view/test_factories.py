import pytest
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from cell_typist.view.factories import (
    Grid,
    PlotGrid,
    SINGLE_RES_PLOT_FIGSIZE,
)


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


def test_grid_initialization():
    """
    Test the initialization of the Grid class.
    """
    grid = Grid(4)
    assert grid.n_plots == 4


def test_calculate_grid():
    """
    Test the calculate_grid method of the Grid class.
    """
    grid = Grid(4)
    n_rows, n_cols = grid.calculate_grid()
    assert n_rows == 2
    assert n_cols == 2

    grid = Grid(5)
    n_rows, n_cols = grid.calculate_grid()
    assert n_rows == 2
    assert n_cols == 3


def test_call():
    """
    Test the __call__ method of the Grid class.
    """
    grid = Grid(4)
    fig, ax = grid()
    assert fig.get_size_inches()[0] == 2 * SINGLE_RES_PLOT_FIGSIZE[0]
    assert fig.get_size_inches()[1] == 2 * SINGLE_RES_PLOT_FIGSIZE[1]
    assert len(ax.flat) == 4
    assert all(a.get_visible() for a in ax.flat)

    grid = Grid(5)
    fig, ax = grid()
    assert fig.get_size_inches()[0] == 3 * SINGLE_RES_PLOT_FIGSIZE[0]
    assert fig.get_size_inches()[1] == 2 * SINGLE_RES_PLOT_FIGSIZE[1]
    assert len(ax.flat) == 6
    assert all(a.get_visible() for a in ax.flat[:-1])
    assert not ax.flat[-1].get_visible()


def test_plotgrid_initialization():
    """
    Test the initialization of the PlotGrid class.
    """
    plot_grid = PlotGrid(2, 2)
    assert plot_grid.n_rows == 2
    assert plot_grid.n_cols == 2
    assert plot_grid.figsize == SINGLE_RES_PLOT_FIGSIZE
    assert plot_grid.kwargs == {}


def test_plotgrid_post_init():
    """
    Test the __post_init__ method of the PlotGrid class.
    """
    plot_grid = PlotGrid(2, 2, (10, 10), {"sharex": True, "sharey": True})
    assert plot_grid.fig.get_size_inches()[0] == 10
    assert plot_grid.fig.get_size_inches()[1] == 10
    assert len(plot_grid.ax.flat) == 4
    assert all(a.get_visible() for a in plot_grid.ax.flat)
    assert all(a.get_shared_x_axes().get_siblings(a) for a in plot_grid.ax.flat)
    assert all(a.get_shared_y_axes().get_siblings(a) for a in plot_grid.ax.flat)