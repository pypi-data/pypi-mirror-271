"""Process a spectrum"""

import sys
import dataclasses
import numpy as np
from spectrumprocessdev import utilities


@dataclasses.dataclass
class ProcessingSettings:
    """Class to store signal and frequency axis parameters

    Keyword arguments:
    - background_subtraction (Optional) -- Whether to subtract the background
    - background_fraction (Optional) -- Signal level below which to set at zero
    - savgol_window (Optional) -- Window for Savgol filter
    - normalize (Optional) -- Whether to apply normalization"""

    background_subtraction: bool = True
    background_fraction: float = None
    savgol_window: int = None
    normalize: bool = True


@dataclasses.dataclass
class SpectrumData:
    """Class to store spectrum parameters

    Keyword arguments:
    - trace -- Measured trace
    - wavelength_axis (Optional) -- Measurement wavelength axis (m)"""

    spectrum: np.ndarray
    wavelength_axis: np.ndarray = None


def process(spectrum: SpectrumData, settings: ProcessingSettings):
    """Process spectrum

    Keyword arguments:
    - spectrum -- Object representing spectrum
    - settings -- Object containing processing settings"""

    spectrum_processed = spectrum.spectrum
    if settings.background_subtraction:
        spectrum_processed = utilities.background.minimum(spectrum_processed)

    if settings.savgol_window is not None:
        spectrum_processed = utilities.smooth.savgolfilter(
            spectrum_processed, settings.savgol_window
        )

    if settings.background_fraction is not None:
        spectrum_processed = utilities.threshold.fraction(
            spectrum_processed, settings.background_fraction
        )

    if settings.normalize:
        spectrum_processed = utilities.normalize.maximum(spectrum_processed)

    wavelength_weighted = None
    if spectrum.wavelength_axis is not None:
        wavelength_weighted = utilities.maxima.weighted1d(
            spectrum.wavelength_axis, spectrum_processed
        )

    return spectrum_processed, wavelength_weighted
