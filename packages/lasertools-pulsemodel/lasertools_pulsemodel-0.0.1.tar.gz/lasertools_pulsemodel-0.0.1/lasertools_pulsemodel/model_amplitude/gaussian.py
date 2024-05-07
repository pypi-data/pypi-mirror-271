"""Define an amplitude model"""
import sys
import numpy as np
from .base import _AmplitudeBase


class GaussianWavelength(_AmplitudeBase):
    """A Gaussian amplitude"""

    def check_id(self, id_string):
        """Check if model name matches this pulse class"""

        return id_string == "GaussianWavelength"

    def amplitude(
        self,
        frequency_axis,
        parameters,
    ):
        """Return spectral amplitude"""

        if parameters["wavelength_center"] == 0:
            sys.exit("Center wavelength cannot be zero.")

        self.frequency_center = 299792458 / parameters["wavelength_center"]
        _frequency_bandwidth = parameters["wavelength_bandwidth"] * (
            299792458 / (parameters["wavelength_center"] ** 2)
        )
        return np.exp(
            (-((np.abs(frequency_axis) - self.frequency_center) ** 2))
            / (_frequency_bandwidth**2 / (4 * np.log(2) / 2))
        )
