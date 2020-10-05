import adsk.core
import adsk.fusion
import adsk.cam
import requests

# Import the entire apper package
import apper
import config

# Alternatively you can import a specific function or class
from apper import AppObjects

# TODO Switch for production
FORGE_BASE = "https://developer-stg.api.autodesk.com/forge-dm-qa"
# FORGE_BASE = "https://developer.api.autodesk.com"


def get_forge_data(url):
    ao = AppObjects()

    access_token = config.access_token
    headers = {
        'Authorization': f"Bearer {access_token}",
        'Content-Type': 'application/vnd.api+json'
    }

    r = requests.get(FORGE_BASE + url, headers=headers)
    r_json = r.json()

    if r.status_code == 200:
        return r_json

    # TODO deal with expired token
    # elif r.status_code == EXPIRED:
    #     refresh and recall method

    else:
        ao.ui.messageBox(str(r.status_code))
        ao.ui.messageBox(str(r_json))
        return False


class ForgeProjectsFromHubCommand(apper.Fusion360CommandBase):
    def on_create(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs):
        ao = AppObjects()
        hub_id = ao.app.data.activeHub.id
        url = f"/project/v1/hubs/{hub_id}/projects"
        r_json = get_forge_data(url)

        if r_json:
            i = 0
            for project in r_json['data']:
                project_name = project['attributes']['name']
                tb = inputs.addTextBoxCommandInput(f'tb_input_{i}', project_name, project_name, 1, True)
                tb.isFullWidth = True


class ForgeFolderContentsCommand(apper.Fusion360CommandBase):
    def on_create(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs):
        ao = AppObjects()
        folder_id = ao.app.data.activeProject.rootFolder.id
        project_id = ao.app.data.activeProject.id

        url = f"/data/v1/projects/{project_id}/folders/{folder_id}/contents"
        r_json = get_forge_data(url)

        i = 0
        for item in r_json['data']:
            name = item['attributes'].get('name', None)
            if name is None:
                name = item['attributes'].get('displayName', "No Name")
            tb = inputs.addTextBoxCommandInput(f'tb_input_{i}', "Name", name, 1, True)


class ForgeItemDetailsCommand(apper.Fusion360CommandBase):
    def on_create(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs):
        ao = AppObjects()

        if not ao.document.isSaved:
            ao.ui.messageBox("You must save teh active document first")
            command.doExecute(True)

        item_id = ao.document.dataFile.id
        project_id = ao.app.data.activeProject.id

        url = f"/data/v1/projects/{project_id}/items/{item_id}"
        r_json = get_forge_data(url)

        name = r_json['data']['attributes'].get('displayName', "No Name")
        tb1 = inputs.addTextBoxCommandInput(f'tb_input_{i}', "Name", name, 1, True)
        name = r_json['data'].get('type', "No Type")
        tb2 = inputs.addTextBoxCommandInput(f'tb_input_{i}', "Type", name, 1, True)


class ForgeVersionDetailsCommand(apper.Fusion360CommandBase):
    def on_create(self, command: adsk.core.Command, inputs: adsk.core.CommandInputs):
        ao = AppObjects()

        if not ao.document.isSaved:
            ao.ui.messageBox("You must save teh active document first")
            command.doExecute(True)

        version_id = ao.document.dataFile.versionId
        project_id = ao.app.data.activeProject.id

        url = f"/data/v1/projects/{project_id}/versions/{version_id}"
        r_json = get_forge_data(url)

        name = r_json['data']['attributes'].get('displayName', "No Name")
        tb1 = inputs.addTextBoxCommandInput(f'tb_input_{i}', "Name", name, 1, True)
        name = r_json['data'].get('type', "No Type")
        tb2 = inputs.addTextBoxCommandInput(f'tb_input_{i}', "Type", name, 1, True)

