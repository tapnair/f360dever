
import sys
from collections import defaultdict
from importlib import reload

import adsk.core
import adsk.fusion
import adsk.cam
import traceback

# Import the entire apper package
import apper

# Alternatively you can import a specific function or class
from apper import AppObjects

reload(apper)


def display_joint_info(joint: adsk.fusion.Joint) -> list:
    """Basic Joint details

    Args:
        joint: this joint
    """
    msg_list = ["Joint name: {}".format(joint.name),
                "Joint Parent Component Name: {} \n".format(joint.parentComponent.name),
                "Joint Occurrence 1 Name: {} \n".format(joint.occurrenceOne.name),
                "Joint Occurrence 1 Path: {} \n".format(joint.occurrenceOne.fullPathName),
                "Joint Occurrence 2 Name: {} \n".format(joint.occurrenceTwo.name),
                "Joint Occurrence 2 Path: {} \n".format(joint.occurrenceTwo.fullPathName)]

    if joint.assemblyContext is not None:
        msg_list.append("Joint ASM Context Name: {} \n".format(joint.assemblyContext.name))
        msg_list.append("Joint ASM Context Path: {} \n".format(joint.assemblyContext.fullPathName))

    else:
        msg_list.append("Joint exists in the root level assembly \n")

    return msg_list


def show_occurrence_joints(occurrence: adsk.fusion.Occurrence, source: str) -> list:
    """

    Args:
        occurrence: occurrence proxy or native object to interogate
        source: String to indicate whether its a proxy or native object
    """
    app = adsk.core.Application.get()
    ui = app.userInterface

    msg_list = []

    try:
        if occurrence.joints is not None:
            msg_list.append(
                "Joints for the selected occurrence's {}: {} \n".format(
                    source, occurrence.name
                )
            )
            if occurrence.joints.count > 0:
                msg_list.append("Joint count: {}".format(occurrence.joints.count))
                for joint in occurrence.joints:
                    msg_list.extend(display_joint_info(joint))
            else:
                msg_list.append("There were no joints associated with this {}: {} \n".format(source, occurrence.name))

    except:
        msg_list.append(
            "Couldn't display joints info for the selected occurrence's {}: {} \n".format(
                source, occurrence.name
            )
        )
        ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

    return msg_list


def get_transform(occurrence: adsk.fusion.Occurrence) -> str:
    """Gets the transform vector as nicely formatted string

    Args:
        occurrence: Input Occurence, could be a proxy or native object

    Returns: Formatted Translation Vector

    """
    _translation = occurrence.transform.translation
    translation_string = "({:.2f}, {:.2f}, {:.2f}) \n".format(_translation.x, _translation.y, _translation.z)

    return translation_string


def show_asm_context(occurrence: adsk.fusion.Occurrence, prefix: str, msg_list) -> None:
    """Walks up assembly tree for selected item

    Args:
        occurrence: input occurrence then recursively sm context
        prefix: continue building up parent contexts as you recursively move up the tree
    """
    app = adsk.core.Application.get()
    ui = app.userInterface

    msg_list.append(
        prefix + "Path: {} \n".format(occurrence.fullPathName)
    )

    msg_list.append(
        prefix + "Translation Vector: {} \n".format(get_transform(occurrence))
    )

    msg_list.append(
        prefix + "Native Object, Path: {} \n".format(occurrence.nativeObject.fullPathName)
    )
    msg_list.append(
        prefix + "Native Object, Translation Vector: {} \n".format(get_transform(occurrence.nativeObject))
    )

    if occurrence.assemblyContext is not None:
        prefix = "ASM Context -> " + prefix
        show_asm_context(occurrence.assemblyContext, prefix, msg_list)

    return msg_list

class AssemblyContextCommand(apper.Fusion360CommandBase):
    def on_input_changed(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs, changed_input,
                         input_values):

        all_selections = input_values['selection_input_id']
        text_box_input: adsk.core.TextBoxCommandInput = inputs.itemById('text_box_input_id')

        if len(all_selections) > 0:
            msg_list = []
            occurrence: adsk.fusion.Occurrence = all_selections[0]
            prefix = "Selected Item (Proxy): "
            show_asm_context(occurrence, prefix, msg_list)

            msg_list.extend(show_occurrence_joints(occurrence, "Proxy"))

            msg = ''.join(msg_list)

            text_box_input.numRows = len(msg_list) + 2
            text_box_input.formattedText = msg

        else:
            text_box_input.formattedText = 'Nothing Selected'

    def on_execute(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs, args, input_values):
        pass

    def on_create(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs):

        # Other Input types
        selection_input = inputs.addSelectionInput('selection_input_id', 'Occurrence', 'Select an Occurrence')

        selection_input.setSelectionLimits(0, 1)
        selection_input.addSelectionFilter('Occurrences')
        # Read Only Text Box
        inputs.addTextBoxCommandInput('text_box_input_id', 'Occurrence Info:', 'Nothing Selected', 1, True)


class AssemblyJointCommand(apper.Fusion360CommandBase):
    def on_input_changed(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs, changed_input,
                         input_values):

        all_selections = input_values['selection_input_id']
        text_box_input: adsk.core.TextBoxCommandInput = inputs.itemById('text_box_input_id')

        if len(all_selections) > 0:
            msg_list_0 = []
            occurrence: adsk.fusion.Occurrence = all_selections[0]
            prefix = "Selected Item (Proxy): "
            show_asm_context(occurrence, prefix, msg_list_0)

            msg_list_1 = show_occurrence_joints(occurrence, "Proxy")
            # msg_list_2 = show_occurrence_joints(occurrence.nativeObject, "Native Object")

            msg = ''.join(msg_list_0)
            msg.join(msg_list_1)
            # msg.join(msg_list_2)

            # text_box_input.numRows = len(msg_list_1) + len(msg_list_2) + 2
            text_box_input.numRows = len(msg_list_1) + 2
            text_box_input.formattedText = msg

        else:
            text_box_input.formattedText = 'Nothing Selected'

    def on_execute(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs, args, input_values):
        pass

    def on_create(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs):

        # Other Input types
        selection_input = inputs.addSelectionInput('selection_input_id', 'Occurrence', 'Select an Occurrence')

        selection_input.setSelectionLimits(0, 1)
        selection_input.addSelectionFilter('Occurrences')
        # Read Only Text Box
        inputs.addTextBoxCommandInput('text_box_input_id', 'Occurrence Info:', 'Nothing Selected', 1, True)


class JointInfoCommand(apper.Fusion360CommandBase):
    def on_input_changed(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs, changed_input,
                         input_values):
        all_selections = input_values['selection_input_id']
        text_box_input: adsk.core.TextBoxCommandInput = inputs.itemById('text_box_input_id')

        if len(all_selections) > 0:

            joint: adsk.fusion.Joint = all_selections[0]
            msg_list = display_joint_info(joint)

            msg = ''.join(msg_list)

            text_box_input.numRows = len(msg_list) + 2
            text_box_input.formattedText = msg

        else:
            text_box_input.formattedText = 'Nothing Selected'

    def on_execute(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs, args, input_values):
        pass

    def on_create(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs):

        # Other Input types
        selection_input = inputs.addSelectionInput('selection_input_id', 'Joint', 'Select a Joint')

        selection_input.setSelectionLimits(0, 1)
        selection_input.addSelectionFilter('Joints')
        # Read Only Text Box
        inputs.addTextBoxCommandInput('text_box_input_id', 'Joint Info:', 'Nothing Selected', 1, True)
