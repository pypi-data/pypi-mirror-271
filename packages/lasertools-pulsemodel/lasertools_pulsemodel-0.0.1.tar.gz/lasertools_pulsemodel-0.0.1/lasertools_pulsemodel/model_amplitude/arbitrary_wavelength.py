"""Define an amplitude model"""
import numpy as np
from .base import _AmplitudeBase


class AmplitudeArbitraryWavelength(_AmplitudeBase):
    """An arbitrary amplitude"""

    def check_id(self, id_string):
        """Check if model name matches this pulse class"""

        return id_string == "ArbitraryWavelength"

    def amplitude(
        self,
        frequency_axis,
        parameters,
    ):
        """Return spectral amplitude"""

        frequency_raw = np.flip(299792458 / parameters["wavelengths"])
        intensities_raw = np.flip(parameters["intensities"])
        intensities_raw[intensities_raw < 0] = 0
        amplitude_raw = np.sqrt(intensities_raw)
        amplitude = np.interp(
            np.abs(frequency_axis),
            frequency_raw,
            amplitude_raw * 299792458 / (frequency_raw**2),
            left=0,
            right=0,
        )
        amplitude /= np.max(amplitude)

        return amplitude
