import adsk.core, adsk.fusion, traceback
import apper


class DumpWorkspacePanels(apper.Fusion360CommandBase):
    def on_execute(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs, args, input_values):
        ui = None
        try:
            app = adsk.core.Application.get()
            ui = app.userInterface

            file_dialog = ui.createFileDialog()
            file_dialog.isMultiSelectEnabled = False
            file_dialog.title = "Specify result filename"
            file_dialog.filter = 'Text files (*.txt)'
            file_dialog.filterIndex = 0
            dialog_result = file_dialog.showSave()
            if dialog_result == adsk.core.DialogResults.DialogOK:
                filename = file_dialog.filename
            else:
                return

            result = '\n\n** Workspaces  (' + str(ui.workspaces.count) + ')____\n'
            for workspace in ui.workspaces:
                try:
                    msg = '   ' + workspace.id + ' (' + str(workspace.toolbarTabs.count) + ')____\n'
                    result += msg
                    for tab in workspace.toolbarTabs:
                        msg = '      ' + tab.id + ' (' + str(tab.toolbarPanels.count) + ')____\n'
                        result += msg
                        for panel in tab.toolbarPanels:
                            msg = '            ' + panel.id + '   Visible:  ' + str(panel.isVisible) + '\n'
                            result += msg
                except:
                    msg = '******failed        ' +  workspace.id + '\n'

            output = open(filename, 'w')
            output.writelines(result)
            output.close()

            ui.messageBox('File written to "' + filename + '"')
        except:
            if ui:
                ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

