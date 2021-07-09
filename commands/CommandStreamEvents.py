import adsk.core
import adsk.fusion
import json

from ..apper import apper
from .. import config


def palette_push(command, action_data):
    ao = apper.AppObjects()
    palette = ao.ui.palettes.itemById(config.command_stream_palette_id)

    # Send message to the HTML Page
    if palette:
        palette.sendInfoToHTML(command, json.dumps(action_data))


def send_command(cmd_id):
    ui_message = make_ui_message()

    action_data = {
        'cmd_id': cmd_id,
        'ui_message': ui_message,
    }
    palette_push('command', action_data)


def send_selections(current_selection):
    selection_list = []
    for selection in current_selection:
        selection_list.append(selection.entity.objectType)

    if len(selection_list) == 0:
        selection_list.append("Nothing Selected")

    action_data = {
        'selection_list': selection_list,
    }
    palette_push('selection', action_data)


def make_ui_message():
    msg = ""
    ao = apper.AppObjects()

    try:
        active_workspace = ao.ui.activeWorkspace
    except RuntimeError:
        return

    msg += "<div>"
    msg += "Name: {}<br>".format(active_workspace.name)
    msg += "ID: {}".format(active_workspace.id)
    msg += "</div>"

    msg += "<h3>Visible Toolbar Tabs</h3>"
    msg += "<div style='padding-left: 25px;'>"

    tab: adsk.core.ToolbarTab
    for tab in active_workspace.toolbarTabs:
        if tab is not None:

            if tab.isVisible:

                msg += "<div>"
                msg += "<h4>{} - Toolbar Tab</h4>".format(tab.name)
                msg += "Name: {}<br>".format(tab.name)
                msg += "ID: {}<br>".format(tab.id)
                msg += "Index: {}<br>".format(tab.index)
                # msg += "Tool Bar Panels:"
                # msg += "</div>"

                # msg += "<UL>"
                # toolbar_panel: adsk.core.ToolbarPanel
                # for toolbar_panel in tab.toolbarPanels:
                #     if toolbar_panel is not None:
                #         if toolbar_panel.isVisible:
                #             # msg += "<LI><b>Panel ID: {}</b><UL>".format(toolbar_panel.id)
                #             toolbar_control: adsk.core.ToolbarControl
                #             for toolbar_control in toolbar_panel.controls:
                #                 if toolbar_control is not None:
                #                     # msg += "<LI>{}</LI>".format(toolbar_control.id)
                #                     pass
                #             msg += "</UL></LI>"
            # msg += "</UL>"

    msg += "</div>"
    return msg


class CommandStreamEvent(apper.Fusion360CommandEvent):

    def command_event_received(self, event_args, command_id, command_definition):
        send_command(command_id)


class SelectionStreamEvent(apper.Fusion360ActiveSelectionEvent):

    def selection_event_received(self, event_args, current_selection):
        send_selections(current_selection)
