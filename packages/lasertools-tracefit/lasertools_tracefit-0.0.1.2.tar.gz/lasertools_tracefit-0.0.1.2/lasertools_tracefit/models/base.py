"""Define an fitting pulse model template"""

import dataclasses
import numpy as np
import lasertools_rffthelper as rfft
from lasertools_pulsedispersion.models import _DispersionBase
from lasertools_pulsenlo.models import _NLOBase
from lasertools_traceprocess import Normalizer
from lasertools_pulsemodel import PulseModel
from lasertools_pulse import Pulse
from lasertools_trace.models.base import _TraceBase


def residual_sos(am, bm):
    """Calculate the residual sum of squares of two arrays

    Keyword arguments:
    - am -- Array 1
    - bm -- Array 2"""

    a = (am - bm) ** 2
    b = a.flatten()
    s = b.sum()
    return s


@dataclasses.dataclass
class ModelSettings:
    """Class to store settings for the fit model

    Keyword arguments:
    - name -- name of fitting model
    - variables_static -- model variables not used for fit
    - variables_fitting_ranges -- valid ranges of variables used for fit"""

    name: str
    variables_static: dict
    variables_fitting_ranges: list[dict]


class _ModelBase:
    """Base class for a pulse fitting model"""

    def __init__(self, settings: ModelSettings, axes: rfft.Axes):
        self.settings = settings
        self.axes = axes
        self.pulsemodel: PulseModel = None
        self.pulsereference: Pulse = None
        self.dispersionmodels: list[_DispersionBase] = None
        self.nlomodels: list[_NLOBase] = None


class ModelComparison:
    """Class to handle comparison between fit and measurement"""

    def __init__(
        self,
        fit_model: _ModelBase,
        trace_model: _TraceBase,
        trace_data: np.ndarray,
        normalizer: Normalizer,
    ):
        self.normalizer = normalizer
        self.fit_model = fit_model
        self.trace_model = trace_model
        self.trace_data = normalizer.normalize(trace_data)
        self.sos_total = np.var(self.trace_data) * np.size(self.trace_data)

    def calculate_fitness(self, solution):
        """Calculation of residual sum of squares"""

        trace_model_test = self.normalizer.normalize(
            self.trace_solution(solution)
        )
        R2 = 1 - (
            residual_sos(trace_model_test, self.trace_data) / self.sos_total
        )
        return R2

    def trace_solution(self, solution):
        """Calculate the test trace"""
        pulse_test = self.fit_model.update(solution)
        trace_model_test = (
            np.abs(
                self.trace_model.spectrum_complex(
                    self.trace_model.time(pulse_test)
                )
            )
            ** 2
        )
        return trace_model_test
