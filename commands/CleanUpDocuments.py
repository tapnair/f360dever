import adsk.core
import adsk.fusion
import adsk
import traceback

import apper
import config
from . import NewNumbers


class CleanUpDocuments(apper.Fusion360CommandBase):

    def on_execute(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs, args, input_values):
        app = adsk.core.Application.get()
        log_file_name = apper.get_log_file_name(config.app_name)
        update_folders(app.data.activeProject.rootFolder, log_file_name)


# TODO make number an optional match field?
def update_folders(root_folder, log_file_name):
    for folder in root_folder.dataFolders:
        update_folders(folder, log_file_name)

    update_folder(root_folder, log_file_name)


def update_folder(root_folder, log_file_name):
    for file in root_folder.dataFiles:
        try:
            update_file(file)
        except:

            log_file = open(log_file_name, 'w')
            log_file.write("The following FIle could not be updated:\n")
            log_file.write(file.name)
            log_file.close()


def update_file(file):
    if file is None:
        return
    try:
        if file.hasChildReferences:
            for ref_file in file.childReferences:
                update_file(ref_file)

        if file.fileExtension == "f3d":
            apper.open_doc(file)

            changed = False

            ao = apper.AppObjects()
            if ao.ui.activeWorkspace.name != 'Model':
                ao.ui.workspaces.itemById('FusionSolidEnvironment').activate()

            if ao.document.documentReferences.count > 0:
                for reference in ao.document.documentReferences:
                    if reference.isOutOfDate:
                        reference.getLatestVersion()
                        changed = True

            numbers_changed = NewNumbers.make_numbers()
            if changed or numbers_changed:
                ao.document.save('Properties updated by {}'.format(config.app_name))

            ao.document.close(False)
    except:
        pass
