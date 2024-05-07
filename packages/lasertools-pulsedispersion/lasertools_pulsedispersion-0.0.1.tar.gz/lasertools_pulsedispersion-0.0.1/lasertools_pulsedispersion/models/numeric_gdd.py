"""Define an amplitude model"""
import numpy as np
from .base import _DispersionBase


class NumericGDD(_DispersionBase):
    """An arbitrary index of refraction defined by an equation"""

    def check_id(self, id_string):
        """Check if model name matches this pulse class"""

        return id_string == "numeric GDD"

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
        data_gdd = np.flip(np.array(parameter_dictionary["gdd_fs2"]) * 1e-30)

        gdd = np.interp(
            frequencies,
            data_frequencies,
            data_gdd,
            left=0,
            right=0,
        )

        gd = np.cumsum(gdd) * 2 * np.pi * (frequencies[1] - frequencies[0])

        phase_full = number * (
            np.cumsum(gd) * 2 * np.pi * (frequencies[1] - frequencies[0])
        )

        return phase_full
