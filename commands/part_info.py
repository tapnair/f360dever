#Author-
#Description-
from os import wait
from time import sleep

import adsk.core, adsk.fusion, adsk.cam, traceback

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface

        # *********************See Info about current file*******************************

        # If you manually import the file AND SAVE IT
        # You can uncomment these lines to validate some basic info as presented to the API

        # design: adsk.fusion.Design = app.activeProduct
        #
        # for occurrence in design.rootComponent.allOccurrences:
        #     if occurrence.isReferencedComponent:
        #         ui.messageBox(occurrence.name)
        #
        # ui.messageBox("Does file have child references: {}".format(app.activeDocument.dataFile.hasChildReferences))
        # ui.messageBox("Does file have out of date child references: {}".format(app.activeDocument.dataFile.hasOutofDateChildReferences))
        # ui.messageBox("Does file have parent references: {}".format(app.activeDocument.dataFile.hasParentReferences))
        #
        # for reference in app.activeDocument.dataFile.childReferences:
        #     ui.messageBox(reference.name)

        # ********************To import the model locally**************************

        # import_mgr = app.importManager
        # fus_import = import_mgr.createFusionArchiveImportOptions(
        #     # Update this path:
        #     '/Users/rainsbp/Downloads/49407_fusion-360-160611-9298-42a00b92-screw-2-562a5edc-c441-4cf3-90d6-279e3faf1b96.f3d'
        # )
        #
        # # Import to new document
        # document = import_mgr.importToNewDocument(fus_import)
        # document.activate()

        # Import local
        # import_mgr.importToTarget2(fus_import, design.rootComponent)

        # # ********************Cloud Import**********************************
        #
        # df_future = app.data.activeProject.rootFolder.uploadFile(
        #     '/Users/rainsbp/Downloads/49407_fusion-360-160611-9298-42a00b92-screw-2-562a5edc-c441-4cf3-90d6-279e3faf1b96.f3d'
        # )
        #
        # while df_future.uploadState == adsk.core.UploadStates.UploadProcessing:
        #     if df_future.uploadState == adsk.core.UploadStates.UploadFailed:
        #         ui.messageBox("Upload Failed")
        #     else:
        #         sleep(5)
        #         adsk.doEvents()
        #
        # ui.messageBox("Upload Done")
        # document = app.documents.open(df_future.dataFile)
        #
        # if document is not None:
        #     document.activate()
        # else:
        #     ui.messageBox("open failed")

        # *************Protocol Handler*****************

        import webbrowser
        import pathlib
        local_path = '/Users/rainsbp/Downloads/49407_fusion-360-160611-9298-42a00b92-screw-2-562a5edc-c441-4cf3-90d6-279e3faf1b96.f3d'

        file_uri = pathlib.Path(local_path).as_uri()
        fusion_path = "fusion360://command=open&file=" + file_uri[8:]
        # ui.messageBox(fusion_path)

        webbrowser.open(fusion_path)

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
