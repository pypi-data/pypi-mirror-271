"""Find maxima"""

import numpy as np


def weighted2d(
    x_axis: np.ndarray,
    y_axis: np.ndarray,
    array: np.ndarray,
):
    """Return weighted average parameters for 2d data

    Keyword arguments:
    - x_axis -- Raw x axis values (second array dimension)
    - y_axis -- Raw y axis values (first array dimension)
    - array -- Array of weights"""

    x_axis_array, y_axis_array = np.meshgrid(x_axis, y_axis)
    array_weighted_x_axis = x_axis_array * array
    array_weighted_y_axis = y_axis_array * array
    array_weights = np.sum(array)
    weighted_average_x = np.sum(array_weighted_x_axis) / array_weights
    weighted_average_y = np.sum(array_weighted_y_axis) / array_weights
    return weighted_average_x, weighted_average_y
