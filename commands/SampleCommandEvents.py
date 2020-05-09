import adsk.core
import adsk.fusion
import apper
import json
import config


def palette_push(cmd_id, palette_id, event_args):
    ao = apper.AppObjects()
    palette = ao.ui.palettes.itemById(palette_id)
    app = adsk.core.Application.get()
    cmd = ao.ui.commandDefinitions.itemById(cmd_id)
    toolbar_tab_msg = make_tab_message_list()

    action_data = {'cmd_id': cmd_id,
                   'version': app.version,
                   'toolbar_tab_msg': toolbar_tab_msg,

                   }
    # Send message to the HTML Page
    if palette:
        palette.sendInfoToHTML('command', json.dumps(action_data))


def make_tab_message():

    msg = ""
    ao = apper.AppObjects()

    tab: adsk.core.ToolbarTab
    for tab in ao.ui.activeWorkspace.toolbarTabs:

        if tab.isActive:
            msg += "Toolbar Tab: {}\n".format(tab.id)
            toolbar_panel: adsk.core.ToolbarPanel
            for toolbar_panel in tab.toolbarPanels:
                msg += "    Panel: {}\n".format(toolbar_panel.id)
                toolbar_control: adsk.core.ToolbarControl
                for toolbar_control in toolbar_panel.controls:
                    msg += "     - {}\n".format(toolbar_control.id)

    return msg


def make_tab_message_list():

    msg = ""
    ao = apper.AppObjects()

    tab: adsk.core.ToolbarTab
    for tab in ao.ui.activeWorkspace.toolbarTabs:

        if tab.isActive:
            msg += "Toolbar Tab: {}<OL>".format(tab.id)
            toolbar_panel: adsk.core.ToolbarPanel
            for toolbar_panel in tab.toolbarPanels:
                msg += "<LI>Panel: {}<UL>\n".format(toolbar_panel.id)
                toolbar_control: adsk.core.ToolbarControl
                for toolbar_control in toolbar_panel.controls:
                    msg += "<LI>{}</LI>".format(toolbar_control.id)
                msg += "</UL></LI>"
            msg += "</OL>"
    return msg


def make_panel_message_list():

    msg = ""
    ao = apper.AppObjects()

    msg += "<OL>"
    toolbar_panel: adsk.core.ToolbarPanel
    for toolbar_panel in ao.ui.activeWorkspace.toolbarPanels:

        msg += "<LI>Panel: {}<UL>\n".format(toolbar_panel.id)
        toolbar_control: adsk.core.ToolbarControl
        for toolbar_control in toolbar_panel.controls:
            msg += "<LI>{}</LI>".format(toolbar_control.id)
        msg += "</UL></LI>"
    msg += "</OL>"
    return msg


class CommandStreamEvent(apper.Fusion360CommandEvent):

    def command_event_received(self, event_args, command_id, command_definition):
        palette_push(command_id, config.command_stream_palette_id, event_args)
