""" Functions for measuring expression levels and densities. """
import copy

import numpy as np
import pandas as pd


from cell_typist.core.experiment import HCRexperiment
from cell_typist.core.datatypes import MarkerSelection, Result


def threshold_expression(
    experiment: HCRexperiment,
    thresholds: dict,
    custom_selections: list[MarkerSelection] | None = None,
    inplace: bool = False,
) -> HCRexperiment:
    """
    Calculate the percentage of cells expressing each gene.

    Args:
        experiment (HCRexperiment): An instance of the HCRexperiment class.
        thresholds (dict): A dictionary mapping channel names to threshold values.
        custom_selections (list[MarkerSelection], optional): A list of MarkerSelection objects containing custom selections.
        inplace (bool, optional): Whether to modify the experiment object in-place. Defaults to False.

    Returns:
        HCRexperiment: An instance of the HCRexperiment class.

    Raises:
        ValueError: If the number of thresholds does not match the number of channels.

    Example:
        >>> experiment = HCRexperiment()
        >>> thresholds = {'channel1': 0.5, 'channel2': 0.3}
        >>> custom_selections = [MarkerSelection('selection1', ['channel1'], ['channel2'])]
        >>> threshold_expression(experiment, thresholds, custom_selections)
    """
    if not inplace:
        experiment = copy.deepcopy(experiment)

    channels = experiment.channel_names
    df = experiment.detections.dataframe
    if len(thresholds) != len(channels):
        raise ValueError(
            f"Number of thresholds ({len(thresholds)}) does not match number of channels ({len(channels)})."
        )

    if isinstance(thresholds, list):
        thresholds = {
            channel: threshold for channel, threshold in zip(channels, thresholds)
        }

    experiment.thresholds = thresholds

    for channel in channels:
        percentage_series = pd.Series(
            np.zeros(len(df), dtype=bool), index=df.index, name=f"{channel}_pos"
        )
        threshold = thresholds[channel]
        percentage_series[df[channel] > threshold] = True
        experiment.add_detection_column(f"{channel}_pos", percentage_series)

    custom_selections = [] if custom_selections is None else custom_selections
    for selection in custom_selections:
        df = experiment.detections.dataframe
        columns = selection.positive_selection + selection.negative_selection
        columns = [f"{ch}_pos" for ch in columns]
        df_selection = df[columns].copy()
        for marker in selection.negative_selection:
            sel = f"{marker}_pos"
            df_selection[sel] = np.invert(df_selection[sel].values)

        intersection = df_selection.min(axis=1)
        experiment.add_detection_column(f"{selection.name}_pos", intersection > 0)

    return experiment


def threshold_expression_interactive(
    experiment: HCRexperiment, custom_selections: list[MarkerSelection] | None = None
) -> HCRexperiment:
    """
    Calculate the percentage of cells expressing each gene interactively.

    Args:
        experiment (HCRexperiment): An instance of the HCRexperiment class.
        custom_selections (list[MarkerSelection], optional): A list of MarkerSelection objects containing custom selections. Defaults to [].

    Returns:
        HCRexperiment: An instance of the HCRexperiment class.
    """
    thresholds = {}

    for channel in experiment.channel_names:
        threshold = input(f"Enter threshold for {channel}: ")
        thresholds[channel] = int(threshold)

    return threshold_expression(experiment, thresholds, custom_selections)


def calculate_percentages(
    experiment: HCRexperiment,
    groupby: list[str],
    decimals: int = 2,
) -> Result:
    """
    Calculate the percentages of positive detections for each group in the experiment.

    Args:
        experiment (HCRexperiment): The HCRexperiment object containing the data.
        groupby (list[str]): The list of columns to group the data by.
        decimals (int, optional): The number of decimal places to round the percentages to. Defaults to 2.

    Returns:
        Result: The result object containing the calculated percentages.

    Raises:
        ValueError: If expression thresholds have not been calculated.

    Example:
        >>> experiment = HCRexperiment()
        >>> groupby = ['Sample', 'Condition']
        >>> calculate_percentages(experiment, groupby)
    """

    if not experiment.is_expression_thresholded:
        exception_message = "Expression thresholds have not been calculated. Please run threshold_expression() first."
        raise ValueError(exception_message)

    df = experiment.detections.dataframe

    missing_columns = [column for column in groupby if column not in df.columns]
    if len(missing_columns) > 0:
        raise ValueError(f"Columns {missing_columns} are missing from the dataframe.")

    data_columns = [key for key in experiment.data if "_pos" in key]

    full_groupby = groupby
    full_data_columns = data_columns
    missing_metadata = [
        column for column in experiment.metadata if column not in full_groupby
    ]

    df_percentages = df.groupby(full_groupby)[full_data_columns].apply(
        lambda x: x.sum() / x.count().replace(0, 1).ffill() * 100
    )

    df_percentages = df_percentages.reset_index().round(decimals=decimals)

    df_percentages_metadata = (
        df.groupby(full_groupby)[missing_metadata].first().reset_index()
    )
    df_percentages = pd.merge(df_percentages, df_percentages_metadata, how="left")

    rename_dict = {col: col.replace("_x", "") for col in df_percentages.columns if col.endswith("_x")}
    df_percentages = df_percentages.rename(columns=rename_dict)
    df_percentages.drop(columns=[col for col in df_percentages.columns if col.endswith("_y")], inplace=True)

    rename_dict = {}
    for col in df_percentages.columns:
        rename_dict[col] = col.replace("_pos", "")
    df_percentages = df_percentages.rename(columns=rename_dict)

    return Result(
        name="percentage",
        experiment=experiment.name,
        groupby=groupby,
        measurements=[col for col in df_percentages.columns if col not in groupby],
        data=df_percentages,
    )


def calculate_densities(
    experiment: HCRexperiment,
    groupby: list[str],
    decimals: int = 2,
) -> Result:
    """
    Calculate the densities of positive detections for each group in the experiment.

    Args:
        experiment (HCRexperiment): The HCRexperiment object containing the data.
        groupby (list[str]): The list of columns to group the data by.
        decimals (int, optional): The number of decimal places to round the densities to. Defaults to 2.

    Returns:
        Result: The result object containing the calculated densities.

    Raises:
        ValueError: If expression thresholds have not been calculated.

    Example:
        >>> experiment = HCRexperiment()
        >>> groupby = ['Sample', 'Condition']
        >>> calculate_densities(experiment, groupby)
    """

    if not experiment.is_expression_thresholded:
        exception_message = "Expression thresholds have not been calculated. Please run threshold_expression() first."
        raise ValueError(exception_message)

    if isinstance(groupby, str):
        groupby = [groupby]

    df = experiment.detections.dataframe

    missing_columns = [column for column in groupby if column not in df.columns]
    if len(missing_columns) > 0:
        raise ValueError(f"Columns {missing_columns} are missing from the dataframe.")

    data_columns = [key for key in experiment.data if "_pos" in key]

    full_groupby = ["Image"] + groupby
    full_data_columns = data_columns
    missing_metadata  = [column for column in experiment.metadata if column not in full_groupby]

    df_densities = (
        df.groupby(full_groupby)[full_data_columns].sum(numeric_only=True).reset_index()
    )
    df_densities_metadata = (
        df.groupby(full_groupby)[missing_metadata].first().reset_index()
    )
    df_densities = pd.merge(df_densities, df_densities_metadata, how="left")

    grouped_area = experiment.annotations.dataframe.groupby(full_groupby)['area'].sum().reset_index()
    df_densities = df_densities.merge(grouped_area, on='Image', how='left')

    rename_dict = {col: col.replace("_x", "") for col in df_densities.columns if col.endswith("_x")}
    df_densities = df_densities.rename(columns=rename_dict)
    df_densities.drop(columns=[col for col in df_densities.columns if col.endswith("_y")], inplace=True)


    for column in data_columns:
        df_densities[f"{column}_density"] = (
            df_densities[column] / df_densities["area"]
        ).round(decimals=decimals)

    new_data_columns = data_columns + [f"{column}_density" for column in data_columns] + ["area"]
    df_densities_grouped = df_densities.groupby(groupby)[new_data_columns].mean().reset_index()
    df_densities_metadata = df_densities.groupby(groupby)[missing_metadata].first().reset_index()
    df_densities = pd.merge(df_densities_grouped, df_densities_metadata, how="left")

    df_densities["area"] = df_densities["area"].round(decimals=4)

    rename_dict = {}
    for col in df_densities.columns:
        rename_dict[col] = (
            col.replace("_pos", "_count")
            if "density" not in col
            else col.replace("_pos", "")
        )
    df_densities = df_densities.rename(columns=rename_dict)

    return Result(
        name="density",
        experiment=experiment.name,
        groupby=groupby,
        measurements=[col for col in df_densities.columns if "density" in col],
        data=df_densities,
    )
