import adsk.core
import apper
from apper import AppObjects
import base64


class DataInfoCommand(apper.Fusion360CommandBase):
    def __init__(self, name: str, options: dict):
        super().__init__(name, options)

        ao = AppObjects()
        self.hub = ao.app.data.activeHub
        self.data_file = ao.document.dataFile

        self.lineage_urn = ''
        self.version_urn = ''
        self.encoded_lineage_urn = ''
        self.encoded_version_urn = ''

        self.hub_id = "YOUR_HUB_ID"

    def on_execute(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs, args, input_values):
        # ao = AppObjects()
        # ao.ui.messageBox()
        pass

    def on_input_changed(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs,
                         changed_input, input_values):
        if changed_input.id == 'hub_id_input_id':
            text_box = adsk.core.TextBoxCommandInput.cast(changed_input)
            self.hub_id = text_box.text
            self.update_urls(inputs)

    def on_create(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs):
        command.setDialogInitialSize(800, 800)

        self.update_data()

        inputs.addTextBoxCommandInput('hub_id_input_id', 'Your Hub ID: ', self.hub_id, 1, False)
        info_box = inputs.addTextBoxCommandInput('hub_id_info_id', 'Hub Info',
                                                 'Note: this is the first part of the url you see in Fusion team\n'
                                                 'Like: https://YOUR_HUB_ID.autodesk360.com/g/projects/.../',
                                                 3, True)
        info_box.isFullWidth = True
        inputs.addTextBoxCommandInput('hub_name_input_id', 'Hub Name: ', self.hub.name, 1, True)
        # inputs.addTextBoxCommandInput('hub_type_input_id', 'Hub Type: ', hub.hubType.name, 1, True)

        inputs.addTextBoxCommandInput('project_name_input_id', 'Project Name: ',
                                      self.data_file.parentProject.name, 1, True)
        # inputs.addTextBoxCommandInput('project_id_input_id', 'Project ID: ', data_file.parentProject.id, 1, True)
        inputs.addTextBoxCommandInput('folder_name_input_id', 'Folder Name: ',
                                      self.data_file.parentFolder.name, 1, True)
        inputs.addTextBoxCommandInput('folder_id_input_id', 'Folder ID: ',
                                      self.data_file.parentFolder.id, 1, True)

        inputs.addTextBoxCommandInput('Lineage_input_id', 'Lineage URN: ', self.lineage_urn, 1, True)
        inputs.addTextBoxCommandInput('base64_lineage_input_id', 'base64 Lineage URN: ',
                                      str(self.encoded_lineage_urn), 1, True)
        inputs.addTextBoxCommandInput('version_input_id', 'Version URN: ', self.version_urn, 1, True)
        inputs.addTextBoxCommandInput('base64_version_input_id', 'base64 Version URN: ',
                                      str(self.encoded_version_urn), 1, True)

        inputs.addTextBoxCommandInput('view_url_id', 'View Url: ', '', 3, True)
        inputs.addTextBoxCommandInput('thumbnail_url_id', 'Thumbnail Url: ', '', 3, True)
        inputs.addTextBoxCommandInput('open_url_id', 'Open Url: ', '', 3, True)

        self.update_urls(inputs)

    def update_data(self):
        ao = AppObjects()

        self.hub = ao.app.data.activeHub
        self.data_file = ao.document.dataFile

        self.lineage_urn = self.data_file.id
        core_id = self.lineage_urn.split(':')[-1]
        self.version_urn = f"urn:adsk.wipprod:fs.file:vf.{core_id}?version={self.data_file.versionNumber}"
        self.encoded_lineage_urn = b64_url_safe_encode(self.lineage_urn)
        self.encoded_version_urn = b64_url_safe_encode(self.version_urn)

    def update_urls(self, inputs):
        ao = AppObjects()

        view_url = f"https://{self.hub_id}.autodesk360.com/g/data/{self.encoded_lineage_urn}"

        thumbnail_url = f"https://developer.api.autodesk.com/modelderivative/v2/designdata/" \
                        f"{self.encoded_version_urn}/thumbnail"

        open_url = f"fusion360://userEmail={ao.app.currentUser.email}&" \
                   f"lineageUrn={self.lineage_urn}&" \
                   f"hubUrl=https://{self.hub_id}.autodesk360.com&" \
                   f"documentName={self.data_file.name}"

        inputs.itemById('view_url_id').formattedText = url_of(view_url)
        inputs.itemById('thumbnail_url_id').formattedText = url_of(thumbnail_url)
        inputs.itemById('open_url_id').formattedText = url_of(open_url)


def url_of(url: str) -> str:
    return f"<a href={url}>{url}</a>"


def b64_url_safe_encode(string):
    encoded_bytes = base64.urlsafe_b64encode(string.encode("utf-8"))
    encoded_str = str(encoded_bytes, "utf-8")
    return encoded_str.rstrip("=")
