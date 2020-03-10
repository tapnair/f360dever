import adsk.core, adsk.fusion, traceback

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
            
        fileDialog = ui.createFileDialog()
        fileDialog.isMultiSelectEnabled = False
        fileDialog.title = "Specify result filename"
        fileDialog.filter = 'Text files (*.txt)'
        fileDialog.filterIndex = 0
        dialogResult = fileDialog.showSave()
        if dialogResult == adsk.core.DialogResults.DialogOK:
            filename = fileDialog.filename
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
