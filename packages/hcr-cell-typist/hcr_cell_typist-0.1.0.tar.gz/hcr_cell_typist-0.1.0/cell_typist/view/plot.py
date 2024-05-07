"""
This module contains functions for plotting the results of the cell_typist pipeline.
"""

# pylint: disable=too-many-arguments
# pylint: disable=no-name-in-module

import re

from typing import Literal

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import matplotlib.colors as mcolors
from skimage.filters import threshold_li

from cell_typist.core.experiment import HCRexperiment
from cell_typist.core.datatypes import Result
from cell_typist.view.factories import FigureFactory, BarPlotFactory, StripPlotFactory, LinePlotFactory, LabelFactory


PLOT_KIND_BINDINGS = {
    "hist": sns.histplot,
    "kde": sns.kdeplot,
}

RESULTPLOT_KIND_BINDINGS = {
    "hist": BarPlotFactory,
    "line": LinePlotFactory,
}

SINGLE_EXP_PLOT_FIGSIZE = (10, 5)
SINGLE_RES_PLOT_FIGSIZE = (5, 5)


def plot_expression(
    experiment: HCRexperiment,
    gene_x: str | list[str],
    x_threshold: float = 0,
    hue: str = None,
    kind: str = "hist",
    figsize: tuple = SINGLE_EXP_PLOT_FIGSIZE,
    automatic_treshold: bool = False,
    kwargs: dict = None,
) -> plt.Figure:
    """
    Plot the expression of two genes in the experiment.

    Args:
        experiment (HCRexperiment): An instance of the HCRexperiment class.
        gene_x (str): The name of the gene to plot on the x-axis.
        gene_y (str, optional): The name of the gene to plot on the y-axis. Defaults to None.
        x_threshold (float, optional): The threshold for the x-axis. Defaults to 0.
        y_threshold (float, optional): The threshold for the y-axis. Defaults to 0.
        hue (str, optional): The name of the gene to use for color coding. Defaults to None.
        kind (str, optional): The type of plot to create. Defaults to "hist".
        figsize (tuple, optional): The size of the figure. Defaults to (10, 5).
        automatic_treshold (bool, optional): If True, the threshold is set to the 99th percentile of the data. Defaults to False.
        kwargs (dict, optional): Additional keyword arguments to pass to the plotter function. Defaults to {}.

    Returns:
        plt.Figure: The matplotlib Figure object.
    """
    if not experiment.are_channels_defined:
        raise ValueError(
            "Channel names have not been defined. Please run define_channel_names() first."
        )

    if not hue:
        hue = "file"

    data = experiment.detections.dataframe

    try:
        plotter = PLOT_KIND_BINDINGS[kind]
    except KeyError as exc:
        raise ValueError(
            f"Kind {kind} not supported. Choose from {PLOT_KIND_BINDINGS}."
        ) from exc

    if not kwargs:
        kwargs = {
            "bins": 128,
        }

    if isinstance(gene_x, str):
        genes = [gene_x]
        actual_figsize = SINGLE_EXP_PLOT_FIGSIZE
    else:
        genes = gene_x
        actual_figsize = (
            SINGLE_EXP_PLOT_FIGSIZE[0],
            SINGLE_EXP_PLOT_FIGSIZE[1] * len(gene_x),
        )

    if figsize != SINGLE_EXP_PLOT_FIGSIZE:
        actual_figsize = figsize

    fig, ax = plt.subplots(len(genes), 1, figsize=actual_figsize)
    for i, gene in enumerate(genes):
        actual_ax = ax[i] if len(genes) > 1 else ax
        x_95_percentile = np.nanpercentile(data[gene].values, 99)
        plotter(
            x=gene,
            data=data,
            hue=hue,
            ax=actual_ax,
            **kwargs,
        )
        actual_ax.set_xlabel(f"Number of estimated {gene} spots")
        actual_ax.set_xlim(0, x_95_percentile)

        if automatic_treshold:
            x_threshold = threshold_li(data[gene].values)
            actual_ax.axvline(x_threshold, color="red")

    return fig


def plot_results(
    results: Result,
    x: str | list[str],
    y: str,
    hue: str = None,
    split_by: str = None,
    plot_kind: Literal["hist", "line"] = "hist",
    x_label: str = None,
    y_label: str = None,
    y_lim: tuple = None,
    fig_title: str = None,
    overlay_dots: bool = True,
    x_order: list[str] = None,
    custom_colors: dict[str, str] = None,
) -> plt.Figure | list[plt.Figure]:
    """
    Plot the results of a cell typing analysis.

    Args:
        results (Result): The cell typing results.
        x (str | list[str]): The variable(s) to plot on the x-axis.
        y (str): The variable to plot on the y-axis.
        hue (str, optional): The variable to use for color grouping. Defaults to None.
        split_by (str, optional): The variable to use for splitting the plot. Defaults to None.
        plot_kind (Literal["hist", "line"], optional): The kind of plot to create. Defaults to "hist".
        x_label (str, optional): The label for the x-axis. Defaults to None.
        y_label (str, optional): The label for the y-axis. Defaults to None.
        y_lim (tuple, optional): The y-axis limits. Defaults to None.
        fig_title (str, optional): The title of the figure. Defaults to None.
        overlay_dots (bool, optional): Whether to overlay dots on the bars or lines. Defaults to True.
        x_order (list[str], optional): The order of the x-axis categories. Defaults to None, meaning alphabetical.
        custom_colors (dict[str, str], optional): A dictionary of custom colors for the hue categories. Defaults to None.

    Returns:
        plt.Figure | list[plt.Figure]: The plotted figure(s).
    """

    
    if plot_kind not in RESULTPLOT_KIND_BINDINGS.keys():
        raise ValueError(
            f"Kind {plot_kind} not supported. Choose from {RESULTPLOT_KIND_BINDINGS.keys()}."
        )
    else:
        base_plot_factory = RESULTPLOT_KIND_BINDINGS[plot_kind]

    if custom_colors:
        _validate_custom_colors(results.data, hue, custom_colors)
    
    result_type = results.type.value.capitalize()
    
    base_title = f"Cell {result_type}"


    df_results = results.data
    if split_by:
        figs = []
        for name, group in df_results.groupby(split_by):
            group_results = Result(
                name=name,
                experiment=results.experiment,
                groupby=results.groupby,
                measurements=results.measurements,
                data=group
            )
            group_results.type = results.type

            split_title  = fig_title if fig_title else base_title
            split_title += f" - {name.capitalize()}"

            fig = plot_results(
                results=group_results,
                x=x,
                y=y,
                hue=hue,
                plot_kind=plot_kind,
                x_label=x_label,
                y_label=y_label,
                y_lim=y_lim,
                fig_title=split_title,
                overlay_dots=overlay_dots,
                x_order=x_order,
                custom_colors=custom_colors,
            )

            plot_type = results.type.value.capitalize()

            title_addition = ""
            if split_by:
                title_addition = f" in {name}"
            fig.suptitle(f"{plot_type} of cells{title_addition}", fontsize=16)

            figs.append(fig)
        return figs
    else:
        genes = [y] if isinstance(y, str) else y

        fig, ax, genes = FigureFactory(
            y=genes,
            result_type=results.type,
        )()

        for i, gene in enumerate(genes):
            actual_ax = ax[i]

            if base_plot_factory == LinePlotFactory:
                x_order = None
            else:
                if x_order:
                    # check if all x_order values are in the data
                    if not all([value in df_results[x].values for value in x_order]):
                        raise ValueError("Not all x_order values are in the data")

            actual_ax = base_plot_factory(
                x=x,
                y=gene,
                hue=hue,
                data=df_results,
                ax=actual_ax,
                x_order=x_order,
                custom_colors=custom_colors,
            )()

            if overlay_dots:
                actual_ax = StripPlotFactory(
                    x=x,
                    y=gene,
                    hue=hue,
                    data=df_results,
                    ax=actual_ax,
                    x_order=x_order,
                    custom_colors=custom_colors,
                )()
            
            LabelFactory(
                gene=gene,
                result_type=results.type,
                ax=actual_ax,
                y_lim=y_lim,
                x_label=x_label,
                y_label=y_label,
            )()

            if fig_title and len(genes) == 1:
                actual_ax.set_title(fig_title)
            else:
                ax_title = f"{result_type} of {gene.replace("_density", "")}+ cells"
                actual_ax.set_title(ax_title)

        if fig_title and len(genes) > 1:
            fig.suptitle(fig_title, fontsize=16)
        elif (not fig_title) and len(genes) > 1:
            fig.suptitle(base_title, fontsize=16)
        
        plt.tight_layout()
        return fig


def _validate_custom_colors(data: pd.DataFrame, hue: str, custom_colors: dict[str, str]) -> None:
    """
    Validate the custom colors dictionary.

    Args:
        data (pd.DataFrame): The data to be plotted.
        hue (str): The column name for the hue.
        custom_colors (dict[str, str]): A dictionary of custom colors for the hue categories.

    Raises:
        ValueError: If the custom colors dictionary is invalid.
    """

    if not all([category in data[hue].values for category in custom_colors.keys()]):
        missing_categories = [category for category in custom_colors.keys() if category not in data[hue].values]
        raise ValueError(f"Not all custom color categories are in the data: {missing_categories}")
    
    if not all([_validate_color(color) for color in custom_colors.values()]):
        invalid_colors = [color for color in custom_colors.values() if not _validate_color(color)]
        raise ValueError(f"Not all custom colors are valid names or hex codes: {invalid_colors}")


def _validate_color(color: str) -> bool:
    """
    Validate a color hex code.

    Args:
        color (str): The color hex code.

    Returns:
        bool: True if the color is a valid hex code.
    """

    if re.match(r"^#(?:[0-9a-fA-F]{3}){1,2}$", color):
        return True
    else:
        try:
            mcolors.to_rgba(color)
            return True
        except ValueError:
            return False