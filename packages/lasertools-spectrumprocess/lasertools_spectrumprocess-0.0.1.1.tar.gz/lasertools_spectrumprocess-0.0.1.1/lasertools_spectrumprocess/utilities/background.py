"""Background subtraction"""

import numpy as np


def minimum(array: np.ndarray):
    """Returns array after subtracting minimum value

    Keyword arguments:
    - array -- Array to process"""

    return array - np.min(array)
