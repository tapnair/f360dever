import adsk.core
import adsk.fusion
import adsk.cam

import json

import apper
import config


# Class for a Fusion 360 Palette Command
class AuthPaletteShow(apper.PaletteCommandBase):

    # Run when user executes command in UI, useful for handling extra tasks on palette like docking
    def on_palette_execute(self, palette: adsk.core.Palette):

        # Dock the palette to the right side of Fusion window.
        if palette.dockingState == adsk.core.PaletteDockingStates.PaletteDockStateFloating:
            palette.dockingState = adsk.core.PaletteDockingStates.PaletteDockStateRight
        palette.htmlFileURL = config.auth_url

    # Run when ever a fusion event is fired from the corresponding web page
    def on_html_event(self, html_args: adsk.core.HTMLEventArgs):
        ao = apper.AppObjects()

        # Parse incoming message and build message for Fusion message box
        data = json.loads(html_args.data)
        config.access_token = data['access_token']
        config.refresh_token = data['refresh_token']
        msg = "Forge Bearer Token:: {}".format(
            config.access_token,
        )

        # Display Message
        ao = apper.AppObjects()
        ao.ui.messageBox(msg)

    # Handle any extra cleanup when user closes palette here
    def on_palette_close(self):
        pass