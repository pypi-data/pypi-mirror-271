"""Find maxima"""
import numpy as np


def weighted1d(
    x_axis: np.ndarray,
    array: np.ndarray,
):
    """Return weighted average parameter for 1d data

    Keyword arguments:
    - x_axis -- Raw x axis values
    - array -- Array of weights"""

    array_weighted_x_axis = x_axis * array
    array_weights = np.sum(array)
    weighted_average_x = np.sum(array_weighted_x_axis) / array_weights
    return weighted_average_x
