"""Smooth data"""

import scipy
import numpy as np


def savgolfilter(
    array: np.ndarray, savgol_window_length: float, savgol_order: int = 3
):
    """Returns array after Savgol filtering

    Keyword argument:
    - array -- Array to process
    - savgol_window_length -- Window of Savgol filter
    - savgol_order (Optional) -- Order of Savgol filter"""

    return scipy.signal.savgol_filter(
        array, savgol_window_length, savgol_order
    )
