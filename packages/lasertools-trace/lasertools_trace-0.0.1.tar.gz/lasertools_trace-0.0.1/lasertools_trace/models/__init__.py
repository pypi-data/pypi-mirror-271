"""Find trace model"""

import importlib
import pkgutil
import os
from .base import _TraceBase

trace_models_directory = os.path.dirname(__file__)
for _, name, _ in pkgutil.iter_modules([trace_models_directory]):
    importlib.import_module("." + name, __package__)

trace_classes = {
    TraceClass.__name__: TraceClass
    for TraceClass in _TraceBase.__subclasses__()
}