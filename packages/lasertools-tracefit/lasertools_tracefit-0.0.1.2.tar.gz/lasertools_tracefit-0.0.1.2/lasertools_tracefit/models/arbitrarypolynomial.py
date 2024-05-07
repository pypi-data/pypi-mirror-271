"""A pulse fitting model"""
import copy
import numpy as np
import lasertools_pulsemodel as pmd
import lasertools_pulsedispersion as pdp
from .base import _ModelBase


class ArbitraryPolynomial(_ModelBase):
    """A pulse fitting model using abitrary amplitude and polynomial phase"""

    def check_id(self):
        """Check if model name matches this pulse class"""

        return self.settings.name == "arbitrary, polynomial"

    def initialize(self):
        """Initialize the fitting model"""

        self.pulsemodel = pmd.PulseModel(
            self.axes, "ArbitraryFrequency", "Polynomial"
        )
        self.pulsemodel.update(
            {
                "frequencies": self.settings.variables_static["frequencies"],
                "intensities": self.settings.variables_static["intensities"],
            },
            {
                "frequency_center": self.settings.variables_static[
                    "frequency_center"
                ],
                "phase_coefficients": [
                    0,
                    0,
                    0,
                    0,
                    0,
                ],
            },
        )
        self.pulsereference = self.pulsemodel.make_pulse()
        self.dispersionmodels = [pdp.find_model("polynomial")]

    def update(self, variables_fitting):
        """Update the fitting model"""

        dispersion_model_object = self.dispersionmodels[0][0]
        dispersion_model_dictionary = self.dispersionmodels[0][1]
        model_variables = np.insert(
            variables_fitting,
            0,
            self.settings.variables_static["frequency_center"],
        )

        return pdp.disperse_pulse(
            copy.copy(self.pulsereference),
            dispersion_model_object,
            dispersion_model_dictionary,
            model_variables=model_variables,
        )
