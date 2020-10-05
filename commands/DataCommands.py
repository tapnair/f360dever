import adsk.core
import apper
from apper import AppObjects
import base64

LATEST_DEV = True


class DataInfoCommand(apper.Fusion360CommandBase):
    def __init__(self, name: str, options: dict):
        super().__init__(name, options)

        ao = AppObjects()
        self.hub = ao.app.data.activeHub
        self.data_file = ao.document.dataFile

        self.lineage_urn = ''
        self.version_urn = ''
        self.b64_lineage_urn = ''
        self.b64_version_urn = ''

        self.hub_id_name = "YOUR_HUB_ID"
        self.hub_id = "Not Implemented"
        self.hub_id_decoded = "Not Implemented"
        self.hub_name = ''

        self.project_id = "Not Implemented"
        self.project_id_decoded = "Not Implemented"
        self.project_name = ''
        self.folder_id = ''
        self.folder_name = ''

        self.team_url = ''

    def on_execute(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs, args, input_values):
        # ao = AppObjects()
        # ao.ui.messageBox()
        pass

    def on_input_changed(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs,
                         changed_input, input_values):
        if changed_input.id == 'hub_id_name':
            text_box = adsk.core.TextBoxCommandInput.cast(changed_input)
            self.hub_id_name = text_box.text
            self.update_urls(inputs)

    def on_create(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs):
        ao = AppObjects()
        if not ao.document.isSaved:
            ao.ui.messageBox("You must save teh active document first")
            command.doExecute(True)

        command.setDialogInitialSize(800, 800)

        inputs.addTextBoxCommandInput('hub_id_name', 'Your Hub ID: ', self.hub_id_name, 1, False)
        info_box = inputs.addTextBoxCommandInput('hub_id_info_id', 'Hub Info',
                                                 'Note: this is the first part of the url you see in Fusion team\n'
                                                 'Like: https://YOUR_HUB_ID.autodesk360.com/g/projects/.../',
                                                 3, True)
        info_box.isFullWidth = True

        inputs.addTextBoxCommandInput('hub_name', 'Hub Name: ', self.hub_name, 1, True)
        inputs.addTextBoxCommandInput('hub_id', 'Hub ID: ', self.hub_id, 1, True)
        inputs.addTextBoxCommandInput('hub_id_decoded', 'Hub ID Decoded: ', self.hub_id_decoded, 1, True)

        inputs.addTextBoxCommandInput('project_name', 'Project Name: ', self.project_name, 1, True)
        inputs.addTextBoxCommandInput('project_id', 'Project ID: ', self.project_id, 1, True)
        inputs.addTextBoxCommandInput('project_id_decoded', 'Project ID Decoded: ', self.project_id_decoded, 1, True)

        inputs.addTextBoxCommandInput('folder_name', 'Folder Name: ', self.folder_name, 1, True)
        inputs.addTextBoxCommandInput('folder_id', 'Folder ID: ', self.folder_name, 1, True)

        inputs.addTextBoxCommandInput('lineage_urn', 'Lineage URN: ', self.lineage_urn, 1, True)
        inputs.addTextBoxCommandInput('b64_lineage_urn', 'base64 Lineage URN: ', self.b64_lineage_urn, 1, True)

        inputs.addTextBoxCommandInput('version_urn', 'Version URN: ', self.version_urn, 1, True)
        inputs.addTextBoxCommandInput('b64_version_urn', 'base64 Version URN: ', self.b64_version_urn, 1, True)

        inputs.addTextBoxCommandInput('view_url', 'View Url: ', '', 3, True)
        inputs.addTextBoxCommandInput('thumbnail_url', 'Thumbnail Url: ', '', 3, True)
        inputs.addTextBoxCommandInput('open_url', 'Open Url: ', '', 3, True)

        self.update_data()
        self.update_data_inputs(inputs)
        self.update_urls(inputs)

    def update_data_inputs(self, inputs):
        inputs.itemById('hub_name').formattedText = self.hub_name
        inputs.itemById('hub_id').formattedText = self.hub_id
        inputs.itemById('hub_id_decoded').formattedText = self.hub_id_decoded
        inputs.itemById('project_name').formattedText = self.project_name
        inputs.itemById('project_id').formattedText = self.project_id
        inputs.itemById('project_id_decoded').formattedText = self.project_id_decoded
        inputs.itemById('folder_name').formattedText = self.folder_name
        inputs.itemById('folder_id').formattedText = self.folder_id
        inputs.itemById('lineage_urn').formattedText = self.lineage_urn
        inputs.itemById('b64_lineage_urn').formattedText = self.b64_lineage_urn
        inputs.itemById('version_urn').formattedText = self.version_urn
        inputs.itemById('b64_version_urn').formattedText = self.b64_version_urn

    def update_data(self):
        ao = AppObjects()

        self.hub = ao.app.data.activeHub
        self.data_file = ao.document.dataFile

        # Existing Properties
        self.hub_name = self.hub.name
        self.project_name = self.data_file.parentProject.name
        self.folder_name = self.data_file.parentFolder.name
        self.folder_id = self.data_file.parentFolder.id
        self.lineage_urn = self.data_file.id

        if LATEST_DEV:
            self.team_url = 'staging.autodesk360beta'
            self.version_urn = self.data_file.versionId

            # TODO Move after production
            self.hub_id = self.hub.id
            self.hub_id_decoded = b64_url_safe_decode(self.hub_id)

            self.project_id = self.data_file.parentProject.id
            self.project_id_decoded = b64_url_safe_decode(self.project_id)

        else:
            self.team_url = 'autodesk360'
            core_id = self.lineage_urn.split(':')[-1]
            self.version_urn = f"urn:adsk.wipprod:fs.file:vf.{core_id}?version={self.data_file.versionNumber}"

        self.b64_lineage_urn = b64_url_safe_encode(self.lineage_urn)
        self.b64_version_urn = b64_url_safe_encode(self.version_urn)

    def update_urls(self, inputs):
        ao = AppObjects()

        view_url = f"https://{self.hub_id_name}.{self.team_url}.com/g/data/{self.b64_lineage_urn}"

        thumbnail_url = f"https://developer.api.autodesk.com/modelderivative/v2/designdata/" \
                        f"{self.b64_lineage_urn}/thumbnail"

        open_url = f"fusion360://userEmail={ao.app.currentUser.email}&" \
                   f"lineageUrn={self.lineage_urn}&" \
                   f"hubUrl=https://{self.hub_id_name}.{self.team_url}.com&" \
                   f"documentName={self.data_file.name}"

        inputs.itemById('view_url').formattedText = url_of(view_url)
        inputs.itemById('thumbnail_url').formattedText = url_of(thumbnail_url)
        inputs.itemById('open_url').formattedText = url_of(open_url)


def url_of(url: str) -> str:
    return f"<a href={url}>{url}</a>"


def b64_url_safe_encode(string):
    encoded_bytes = base64.urlsafe_b64encode(string.encode("utf-8"))
    encoded_str = str(encoded_bytes, "utf-8")
    return encoded_str.rstrip("=")


def b64_url_safe_decode(string):
    return str(base64.urlsafe_b64decode(string.lstrip('a.')), "utf-8")
    # return string
