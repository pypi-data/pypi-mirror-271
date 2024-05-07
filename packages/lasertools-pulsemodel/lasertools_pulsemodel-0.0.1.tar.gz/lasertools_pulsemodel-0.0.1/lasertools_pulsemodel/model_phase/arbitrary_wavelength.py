"""Define a phase model"""
import numpy as np
from .base import _PhaseBase


class AmplitudePhaseWavelength(_PhaseBase):
    """An arbitrary phase"""

    def check_id(self, id_string):
        """Check if model name matches this pulse class"""

        return id_string == "ArbitraryWavelength"

    def phase(
        self,
        frequency_axis,
        parameters,
    ):
        """Return spectral amplitude"""

        frequency_raw = np.flip(299792458 / parameters["wavelengths"])
        phases_raw = np.flip(parameters["phases"])
        phases = np.interp(
            np.abs(frequency_axis),
            frequency_raw,
            phases_raw,
            left=0,
            right=0,
        )
        return phases
