"""Smooth data"""

import scipy
import numpy as np


def gaussianblur(array: np.ndarray, sigma: float = 0):
    """Returns array after Gaussian blurring

    Keyword argument:
    - array -- Array to process
    - sigma (Optional) -- Standard deviations for Gaussian blurring"""

    return scipy.ndimage.gaussian_filter(array, sigma)
