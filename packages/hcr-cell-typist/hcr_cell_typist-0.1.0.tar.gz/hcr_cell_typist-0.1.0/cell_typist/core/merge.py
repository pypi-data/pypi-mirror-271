import copy

from cell_typist.core.datatypes import Result


def merge_results(
    results: list[Result],
    experiment_name: str | None = None,
) -> Result:
    """
    Merge the results of multiple experiments.

    Args:
        results (list[Result]): A list of Result objects.
        experiment_name (str, optional): Name of the merged experiment. Defaults to sum of existing names.

    Returns:
        Result: A Result object containing the merged results.
    """

    if any([not isinstance(result, Result) for result in results]):
        raise ValueError("All elements in the results list must be Result objects.")
    
    if any([result.type != results[0].type for result in results]):
        raise ValueError("All results must have the same type. (e.g. 'percentage', 'density')")

    all_measurements = [result.measurements for result in results]

    try:
        results[0]._validate_matching_lists(all_measurements)
        print("All measurements match.")
    except ValueError:
        print("All measurements do not match.")

    new_result = copy.deepcopy(results[0].append(results[1:]))

    new_result.type = results[0].type

    return new_result
