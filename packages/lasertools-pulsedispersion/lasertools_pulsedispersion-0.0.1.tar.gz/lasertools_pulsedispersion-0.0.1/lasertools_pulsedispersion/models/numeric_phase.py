"""Define an amplitude model"""
import numpy as np
from .base import _DispersionBase


class NumericPhase(_DispersionBase):
    """An arbitrary index of refraction defined by an equation"""

    def check_id(self, id_string):
        """Check if model name matches this pulse class"""

        return id_string == "numeric phase"

    def define_phase(
        self,
        parameter_dictionary: dict,
        frequencies: np.ndarray,
        number: int = 1,
    ):
        """Define phase"""
        data_frequencies = np.flip(
            self.wavelength_to_frequency(
                np.array(parameter_dictionary["wavelength_nm"]) * 1e-9
            )
        )
        data_phase = np.flip(parameter_dictionary["phase"])

        phase_full = number * np.interp(
            frequencies,
            data_frequencies,
            data_phase,
            left=data_phase[0],
            right=data_phase[-1],
        )

        return phase_full
