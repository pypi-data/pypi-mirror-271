from typing import Any, Literal
from dataclasses import dataclass, field
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from cell_typist.core.datatypes import ResultType


PLOT_KIND_BINDINGS = {
    "hist": sns.histplot,
    "kde": sns.kdeplot,
}

SINGLE_EXP_PLOT_FIGSIZE = (10, 5)
SINGLE_RES_PLOT_FIGSIZE = (5, 5)

DEFAULT_COLOR_PALETTE = "tab10"


class FigureFactory:
    """
    Factory class for generating figures and axes objects.

    Args:
        y (str): The gene or list of genes to plot.
        result_type (Literal["densities", "percentages"]): The type of result to generate.

    Returns:
        tuple[plt.Figure, list[plt.Axes], list[str]]: A tuple containing the generated figure, list of axes objects, and list of genes.
    """

    def __init__(
            self,
            y: str,
            result_type: ResultType
    ):
        self.y = y
        self.result_type = result_type
    
    def __call__(self) -> tuple[plt.Figure, list[plt.Axes], list[str]]:
        return self._generate_figure()

    def _generate_figure(self) -> tuple[plt.Figure, list[plt.Axes], list[str]]:
        genes = [self.y] if isinstance(self.y, str) else self.y
        if self.result_type == ResultType.DENSITY:
            genes = [f"{gene}_density" for gene in genes]
        fig, ax = Grid(len(genes))()
        ax = [ax] if len(genes) == 1 else ax.flatten()
        return fig, ax, genes


class BarPlotFactory():
    """
    A factory class for generating bar plots using seaborn library.
    """

    def __init__(
            self,
            x: str,
            y: str,
            hue: str,
            data: pd.DataFrame,
            ax: plt.Axes,
            x_order: list[str] = None,
            custom_colors: dict[str, str] = None,
    ):
        """
        Initialize the BarPlotFactory.

        Parameters:
        - x (str): The column name for the x-axis.
        - y (str): The column name for the y-axis.
        - hue (str): The column name for the hue.
        - data (pd.DataFrame): The data to be plotted.
        - ax (plt.Axes): The matplotlib axes object to plot on.
        - x_order (list[str], optional): The order of the x-axis values. Defaults to None, meaning alphabetical.
        """
        self.x = x
        self.y = y
        self.hue = hue
        self.data = data
        self.ax = ax
        self.x_order = x_order
        self.custom_colors = _get_color_palette(
            data[x].unique(),
            custom_colors,
        )

    def __call__(self) -> plt.Axes:
        """
        Generate the bar plot.

        Returns:
        - plt.Axes: The matplotlib axes object containing the bar plot.
        """
        return self._generate_barplot()

    def _generate_barplot(self) -> plt.Axes:
        """
        Generate the bar plot using seaborn library.

        Returns:
        - plt.Axes: The matplotlib axes object containing the bar plot.
        """
        sns.barplot(
            x=self.x,
            y=self.y,
            hue=self.hue,
            data=self.data,
            ax=self.ax,
            order=self.x_order,
            palette=self.custom_colors,
        )

        for bar in self.ax.patches:
            r, g, b = bar.get_facecolor()[:3]
            bar.set_facecolor((r, g, b, 0.4))
            bar.set_edgecolor((r, g, b, 0.6))

        return self.ax


class LinePlotFactory:
    """
    A factory class for generating line plots using seaborn library.
    """

    def __init__(
        self,
        x: str,
        y: str,
        hue: str,
        data: pd.DataFrame,
        ax: plt.Axes,
        x_order: list[str] = None,
        custom_colors: dict[str, str] = None,
    ):
        """
        Initialize the LinePlotFactory.

        Parameters:
        - x (str): The column name for the x-axis.
        - y (str): The column name for the y-axis.
        - hue (str): The column name for the hue.
        - data (pd.DataFrame): The data to be plotted.
        - ax (plt.Axes): The matplotlib axes object to plot on.
        - x_order (list[str], optional): The order of the x-axis values. NOT IMPLEMENTED.
        """
        self.x = x
        self.y = y
        self.hue = hue
        self.data = data
        self.ax = ax
        self.x_order = x_order
        self.custom_colors = _get_color_palette(
            data[x].unique(),
            custom_colors,
        )

    def __call__(self) -> plt.Axes:
        """
        Generate the line plot.

        Returns:
        - plt.Axes: The matplotlib axes object containing the line plot.
        """
        return self._generate_lineplot()

    def _generate_lineplot(self) -> plt.Axes:
        """
        Generate the line plot using seaborn library.

        Returns:
        - plt.Axes: The matplotlib axes object containing the line plot.
        """
        sns.lineplot(
            x=self.x,
            y=self.y,
            hue=self.hue,
            data=self.data,
            ax=self.ax,
            palette=self.custom_colors,
        )

        return self.ax


class StripPlotFactory:
    """
    A factory class for generating strip plots using Seaborn.
    """

    def __init__(
        self,
        x: str,
        y: str,
        hue: str,
        data: pd.DataFrame,
        ax: plt.Axes,
        x_order: list[str] = None,
        custom_colors: dict[str, str] = None,
    ):
        """
        Initialize the StripPlotFactory.

        Parameters:
        - x (str): The column name for the x-axis.
        - y (str): The column name for the y-axis.
        - hue (str): The column name for the hue.
        - data (pd.DataFrame): The data to be plotted.
        - ax (plt.Axes): The matplotlib axes object to plot on.
        - x_order (list[str], optional): The order of the x-axis values. Defaults to None, meaning alphabetical.
        """
        self.x = x
        self.y = y
        self.hue = hue
        self.data = data
        self.ax = ax
        self.x_order = x_order
        self.custom_colors = _get_color_palette(
            data[x].unique(),
            custom_colors,
        )

    def __call__(self) -> plt.Axes:
        """
        Generate and return a strip plot using the specified parameters.

        Returns:
            plt.Axes: The generated strip plot axes.
        """
        return self._generate_stripplot()

    def _generate_stripplot(self) -> plt.Axes:
        """
        Generate a strip plot using the specified parameters.

        Returns:
            plt.Axes: The generated strip plot axes.
        """
        sns.stripplot(
            x=self.x,
            y=self.y,
            hue=self.hue,
            data=self.data,
            ax=self.ax,
            alpha=0.65,
            order=self.x_order,
            palette=self.custom_colors,
        )
        return self.ax


class Grid:
    """
    Class for calculating the grid for a plot.

    Attributes:
        n_plots (int): The number of plots to be displayed.

    Methods:
        calculate_grid(): Calculates the number of rows and columns for the grid.
    """

    def __init__(
        self,
        n_plots: int,
    ):
        self.n_plots = n_plots

    def calculate_grid(
        self,
    ) -> tuple[int, int]:
        """
        Calculates the number of rows and columns for the grid based on the number of plots.

        Returns:
            tuple[int, int]: A tuple containing the number of rows and columns for the grid.
        """
        n_rows = int(np.sqrt(self.n_plots))
        n_cols = int(np.ceil(self.n_plots / n_rows))
        return n_rows, n_cols

    def __call__(
        self,
    ) -> tuple[int, int]:
        """
        Calls the Grid instance and returns the figure and axes for the plot grid.

        Returns:
            tuple[Figure, ndarray]: A tuple containing the figure and axes for the plot grid.
        """
        n_rows, n_cols = self.calculate_grid()
        figsize = (
            n_cols * SINGLE_RES_PLOT_FIGSIZE[0],
            n_rows * SINGLE_RES_PLOT_FIGSIZE[1],
        )
        plot_grid = PlotGrid(n_rows, n_cols, figsize=figsize)
        if (n_rows > 1) and (self.n_plots % n_cols) != 0:
            index = self.n_plots // n_cols
            for n_ax in plot_grid.ax.flat[-index:]:
                n_ax.set_visible(False)
        return plot_grid.fig, plot_grid.ax


class LabelFactory:

    def __init__(
        self,
        gene: str,
        result_type: ResultType,
        ax: plt.Axes,
        y_lim: tuple = None,
        x_label: str = None,
        y_label: str = None,
    ):
        self.gene = gene.replace("_density", "")
        self.result_type = result_type
        self.ax = ax
        self.y_lim = y_lim
        self.x_label = x_label
        self.y_label = y_label
    
    def _generate_label(self) -> plt.Axes:
        if self.y_lim is not None:
            self.ax.set_ylim(*self.y_lim)
        
        if self.x_label is not None:
            self.ax.set_xlabel(self.x_label)
        if self.y_label is not None:
            self.ax.set_ylabel(self.y_label)
        else:
            prefix = "Density" if self.result_type == ResultType.DENSITY else "Percentage"
            suffix = " (over DAPI+ cells)" if self.result_type == ResultType.PERCENTAGE else "(cells/mm²)"
            full_str = f"{prefix} of {self.gene}+ cells {suffix}"
            self.ax.set_ylabel(full_str)
    
    def __call__(self) -> plt.Axes:
        return self._generate_label()


@dataclass
class PlotGrid:
    """
    A class representing a grid of plots.

    Attributes:
        n_rows (int): The number of rows in the grid.
        n_cols (int): The number of columns in the grid.
        figsize (tuple, optional): The size of the figure. Defaults to an empty tuple.
        kwargs (dict, optional): Additional keyword arguments to be passed to `plt.subplots()`. Defaults to an empty dictionary.
    """

    n_rows: int
    n_cols: int
    figsize: tuple = SINGLE_RES_PLOT_FIGSIZE
    kwargs: dict = field(default_factory=dict)

    def __post_init__(self):
        """
        Initialize the PlotGrid object.

        Creates a figure and axes grid using `plt.subplots()`.

        Returns:
            None
        """
        self.fig, self.ax = plt.subplots(
            self.n_rows,
            self.n_cols,
            figsize=self.figsize,
            **self.kwargs,
        )


def _get_color_palette(
    categories: list[str],
    custom_colors: dict[str, str] = None,
) -> dict | str:
    """
    Get the color palette for the plot.

    Args:
        categories (list[str]): The categories to be plotted.
        custom_colors (dict[str, str], optional): The custom colors to be used. Defaults to None.

    Returns:
        dict | str: The color palette to be used for the plot.
    """
    if custom_colors is None:
        return DEFAULT_COLOR_PALETTE
    else:
        if len(custom_colors) < len(categories):
            return _extend_color_palette(categories, custom_colors)
        else:
            return custom_colors

def _extend_color_palette(
    categories: list[str],
    custom_colors: dict[str, str],
) -> dict[str, str]:
    """
    Extend the color palette to include more colors.

    Args:
        categories (list[str]): The categories to be plotted.
        custom_colors (dict[str, str]): The custom colors to be used.

    Returns:
        dict[str, str]: The extended color palette.
    """
    missing_colors = sns.color_palette(DEFAULT_COLOR_PALETTE, len(categories) - len(custom_colors))
    missing_categories = [cat for cat in categories if cat not in custom_colors]

    custom_colors.update(
        {cat: color for cat, color in zip(missing_categories, missing_colors)}
    )
    return custom_colors
