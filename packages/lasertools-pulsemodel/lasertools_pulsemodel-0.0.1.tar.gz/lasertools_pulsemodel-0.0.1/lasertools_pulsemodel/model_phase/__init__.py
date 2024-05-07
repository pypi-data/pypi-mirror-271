"""Import all models"""
import importlib
import pkgutil
import os
from .base import _PhaseBase

pulse_models_directory = os.path.dirname(__file__)
for _, name, _ in pkgutil.iter_modules([pulse_models_directory]):
    importlib.import_module("." + name, __package__)

pulse_classes = {
    PulseClass.__name__: PulseClass
    for PulseClass in _PhaseBase.__subclasses__()
}
