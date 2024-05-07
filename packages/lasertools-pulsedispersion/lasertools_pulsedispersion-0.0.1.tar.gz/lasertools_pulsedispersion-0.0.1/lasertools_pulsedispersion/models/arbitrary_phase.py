"""Define an amplitude model"""

import numpy as np
from .base import _DispersionBase


class ArbitraryPhase(_DispersionBase):
    """An arbitrary index of refraction defined by an equation"""

    def check_id(self, id_string):
        """Check if model name matches this pulse class"""

        return id_string == "arbitrary phase"

    def define_phase(
        self,
        parameter_dictionary: dict,
        frequencies: np.ndarray,
        model_variables: list,
    ):
        """Define phase"""

        return eval(parameter_dictionary["phase"])
