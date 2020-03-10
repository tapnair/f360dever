#Author-
#Description-

import adsk.core, adsk.fusion, adsk.cam, traceback

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface

        doc = app.activeDocument
        file = doc.dataFile
        urn = file.id
        ui.messageBox(urn)

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
