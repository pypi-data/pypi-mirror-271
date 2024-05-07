"""Interpolate onto computation grid"""

import numpy as np
from scipy.interpolate import RegularGridInterpolator


def interpolate2d(
    x_axis: np.ndarray,
    y_axis: np.ndarray,
    array: np.ndarray,
    x_axis_new: np.ndarray,
    y_axis_new: np.ndarray,
):
    """Return array interpolated onto new axes

    Keyword arguments:
    - x_axis -- Raw x axis values (second array dimension)
    - y_axis -- Raw y axis values (first array dimension)
    - array -- Array to interpolate
    - x_axis_new -- Desired x axis
    - y_axis_new -- Desired y axis"""

    x_axis_new_array, y_axis_new_array = np.meshgrid(x_axis_new, y_axis_new)
    interp = RegularGridInterpolator(
        (y_axis, x_axis), array, bounds_error=False, fill_value=0
    )
    array_new = interp((y_axis_new_array, x_axis_new_array))
    return array_new
