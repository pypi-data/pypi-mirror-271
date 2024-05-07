"""Define an phase model template"""
import numpy as np


class _DispersionBase:
    """Base class for a pulse phase template"""

    def __init__(self):
        pass

    def frequency_to_wavelength(self, frequencies):
        """Returns wavelength (m) from frequency (Hz)

        Keyword arguments:
        - frequencies -- frequencies in Hertz to convert"""

        index_minimum_frequency = np.argmin(np.abs(frequencies))
        if frequencies[index_minimum_frequency] == 0:
            frequencies[index_minimum_frequency] = (
                1e-20 * frequencies[index_minimum_frequency + 1]
            )

        return 299792458 / frequencies

    def wavelength_to_frequency(self, wavelengths):
        """Returns frequency (Hz) from wavelength (m)

        Keyword arguments:
        - wavelengths -- wavelengths in meters to convert"""

        index_minimum_wavelength = np.argmin(np.abs(wavelengths))
        if wavelengths[index_minimum_wavelength] == 0:
            wavelengths[index_minimum_wavelength] = (
                1e-20 * wavelengths[index_minimum_wavelength + 1]
            )

        return 299792458 / wavelengths

    def subtract_linear_component(self, phase_full):
        """Returns phase after fitting and subtracting a line

        Keyword arguments:
        - frequencies -- frequencies"""

        polyfitted = np.poly1d(
            np.polyfit(range(len(phase_full)), phase_full, 1)
        )
        return phase_full - polyfitted(range(len(phase_full)))

    def apply_valid_range(self, parameter_dictionary, wavelengths, variable):
        indices_valid_range = np.sort(
            [
                (
                    np.abs(
                        wavelengths
                        - np.min(parameter_dictionary["valid_range"])
                    )
                ).argmin(),
                (
                    np.abs(
                        wavelengths
                        - np.max(parameter_dictionary["valid_range"])
                    )
                ).argmin(),
            ]
        )

        variable[0 : indices_valid_range[0]] = variable[indices_valid_range[0]]
        variable[indices_valid_range[1] :] = variable[indices_valid_range[1]]
        return variable
