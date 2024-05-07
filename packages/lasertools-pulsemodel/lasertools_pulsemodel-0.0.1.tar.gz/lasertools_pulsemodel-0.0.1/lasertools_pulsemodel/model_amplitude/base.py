"""Define an amplitude model template"""


class _AmplitudeBase:
    """Base class for a pulse amplitude template"""

    def __init__(self):
        self.frequency_center = None
