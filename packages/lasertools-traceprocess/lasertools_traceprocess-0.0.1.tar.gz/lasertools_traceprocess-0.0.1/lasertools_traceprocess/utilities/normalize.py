"""Normalize data"""

import numpy as np


class Normalizer:
    """Class to normalize the spectral domain trace"""

    def __init__(self, method, limits: list[int] = None):
        """Initialization

        Keyword arguments:
        - method -- discontinuous (1d) or continuous (2d) in parameter domain
        - limits -- index limits in spectral domain"""

        if method == "discontinuous":
            self.normalizer_argument = 0
        elif method == "continuous":
            self.normalizer_argument = None

        if limits is not None:
            self.limits = limits
        else:
            self.limits = [0, -1]

    def norm(self, array: np.ndarray):
        """Return norm of array

        Keyword arguments:
        - array -- Array to calculate norm of"""

        return np.linalg.norm(
            array[self.limits[0] : self.limits[1], :],
            axis=self.normalizer_argument,
        )

    def normalize(self, array: np.ndarray):
        """Return normalzied array

        Keyword arguments:
        - array -- Array to normalizer"""

        return array / self.norm(array)
