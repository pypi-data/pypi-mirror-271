"""Load dispersion parameters from JSON file"""
import os
import sys
import json


def load_data(element_name):
    """Load JSON file for a dispersive element and return parameter dictionary

    Keyword arguments:
    - element_name -- name of dispersive element
    """

    material_parameters = None
    for directory in list(
        d
        for d in os.listdir(os.path.dirname(__file__))
        if os.path.isdir(os.path.join(os.path.dirname(__file__), d))
    ):
        if material_parameters is None:
            try:
                with open(
                    os.path.join(
                        os.path.dirname(__file__),
                        directory,
                        element_name + ".json",
                    ),
                    "r",
                    encoding="UTF-8",
                ) as material_file:
                    material_parameters = json.load(material_file)
            except FileNotFoundError:
                pass

    if material_parameters is None:
        sys.exit("Dispersion element not found")

    return material_parameters
