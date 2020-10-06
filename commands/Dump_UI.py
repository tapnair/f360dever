import adsk.core
import adsk.fusion
import traceback

from ..apper import apper


class DumpUICommand(apper.Fusion360CommandBase):
    def on_execute(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs, args, input_values):
        ui = None
        try:
            app = adsk.core.Application.get()
            ui = app.userInterface

            dialog_result = ui.messageBox('Create a full report (list and control details) or \n'
                                          'minimal report (control list only)?', 'UI Report Type',
                                          adsk.core.MessageBoxButtonTypes.YesNoCancelButtonType,
                                          adsk.core.MessageBoxIconTypes.QuestionIconType
                                          )
            if dialog_result == adsk.core.DialogResults.DialogYes:
                full_report = True
            elif dialog_result == adsk.core.DialogResults.DialogNo:
                full_report = False
            else:
                return

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

            qat_toolbar = ui.toolbars.itemById('QAT')
            print(qat_toolbar.id)

            # Display the name of all of the existing toolbars.
            result = '** Toolbars (' + str(ui.toolbars.count) + ') **\n'
            for toolbar in ui.toolbars:
                msg = '   ' + toolbar.id + ' (' + str(toolbar.controls.count) + ')____\n'
                result += msg
                result = get_controls(toolbar.controls, 2, full_report, result)

            result += '\n\n** Toolbar Panels (' + str(ui.allToolbarPanels.count) + ')____\n'
            for panel in ui.allToolbarPanels:
                msg = '   ' + panel.id + ' (' + str(panel.controls.count) + ')____\n'
                msg += '      Visible: ' + str(panel.isVisible) + '\n'
                msg += '      Index: ' + str(panel.index) + '\n'
                result += msg
                result = get_controls(panel.controls, 2, full_report, result)

            result += '\n\n** Workspaces  (' + str(ui.workspaces.count) + ')____\n'
            for workspace in ui.workspaces:
                if workspace.productType == '':
                    continue
                try:
                    if workspace.toolbarTabs is not None:
                        msg = '   ' + workspace.id + ' (' + str(workspace.toolbarTabs.count) + ')____\n'
                        result += msg
                        for tab in workspace.toolbarTabs:
                            msg = '      ' + tab.id + ' (' + str(tab.toolbarPanels.count) + ')____\n'
                            result += msg
                            for panel in tab.toolbarPanels:
                                msg = '            ' + panel.id + '\n'
                                result += msg
                except:
                    msg = '      failed' + '\n'

                output = open(filename, 'w')
                output.writelines(result)
                output.close()

                ui.messageBox('File written to "' + filename + '"')
        except:
            if ui:
                ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))


# Function used to recursively traverse the controls.
def get_controls(controls, level, fullReport, result):
    for control in controls:
        if control.objectType == adsk.core.SeparatorControl.classType():
            msg = ((level * 3) * ' ') + '-Separator-\n'
            msg += (((level + 1) * 3) * ' ') + 'Control ID: ' + control.id + '\n'
            msg += (((level + 1) * 3) * ' ') + 'isVisible: ' + str(control.isVisible) + '\n'
            msg += (((level + 1) * 3) * ' ') + 'index: ' + str(control.index) + '\n'
            result += msg
        else:
            if control.objectType == adsk.core.CommandControl.classType():
                msg = ((level * 3) * ' ') + 'Command Control____\n'
                msg += (((level + 1) * 3) * ' ') + 'Control ID: ' + control.id + '\n'
                msg += (((level + 1) * 3) * ' ') + 'isVisible: ' + str(control.isVisible) + '\n'
                msg += (((level + 1) * 3) * ' ') + 'index: ' + str(control.index) + '\n'

                if fullReport:
                    try:
                        msg += (((level + 1) * 3) * ' ') + 'isPromoted: ' + str(control.isPromoted) + '\n'
                        msg += (((level + 1) * 3) * ' ') + 'isPromotedByDefault: ' + str(
                            control.isPromotedByDefault) + '\n'
                    except:
                        # Failed to get isPromoted so do nothing.
                        pass

                    msg += (((level + 1) * 3) * ' ') + 'Command Definition____\n'
                    try:
                        commandDef = control.commandDefinition

                        if commandDef:
                            msg += (((level + 2) * 3) * ' ') + 'Definition ID: ' + control.commandDefinition.id + '\n'

                            msg += (((level + 2) * 3) * ' ') + 'Control Definition____\n'

                            controlDef = commandDef.controlDefinition
                            msg += (((level + 3) * 3) * ' ') + 'Name: ' + controlDef.name + '\n'
                            msg += (((level + 3) * 3) * ' ') + 'isEnabled: ' + str(controlDef.isEnabled) + '\n'
                            msg += (((level + 3) * 3) * ' ') + 'isVisible: ' + str(controlDef.isVisible) + '\n'

                            if controlDef.objectType == adsk.core.ButtonControlDefinition.classType():
                                msg += (((level + 3) * 3) * ' ') + 'Type: ButtonControlDefinition\n'
                            elif controlDef.objectType == adsk.core.CheckBoxControlDefinition.classType():
                                msg += (((level + 3) * 3) * ' ') + 'Type: CheckBoxControlDefinition\n'
                                msg += (((level + 3) * 3) * ' ') + 'isChecked: ' + str(controlDef.isChecked) + '\n'
                            elif controlDef.objectType == adsk.core.ListControlDefinition.classType():
                                msg += (((level + 3) * 3) * ' ') + 'Type: ListControlDefinition\n'
                                if controlDef.listControlDisplayType == adsk.core.ListControlDisplayTypes.CheckBoxListType:
                                    displayType = 'Check box list'
                                elif controlDef.listControlDisplayType == adsk.core.ListControlDisplayTypes.RadioButtonlistType:
                                    displayType = 'Radio button list'
                                elif controlDef.listControlDisplayType == adsk.core.ListControlDisplayTypes.StandardListType:
                                    displayType = 'Standard list'
                                msg += (((level + 3) * 3) * ' ') + 'Displayed as: ' + displayType + '\n'
                                msg += (((level + 3) * 3) * ' ') + 'lastSelected: ' + str(
                                    controlDef.lastSelected.name) + '\n'
                                msg += (((level + 3) * 3) * ' ') + 'List Items\n'
                                for listItem in controlDef.listItems:
                                    if listItem.isSeparator:
                                        msg += (((level + 4) * 3) * ' ') + '-Separator-\n'
                                    else:
                                        msg += (((
                                                             level + 4) * 3) * ' ') + 'name: ' + listItem.name + ', isSelected: ' + str(
                                            listItem.isSelected) + '\n'

                            else:
                                msg += (((level + 3) * 3) * ' ') + '**Unexpected type of control definition.\n'
                    except:
                        msg += (((level + 2) * 3) * ' ') + 'Unable to get the associated CommandDefinition.\n'

                result += msg
            elif control.objectType == adsk.core.DropDownControl.classType():
                msg = ((level * 3) * ' ') + 'Drop Down Control (' + str(control.controls.count) + ')____\n'
                msg += (((level + 1) * 3) * ' ') + 'ID: ' + control.id + '\n'
                result += msg
                result = get_controls(control.controls, level + 1, fullReport, result)
            elif control.objectType == adsk.core.SplitButtonControl.classType():
                msg = ((level * 3) * ' ') + 'Split Button Control____\n'
                msg += (((level + 1) * 3) * ' ') + 'ID: ' + control.id + '\n'
                msg += (((level + 1) * 3) * ' ') + 'isVisible: ' + str(control.isVisible) + '\n'

                if fullReport:
                    msg += (((level + 1) * 3) * ' ') + 'isLastUsedShown: ' + str(control.isLastUsedShown) + '\n'
                    msg += (((level + 1) * 3) * ' ') + 'default Command: ' + control.defaultCommandDefinition.id + '\n'

                    msg += (((level + 1) * 3) * ' ') + '+ Additional associated controls:\n'
                    try:
                        for cmdDef in control.additionalDefinitions:
                            msg += (((level + 2) * 3) * ' ') + cmdDef.id + '\n'
                    except:
                        result += msg
                        continue
                result += msg
            else:
                ctype = control.objectType.split('::')[2]
                msg = ((level * 3) * ' ') + '*****' + control.id + ', type: ' + ctype + ', visible: ' + str(
                    control.isVisible) + '\n'
                result += msg

    return result
