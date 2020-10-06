import sys
from collections import defaultdict
from importlib import reload

import adsk.core
import adsk.fusion
import adsk.cam

from ..apper import apper


def get_name_type(selection):
    try:
        the_selection_type = selection.objectType
    except:
        the_selection_type = "could not determine type"

    try:
        name = selection.name
    except:
        name = "Object has no name.    {} \n".format(str(sys.exc_info()[0]))

    return name, the_selection_type


def attributes_for_selection(selection, msg_list, filter_by_group, filter_group_name):
    name, the_selection_type = get_name_type(selection)

    msg_list.append("Object Type:  {} \n".format(the_selection_type))
    msg_list.append("Object Name:  {} \n".format(name))
    try:
        attributes = selection.attributes
        if len(attributes) == 0:
            msg_list.append("   There are no attributes")
            return

        attribute_list = make_attributes_message(attributes, filter_by_group, filter_group_name)
    except:
        msg_list.append("    Selected Object Type Does not support attributes")
        return

    if len(attribute_list) > 0:
        msg_list.extend(attribute_list)


def make_attributes_message(attributes, filter_by_group, filter_group_name):
    attribute_list = []

    for attribute in attributes:
        try:
            if filter_by_group:
                if filter_group_name == attribute.groupName:
                    attribute_list.append("    {}, {}, {} \n".format(attribute.groupName, attribute.name, attribute.value))
            else:
                attribute_list.append("    {}, {}, {} \n".format(attribute.groupName, attribute.name, attribute.value))
        except:
            attribute_list.append("some failure")

    return attribute_list


class AttributeSelectionCommand(apper.Fusion360CommandBase):

    def on_input_changed(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs, changed_input,
                         input_values):
        ao = apper.AppObjects()
        # Get the values from the user input
        filter_by_group = input_values['bool_input_id']
        filter_group_name = input_values['string_input_id']
        all_selections = input_values['selection_input_id']

        msg_list = []

        if len(all_selections) > 0:
            selection = all_selections[0]
            attributes_for_selection(selection, msg_list, filter_by_group, filter_group_name)

            msg = ''.join(msg_list)

            text_box_input: adsk.core.TextBoxCommandInput = inputs.itemById('text_box_input_id')
            # text_box_input.numRows = len(msg_list) + 2
            text_box_input.formattedText = msg

    def on_execute(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs, args, input_values):
        pass

    def on_create(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs):
        # Other Input types
        inputs.addBoolValueInput('bool_input_id', 'Filter by Group Name?', True)
        inputs.addStringValueInput('string_input_id', 'Attribute Group', "")
        selection_input = inputs.addSelectionInput('selection_input_id', 'Selection', 'Select Something')
        selection_input.setSelectionLimits(0, 1)
        # Read Only Text Box
        inputs.addTextBoxCommandInput('text_box_input_id', 'Details:', 'Nothing Selected', 20, True)


def get_all_attributes(attribute_group, attribute_name):
    # Get a reference to all relevant application objects in a dictionary
    ao = apper.AppObjects()

    msg_list = []

    attributes = ao.design.findAttributes(attribute_group, attribute_name)

    if len(attributes) > 0:
        unique_objects = defaultdict(list)
        orphans = []

        for attribute in attributes:
            if attribute.parent is not None:
                obj_id = apper.item_id(attribute.parent, 'f360dever')
                unique_objects[obj_id].append(attribute)
            else:
                orphans.append(attribute)

        for key, object_attributes in unique_objects.items():
            name, the_selection_type = get_name_type(object_attributes[0].parent)
            apper.remove_item_id(object_attributes[0].parent, 'f360dever')
            attribute_list = make_attributes_message(object_attributes, False, '')

            if len(attribute_list) > 0:
                msg_list.append("\n ----*********---- \n\n")
                msg_list.append("Object Type:  {} \n".format(the_selection_type))
                msg_list.append("Object Name:  {} \n".format(name))
                msg_list.append("Attributes (Group Name, Attribute Name, Value):\n")
                msg_list.extend(attribute_list)

        if len(orphans) > 0:
            msg_list.append("\n ----*********---- \n\n")
            msg_list.append("Orphans (parent no longer exists):\n")
            msg_list.append("Attributes (Group Name, Attribute Name, Value):\n")
            attribute_list = make_attributes_message(orphans, False, '')
            if len(attribute_list) > 0:
                msg_list.extend(attribute_list)

        msg = ''.join(msg_list)

    else:

        msg = " Could not find any attributes with group: {} and name: ".format(attribute_group, attribute_name)

    return msg


class AllAttributesCommand(apper.Fusion360CommandBase):

    def on_input_changed(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs, changed_input,
                         input_values):
        # Get the values from the user input
        attribute_group = input_values['attribute_group_id']
        attribute_name = input_values['attribute_name_id']

        msg = get_all_attributes(attribute_group, attribute_name)
        text_box_input = inputs.itemById('text_box_input_id')
        text_box_input.formattedText = msg

    def on_execute(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs, args, input_values):
        pass

    def on_create(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs):
        ao = apper.AppObjects()

        # Other Input types
        inputs.addStringValueInput('attribute_group_id', 'Attribute Group', "")
        inputs.addStringValueInput('attribute_name_id', 'Attribute Name', "")

        msg = get_all_attributes("", "")
        inputs.addTextBoxCommandInput('text_box_input_id', 'Details:', msg, 20, True)


class AddAttributeCommand(apper.Fusion360CommandBase):

    def on_input_changed(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs, changed_input,
                         input_values):

        all_selections = input_values['selection_input_id']

        if len(all_selections) > 0:
            selection = all_selections[0]
            msg_list = []

            attributes_for_selection(selection, msg_list, False, '')

            msg = ''.join(msg_list)

            text_box_input: adsk.core.TextBoxCommandInput = inputs.itemById('text_box_input_id')
            text_box_input.numRows = len(msg_list) + 2
            text_box_input.formattedText = msg

    def on_execute(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs, args, input_values):
        ao = apper.AppObjects()
        all_selections = input_values['selection_input_id']
        selection = all_selections[0]

        attribute_group = input_values['attribute_group_id']
        attribute_name = input_values['attribute_name_id']
        attribute_value = input_values['attribute_value_id']

        try:
            selection.attributes.add(attribute_group, attribute_name, attribute_value)
        except:
            ao.ui.messageBox("Could not add attribute to selection")

    def on_create(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs):

        # Other Input types
        selection_input = inputs.addSelectionInput('selection_input_id', 'Selection', 'Select Something')
        inputs.addStringValueInput('attribute_group_id', 'Attribute Group', '')
        inputs.addStringValueInput('attribute_name_id', 'Attribute Name', '')
        inputs.addStringValueInput('attribute_value_id', 'Attribute Value', '')

        selection_input.setSelectionLimits(0, 1)
        # Read Only Text Box
        inputs.addTextBoxCommandInput('text_box_input_id', 'Details:', 'Nothing Selected', 1, True)
