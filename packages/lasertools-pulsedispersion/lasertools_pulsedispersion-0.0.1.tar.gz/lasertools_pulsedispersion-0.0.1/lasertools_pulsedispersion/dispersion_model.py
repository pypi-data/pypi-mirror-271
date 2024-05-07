"""Functions to locate and apply a dispersion model"""
import numpy as np
import lasertools_pulsedispersiondata as pddat
from lasertools_pulse import Pulse
from lasertools_pulsedispersion import models


def find_model(element_name: str):
    """Return dispersion model object and parameters for specified element

    Keywords arguments:
    element_name -- Name of dispersive element"""

    element_parameters = pddat.load_data(element_name)

    for model_class in models.model_classes.values():
        model_object = model_class()
        if model_object.check_id(element_parameters["model"]):
            break

    return model_object, element_parameters


def disperse_pulse(
    pulse: Pulse,
    element_model: models._DispersionBase,
    element_model_parameters: dict,
    **model_kwargs
):
    """Return dispersed pulse after element

    Keyword arguments:
    - pulse -- Object representing input pulse
    - element_model -- Model object representing dispersive element
    - element_model_parameters -- Parameters for model object
    - model_kwargs -- Input parameters for specific model"""

    phase = element_model.define_phase(
        element_model_parameters, pulse.axes.frequency_axis, **model_kwargs
    )
    pulse.define_spectrum_complex(pulse.spectrum_complex * np.exp(-1j * phase))
    return pulse
