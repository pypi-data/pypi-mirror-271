"""Define an amplitude model"""
import numpy as np
from .base import _DispersionBase


class SellmeierIndex(_DispersionBase):
    """An arbitrary index of refraction defined by an equation"""

    def check_id(self, id_string):
        """Check if model name matches this pulse class"""

        return id_string == "Sellmeier 1"

    def define_phase(
        self,
        parameter_dictionary: dict,
        frequencies: np.ndarray,
        distance: float,
    ):
        """Define phase"""
        wavelengths_um = self.frequency_to_wavelength(frequencies) * 1e6
        wavelengths_um_squared = wavelengths_um**2

        # Initialize output arraay
        index_sellmeier_squared = parameter_dictionary[
            "coefficient_A"
        ] * np.ones_like(wavelengths_um)

        # Calculate index over entire range
        for coefficient_b, coefficient_c in zip(
            parameter_dictionary["coefficients_B"],
            parameter_dictionary["coefficients_C"],
        ):
            index_sellmeier_squared += (
                coefficient_b * wavelengths_um_squared
            ) / (wavelengths_um_squared - coefficient_c)

        index_sellmeier_squared = self.apply_valid_range(
            parameter_dictionary,
            wavelengths_um * 1e-6,
            index_sellmeier_squared,
        )

        index = np.sqrt(index_sellmeier_squared)

        phase_full = 2 * np.pi * index * distance * frequencies / 299792458
        return self.subtract_linear_component(phase_full)
