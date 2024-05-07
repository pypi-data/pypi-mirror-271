"""Define a phase model"""
import numpy as np
from .base import _PhaseBase


class ArbitraryFrequency(_PhaseBase):
    """An arbitrary phase"""

    def check_id(self, id_string):
        """Check if model name matches this pulse class"""

        return id_string == "ArbitraryFrequency"

    def phase(
        self,
        frequency_axis,
        parameters,
    ):
        """Return spectral phase (radians)"""

        frequency_raw = parameters["frequencies"]
        phases_raw = parameters["phases"]
        phases = np.interp(
            np.abs(frequency_axis),
            frequency_raw,
            phases_raw,
            left=0,
            right=0,
        )
        return phases
