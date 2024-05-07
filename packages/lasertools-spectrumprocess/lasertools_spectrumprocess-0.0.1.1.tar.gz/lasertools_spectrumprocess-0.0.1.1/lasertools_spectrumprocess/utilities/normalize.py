"""Normalize data"""

import numpy as np


def maximum(array):
    """Return array normalized by the maximum value

    Keyword arguments:
    - array -- Array to process"""

    return array / np.max(array)
