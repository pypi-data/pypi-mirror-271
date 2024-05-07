"""Propagate a pulse"""
import sys
import copy

import lasertools_pulsenlo as pln
import lasertools_pulsedispersion as pld
from lasertools_pulse import Pulse


def propagate(process_list: list[dict], pulse: Pulse):
    """Function that returns a pulse after propagation

    Keyword arguments:
    - process_list -- List of dictionaries that define processes
    - pulse -- Initial pulse"""

    pulse_list = [pulse]

    for process in process_list:
        if process["type"] == "dispersion":
            model_object, element_parameters = pld.find_model(
                process["name"]
            )
            pulse = pld.disperse_pulse(
                copy.copy(pulse),
                model_object,
                element_parameters,
                **process["args"]
            )
        elif process["type"] == "nlo":
            model_object = pln.find_model(process["name"])
            pulse = pln.apply(
                copy.copy(pulse), model_object, **process["args"]
            )
        else:
            sys.exit("Process type not found: " + process["type"])
        pulse_list.append(pulse)

    return pulse_list
