"""Thresholding"""

import numpy as np


def fraction(array: np.ndarray, threshold_fraction: float = 0.01):
    """Returns array after thresholding based on fraction

    Keyword arguments:
    - array -- Array to process
    - threshold_fraction (Optional) -- Level below which to set to zero"""

    array[(array / np.max(array)) < threshold_fraction] = 0
    return array
