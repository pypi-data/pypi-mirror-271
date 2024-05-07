"""Import all models"""
import importlib
import pkgutil
import os
from .base import _ModelBase

models_directory = os.path.dirname(__file__)
for _, name, _ in pkgutil.iter_modules([models_directory]):
    importlib.import_module("." + name, __package__)

model_classes = {
    ModelClass.__name__: ModelClass
    for ModelClass in _ModelBase.__subclasses__()
}
