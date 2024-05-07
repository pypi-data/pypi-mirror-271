"""A module to define a pulse model"""
import sys
import numpy as np
import lasertools_pulse as pls
from lasertools_rffthelper.axes import Axes
from . import model_amplitude
from . import model_phase


class PulseModel:
    """An object representing a model pulse based on axes linked by RFFT

    Keyword arguments:
    - axes --  Object representing a signal and frequency axes linked by RFFT
    - amplitude_model_name -- String of amplitude model name
    - amplitude_model_parameters -- Array of amplitude specific parameters
    - phase_model_name -- String of phase model name
    - phase_model_parameters -- Array of phase specific parameters
    """

    def __init__(
        self,
        axes: Axes,
        amplitude_name: str,
        phase_name: str,
    ):
        self.axes = axes
        self.amplitude_model = self._amplitude_model(amplitude_name)
        self.phase_model = self._phase_model(phase_name)
        self.amplitude = None
        self.phase = None
        self.spectrum_complex = None

    def _amplitude_model(self, amplitude_name: str):
        """Find amplitude model"""

        pulse_class = None
        for _pulse_class in model_amplitude.pulse_classes.values():
            _test_pulse_class = _pulse_class()
            if _test_pulse_class.check_id(amplitude_name):
                pulse_class = _test_pulse_class

        if not pulse_class:
            sys.exit("Amplitude model not found.")

        return pulse_class

    def _phase_model(self, phase_name: str):
        """Find amplitude model"""

        pulse_class = None
        for _pulse_class in model_phase.pulse_classes.values():
            _test_pulse_class = _pulse_class()
            if _test_pulse_class.check_id(phase_name):
                pulse_class = _test_pulse_class

        if not pulse_class:
            sys.exit("Phase model not found.")

        return pulse_class

    def update(
        self,
        new_amplitude_parameters: dict = None,
        new_phase_parameters: dict = None,
        update=False,
    ):
        """Update amplitude and/or phase parameters"""

        if new_phase_parameters is not None:
            self.phase = self.phase_model.phase(
                self.axes.frequency_axis, new_phase_parameters
            )
            update = True
        if new_amplitude_parameters is not None:
            self.amplitude = self.amplitude_model.amplitude(
                self.axes.frequency_axis, new_amplitude_parameters
            )
            update = True

        if update:
            self.spectrum_complex = self.amplitude * np.exp(-1j * self.phase)

    def make_pulse(self):
        """Create pulse object"""

        pulse = pls.Pulse(self.axes)
        pulse.define_spectrum_complex(self.spectrum_complex)
        return pulse
