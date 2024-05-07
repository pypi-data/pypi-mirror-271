"""Define a phase model"""
import numpy as np
from .base import _PhaseBase


class Polynomial(_PhaseBase):
    """An arbitrary phase"""

    def check_id(self, id_string):
        """Check if model name matches this pulse class"""

        return id_string == "Polynomial"

    def phase(
        self,
        frequency_axis,
        parameters,
    ):
        """Return spectral phase (radians) for an abitrary polynomial"""

        frequency_center = parameters["frequency_center"]
        phase = np.zeros(np.shape(frequency_axis))

        for phase_order, phase_factor in enumerate(
            parameters["phase_coefficients"]
        ):
            phase += (
                np.sign(frequency_axis)
                * 2
                * np.pi
                * phase_factor
                * (np.abs(frequency_axis) - frequency_center) ** phase_order
            )
        return phase
