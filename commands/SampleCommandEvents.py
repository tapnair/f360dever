import adsk.core
import adsk.fusion
import apper
import json
import config


def palette_push(cmd_id, palette_id):
    ao = apper.AppObjects()
    palette = ao.ui.palettes.itemById(palette_id)
    app = adsk.core.Application.get()

    action_data = {'cmd_id': cmd_id,
                   'version': app.version
                   }
    # Send message to the HTML Page
    if palette:
        palette.sendInfoToHTML('command', json.dumps(action_data))


class CommandStreamEvent(apper.Fusion360CommandEvent):

    def command_event_received(self, event_args, command_id, command_definition):
        palette_push(command_id, config.command_stream_palette_id)