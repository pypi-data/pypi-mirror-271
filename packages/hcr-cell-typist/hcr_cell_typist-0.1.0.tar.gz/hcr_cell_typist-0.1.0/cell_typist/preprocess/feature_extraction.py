""" Module for feature extraction from images. """

# pylint: disable=line-too-long

import copy

import pandas as pd
from cell_typist.core.experiment import HCRexperiment


def parse_file_names(
    experiment: HCRexperiment,
    template: str,
    separator: str = "_",
    verbose: bool = True,
    inplace: bool = False,
) -> HCRexperiment:
    """
    Parses the file names of the detections and extract informations.

    Parameters:
    template (str): The template for parsing the file names, e.g. "condition_age_timepoint"
    separator (str): The separator to use for parsing the file names. Defaults to "_".
    verbose (bool): Whether to print the information extracted. Defaults to True.

    Returns:
    experiment (HCRexperiment): The experiment with the parsed file names.
    """

    if not isinstance(experiment, HCRexperiment):
        raise TypeError(
            f"Expected experiment to be of type HCRexperiment, got {type(experiment)}"
        )

    if not inplace:
        experiment = copy.deepcopy(experiment)

    if separator not in template:
        raise ValueError(f"Template {template} does not contain separator {separator}.")

    for i, dataset in enumerate([experiment.detections, experiment.annotations]):
        template_parts = template.split(separator)
        # TODO: Remove extension from file names properly
        name_parts = (
            dataset.get_series(column_name="Image")
            .str.split(".tif", expand=True)[0]
            .str.split(".czi", expand=True)[0]
            # .str.replace(".tif", "")
            .str.split(separator, expand=True)
        )

        for n, temp in enumerate(template_parts):
            dataset.add_column(temp, name_parts[n].to_list())

        if "annotation" not in dataset.dataframe.columns:
            dataset.add_series("annotation", dataset.get_series("Parent"))

        metadata = ["annotation"] + template_parts
        experiment.metadata = metadata

        if verbose and i == 0:
            print(f"Parsed file names from template {template}.")
            print("Extracted the following metadata:")
            for temp in template_parts:
                print(f" - {temp}")
                print(f"   - Unique values:{dataset.dataframe[temp].unique()}")

    return experiment


def define_channel_names(
    experiment: HCRexperiment,
    template: str,
    separator: str = "-",
    verbose: bool = True,
    inplace: bool = False,
) -> HCRexperiment:
    """
    Defines the channel names for the experiment.

    Parameters:
    template (str): The template for defining the channel names, e.g. "condition-age-timepoint"
    separator (str): The separator to use for defining the channel names. Defaults to "-".
    verbose (bool): Whether to print the information extracted. Defaults to True.

    Returns:
    experiment (HCRexperiment): The experiment with the defined channel names.
    """

    if not isinstance(experiment, HCRexperiment):
        raise TypeError(
            f"Expected experiment to be of type HCRexperiment, got {type(experiment)}"
        )

    if not inplace:
        experiment = copy.deepcopy(experiment)

    if separator not in template:
        raise ValueError(f"Template {template} does not contain separator {separator}.")

    template_parts = template.split(separator)
    df = experiment.detections.dataframe
    orig_ch_names = experiment.original_channel_names

    if len(template_parts) != len(orig_ch_names):
        exception_str = (
            f"Template '{template}' does not match the number of channels in the data."
        )
        exception_str += f"\nTemplate: {len(template_parts)} channels"
        exception_str += f"\nData: {len(orig_ch_names)} channels"
        raise ValueError(exception_str)

    channels = []
    for name, marker in zip(orig_ch_names, template_parts):
        # df[marker] = df[name]
        experiment.add_detection_column(marker, df[name].values.tolist())
        channels.append(marker)

    if verbose:
        print(f"Defined channel names from template {template}.")
        print("Extracted the following metadata:")
        for temp in template_parts:
            print(f" - {temp}")

    experiment.set_channel_names(channels)

    return experiment


def split_columns(
    experiment: HCRexperiment,
    column_name: str,
    template: str = None,
    separator: str = "-",
    verbose: bool = True,
    inplace: bool = False,
) -> HCRexperiment:
    """
    Splits a column in the experiment's dataframe into multiple columns based on a separator.

    Args:
        experiment (HCRexperiment): The experiment object containing the dataframe.
        column_name (str): The name of the column to be split.
        template (str, optional): The template to use for naming the split columns. Defaults to None.
        separator (str, optional): The separator to split the column on. Defaults to "-".
        verbose (bool, optional): Whether to print information about the split. Defaults to True.

    Returns:
        HCRexperiment: The modified experiment object with the split columns.

    Raises:
        TypeError: If the experiment object is not of type HCRexperiment.
        ValueError: If the specified column is not present in the dataframe or if the number of template parts does not match the number of split parts.
    """

    if not isinstance(experiment, HCRexperiment):
        raise TypeError(
            f"Expected experiment to be of type HCRexperiment, got {type(experiment)}"
        )

    if not inplace:
        experiment = copy.deepcopy(experiment)

    dataframe_bindings = {
        "detections": (
            experiment.detections.dataframe,
            experiment.add_detection_column,
            {"is_annotation": True},
        ),
        "annotations": (
            experiment.annotations.dataframe,
            experiment.add_annotation_column,
            {},
        ),
    }

    for df, add_column, kwargs in dataframe_bindings.values():
        if column_name not in df.columns:
            raise ValueError(f"Column {column_name} not present in dataframe.")
        df_split = df[column_name].str.split(separator, expand=True)

        if template:
            template_parts = template.split(separator)
            if len(template_parts) == len(df_split.columns):
                df_split.columns = template_parts
            else:
                exeption_message = f"Number of template parts ({len(template_parts)}) does not match number of split parts ({len(df_split.columns)})"
                exeption_message += f"\nGenerated template parts: {template_parts}"
                exeption_message += "\nGenerated split parts:"
                exeption_message += f"\n{df_split.head()}"
                exeption_message += (
                    "\n\nAdjust the template to match the number of split parts."
                )
                raise ValueError(exeption_message)
        else:
            df_split.add_prefix(f"{column_name}_")

        for col in df_split.columns:
            add_column(col, df_split[col].values.tolist(), **kwargs)
            if col not in experiment.metadata:
                experiment.metadata.append(col)

    if verbose:
        print(f"Split column name {column_name} into multiple columns.")
        print("Extracted the following metadata:")
        print(df_split.head())

    return experiment


def merge_columns(
    experiment: HCRexperiment,
    column_names: list[str],
    new_column_name: str,
    separator: str = "-",
    keep_old: bool = True,
    verbose: bool = True,
    inplace: bool = False,
) -> HCRexperiment:
    """
    Merges multiple columns in the experiment dataframe into a new column.

    Args:
        experiment (HCRexperiment): The experiment object containing the dataframe.
        column_names (list[str]): List of column names to be merged.
        new_column_name (str): Name of the new merged column.
        separator (str, optional): Separator to be used between merged values. Defaults to "-".
        keep_old (bool, optional): Whether to keep the original columns after merging. Defaults to True.
        verbose (bool, optional): Whether to print the merged column and a message. Defaults to True.

    Returns:
        HCRexperiment: The updated experiment object with the merged column.

    Raises:
        TypeError: If the experiment object is not of type HCRexperiment.
        ValueError: If one of the specified columns is not present in the dataframe.
    """

    if not isinstance(experiment, HCRexperiment):
        raise TypeError(
            f"Expected experiment to be of type HCRexperiment, got {type(experiment)}"
        )

    if not inplace:
        experiment = copy.deepcopy(experiment)

    dataframe_bindings = {
        "detections": (
            experiment.detections.dataframe,
            experiment.add_detection_column,
            {"is_annotation": True},
        ),
        "annotations": (
            experiment.annotations.dataframe,
            experiment.add_annotation_column,
            {},
        ),
    }

    for df, add_column, kwargs in dataframe_bindings.values():
        if not all(col in df.columns for col in column_names):
            missing_columns = [col for col in column_names if col not in df.columns]
            raise ValueError(f"Columns {missing_columns} not present in dataframe.")

        merged_series = pd.concat([df[col] for col in column_names], axis=1)
        merged_series = df.apply(
            lambda row: separator.join(row[col] for col in column_names),
            axis=1,
        )

        add_column(new_column_name, merged_series.tolist(), **kwargs)

        if not keep_old:
            df.drop(columns=column_names, inplace=True)

    if verbose:
        print(f"Merged columns {column_names} into {new_column_name}.")
        print(f"{merged_series}")

    return experiment


def replace_in_column(
    experiment: HCRexperiment,
    column_name: str,
    old_value: str,
    new_value: str,
    verbose: bool = True,
    inplace: bool = False,
) -> HCRexperiment:
    """
    Replaces a value in a column of the experiment dataframe.

    Args:
        experiment (HCRexperiment): The experiment object containing the dataframe.
        column_name (str): Name of the column to be modified.
        old_value (str): Value to be replaced.
        new_value (str): Value to replace with.
        verbose (bool, optional): Whether to print the modified column and a message. Defaults to True.

    Returns:
        HCRexperiment: The updated experiment object with the modified column.

    Raises:
        TypeError: If the experiment object is not of type HCRexperiment.
        ValueError: If the specified column is not present in the dataframe.
    """

    if not isinstance(experiment, HCRexperiment):
        raise TypeError(
            f"Expected experiment to be of type HCRexperiment, got {type(experiment)}"
        )

    if not inplace:
        experiment = copy.deepcopy(experiment)

    for df in [experiment.detections.dataframe, experiment.annotations.dataframe]:
        if column_name not in df.columns:
            raise ValueError(f"Column {column_name} not present in dataframe.")

        df[column_name] = df[column_name].str.replace(old_value, new_value)

    if verbose:
        print(f"Replaced {old_value} with {new_value} in column {column_name}.")

    return experiment

def check_unique_values(experiment: HCRexperiment, column_name: str = None) -> None:
    print(f"{experiment.name} has the following metadata:")
    for metadata in experiment.metadata:
        print(f" - {metadata}")
        print(f"   - Unique values:{experiment.detections.dataframe[metadata].unique()}")
