"""Functions to locate and apply an nlo model"""
from lasertools_pulse import Pulse
from lasertools_pulsenlo import models


def find_model(process_name: str):
    """Return an NLO model object

    Keywords arguments:
    - process_name -- Name of nonlinear process"""

    for model_class in models.model_classes.values():
        model_object = model_class()
        if model_object.check_id(process_name):
            break

    return model_object


def apply(pulse: Pulse, process_model: models._NLOBase, **model_kwargs):
    """Return dispersed pulse after element

    Keyword arguments:
    - pulse -- Object representing input pulse
    - process_model -- Model object representing dispersive element
    - model_kwargs -- Input parameters for specific model"""

    pulse = process_model.apply_process_pulse(pulse, **model_kwargs)
    return pulse
