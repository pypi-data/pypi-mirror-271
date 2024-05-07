"""A pulse fitting model"""
import copy
import numpy as np
import rffthelper_pulsemodel as pmd
import rffthelper_pulsedispersion as pdp
from .base import _ModelBase


class GaussianPolynomial(_ModelBase):
    """A pulse fitting model using abitrary amplitude and polynomial phase"""

    def check_id(self):
        """Check if model name matches this pulse class"""

        return self.settings.name == "gaussian, polynomial"

    def initialize(self):
        """Initialize the fitting model"""

        self.pulsemodel = pmd.PulseModel(
            self.axes, "GaussianWavelength", "Polynomial"
        )

    def update(self, variables_fitting):
        """Update the fitting model"""

        self.pulsemodel.update(
            {
                "wavelength_center": 299792458
                / self.settings.variables_static["frequency_center"],
                "wavelength_bandwidth": variables_fitting[0],
            },
            {
                "frequency_center": self.settings.variables_static[
                    "frequency_center"
                ],
                "phase_coefficients": [
                    0,
                    0,
                    variables_fitting[1],
                    variables_fitting[2],
                    variables_fitting[3],
                ],
            },
        )
        return self.pulsemodel.make_pulse()
