from typing import List
import numpy as np


def running_mean(out: int, up_to_id = None, *list_path: List[str]) -> np.ndarray:
    """
    Calculate the running mean of specified columns across multiple files.

    Parameters
    ----------
    inp : List[int]
        List of column indices to calculate the mean for.

    out : int
        Index of the column to consider as the output feature.

    up_to_id : int or None, optional
        Index of the last file to include in the calculation. If None, all files are included. Default is None.

    list_path : List[str]
        Variable number of file paths containing the data.

    Returns
    -------
    np.ndarray
        An array containing the running mean for each specified column.

    """
    cumulative_sum = 0
    
    if up_to_id is None:
        N = len(list_path)
    else:
        N = up_to_id + 1
    
    for r in range(0, N):
        data = np.load(list_path[r])
        cumulative_sum += data[:, out]

    return cumulative_sum/N


def running_std(out: int, up_to_id = None, ddof: int = 1, *list_path: List[str]) -> np.ndarray:
    """
    Calculate the running standard deviation of specified columns across multiple files.

    Parameters
    ----------
    inp : List[int]
        List of column indices to calculate the standard deviation for.

    out : int
        Index of the column to consider as the output feature.

    up_to_id : int or None, optional
        Index of the last file to include in the calculation. If None, all files are included. Default is None.

    ddof : int, optional
        Degrees of freedom. Default is 1 (unbiased variance estimator).

    list_path : List[str]
        Variable number of file paths containing the data.

    Returns
    -------
    np.ndarray
        An array containing the running standard deviation for each specified column.

    """
    cumulative_sum = 0

    if up_to_id is None:
        max_id = len(list_path)
    else:
        max_id = up_to_id + 1

    mean = running_mean(out, max_id - 1, *list_path)
    for r in range(0, max_id):
        data = np.load(list_path[r])
        cumulative_sum += (data[:, out] - mean)**2

    return (cumulative_sum/(max_id - ddof))**0.5
