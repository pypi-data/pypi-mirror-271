"""Define an amplitude model"""
import numpy as np
from .base import _AmplitudeBase


class AmplitudeArbitraryFrequency(_AmplitudeBase):
    """An arbitrary amplitude"""

    def check_id(self, id_string):
        """Check if model name matches this pulse class"""

        return id_string == "ArbitraryFrequency"

    def amplitude(
        self,
        frequency_axis,
        parameters,
    ):
        """Return spectral amplitude"""

        frequency_raw = parameters["frequencies"]
        intensities_raw = parameters["intensities"]
        intensities_raw[intensities_raw < 0] = 0
        amplitude_raw = np.sqrt(intensities_raw)
        amplitude = np.interp(
            np.abs(frequency_axis),
            frequency_raw,
            amplitude_raw,
            left=0,
            right=0,
        )
        amplitude /= np.max(amplitude)
        return amplitude
