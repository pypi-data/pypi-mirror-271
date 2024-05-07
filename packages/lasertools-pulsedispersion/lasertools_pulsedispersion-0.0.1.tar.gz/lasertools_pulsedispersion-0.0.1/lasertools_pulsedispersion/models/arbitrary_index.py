"""Define an amplitude model"""

import numpy as np
from .base import _DispersionBase


class ArbitraryIndex(_DispersionBase):
    """An arbitrary index of refraction defined by an equation"""

    def check_id(self, id_string):
        """Check if model name matches this pulse class"""

        return id_string == "arbitrary index"

    def define_phase(
        self,
        parameter_dictionary: dict,
        frequencies: np.ndarray,
        distance: float,
        model_variables: list = None,
    ):
        """Define phase"""
        wavelengths_um = self.frequency_to_wavelength(frequencies) * 1e6

        wavelengths_um[
            wavelengths_um * 1e-6 < np.min(parameter_dictionary["valid_range"])
        ] = (np.min(parameter_dictionary["valid_range"]) * 1e6)

        wavelengths_um[
            wavelengths_um * 1e-6 > np.max(parameter_dictionary["valid_range"])
        ] = (np.max(parameter_dictionary["valid_range"]) * 1e6)

        index_function = eval(parameter_dictionary["index"])
        index = index_function(wavelengths_um)

        phase_full = 2 * np.pi * index * distance * frequencies / 299792458
        return self.subtract_linear_component(phase_full)
