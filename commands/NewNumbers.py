from importlib import reload

import adsk.core
import adsk.fusion
import traceback
from random import randint

from ..apper import apper
from .. import config

new_number = randint(config.part_number_random_seed_min, config.part_number_random_seed_max)


def make_numbers_one(component: adsk.fusion.Component, changed: bool) -> bool:
    """

    Args:
        component:
        changed:

    Returns:

    """
    global new_number

    if component.partNumber in component.name:
        component.partNumber = str(new_number)
        new_number += 1
        changed = True

    if len(component.description) < 3:
        component.description = component.name
        changed = True

    return changed


def make_numbers() -> bool:
    """

    Returns: True if any component in the design had it's metadata updated

    """
    changed = False
    ao = apper.AppObjects()

    for i, component in enumerate(ao.design.allComponents):

        if component.allOccurrencesByComponent(component).count == 0:
            changed = make_numbers_one(component, changed)

        else:
            if not component.allOccurrencesByComponent(component)[0].isReferencedComponent:
                changed = make_numbers_one(component, changed)

    return changed


class NewNumbers(apper.Fusion360CommandBase):

    def on_execute(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs, args, input_values):
        make_numbers()

