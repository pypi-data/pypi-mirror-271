"""Define an phase model template"""


class _PhaseBase:
    """Base class for a pulse phase template"""

    def __init__(self):
        self.frequency_center = None
