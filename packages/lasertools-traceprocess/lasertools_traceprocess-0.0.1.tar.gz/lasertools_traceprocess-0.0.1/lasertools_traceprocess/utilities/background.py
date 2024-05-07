"""Background subtraction"""

import numpy as np


def minimum(array: np.ndarray):
    """Returns array after subtracting minimum value

    Keyword arguments:
    - array -- Array to process"""

    return array - np.min(array)


def corners2d(array: np.ndarray, points: int = 2):
    """Returns array after subtracting mean value of corner pixels

    Keyword arguments:
    - array -- Array to process
    - points (Optional) -- Size of square at corners to average in pixels"""

    points -= 1
    average_corners = np.mean(
        np.vstack(
            [
                array[:points, :points],
                array[-points:, -points:],
                array[:points, -points:],
                array[-points:, :points],
            ]
        )
    )
    return array - average_corners


def extrema(array: np.ndarray, points: int = 1):
    """Returns array after subtracting mean value of edges

    Keywords arguments:
    - array -- Array to process
    - points -- Indices at edges to subtract"""

    average_edges = np.mean(
        np.hstack((array[:, :points], array[:, -points:])), axis=1
    )

    return array - average_edges[..., None]
