"""Helper functions"""

import sys
from lasertools_rffthelper import Axes
from lasertools_tracefit import models


def find_fit_model(
    settings: models.base.ModelSettings,
    axes: Axes,
):
    """Define a trace based on a model"""

    fit_class = None
    for _model_class in models.model_classes.values():
        _test_model_class = _model_class(
            settings,
            axes,
        )
        if _test_model_class.check_id():
            fit_class = _test_model_class

    if not fit_class:
        sys.exit("Fitting model not found.")

    fit_class.initialize()

    return fit_class
