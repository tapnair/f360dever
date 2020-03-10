import adsk.core
import adsk.fusion
import traceback
from random import randint

import apper
from apper import AppObjects

new_number = randint(1000000, 9999900)


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


def make_numbers():
    """

    Returns:

    """
    changed = False
    ao = AppObjects()

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
