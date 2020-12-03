import os

import adsk.core
import traceback


try:
    from . import config
    from .apper import apper

    # For UI Command and Selection Stream
    from .commands.CommandStreamEvents import CommandStreamEvent, SelectionStreamEvent
    from .commands.CommandStreamPaletteCommand import CommandStreamPaletteShow

    # from .commands.AuthCommand import AuthPaletteShow
    # from .commands import ForgeCommands
    # from .commands.DataCommands import DataInfoCommand

    from .commands import AttributeCommands
    from .commands import AssemblyContextCommands
    from .commands import NewNumbers
    from .commands import CleanUpDocuments
    from .commands import tab_panels_dump
    from .commands import Dump_UI

    # ************Samples**************
    # Basic Fusion 360 Command Base samples
    from .commands.SampleCommand2 import SampleCommand2

    # Palette Command Base samples
    from .commands.SamplePaletteCommand import SamplePaletteSendCommand, SamplePaletteShowCommand

    # Various Application event samples
    from .commands.SampleCustomEvent import SampleCustomEvent1
    from .commands.SampleDocumentEvents import SampleDocumentEvent1, SampleDocumentEvent2
    from .commands.SampleWorkspaceEvents import SampleWorkspaceEvent1
    from .commands.SampleWebRequestEvent import SampleWebRequestOpened
    from .commands.SampleActiveSelectionEvents import SampleActiveSelectionEvent1

    # Create our addin definition object
    my_addin = apper.FusionApp(config.app_name, config.company_name, False)
    my_addin.root_path = config.app_path

    # Creates a basic Hello World message box on execute
    my_addin.add_command(
        'All Attributes',
        AttributeCommands.AllAttributesCommand,
        {
            'cmd_description': 'Display all attributes in a design',
            'cmd_id': 'all_attributes_cmd',
            'workspace': 'FusionSolidEnvironment',
            'toolbar_panel_id': 'Attributes',
            'cmd_resources': 'command_icons',
            'command_visible': True,
            'command_promoted': True,
        }
    )

    my_addin.add_command(
        'Selection Attributes',
        AttributeCommands.AttributeSelectionCommand,
        {
            'cmd_description': 'Display all attributes associated with some selected object',
            'cmd_id': 'selection_attributes_cmd',
            'workspace': 'FusionSolidEnvironment',
            'toolbar_panel_id': 'Attributes',
            'cmd_resources': 'command_icons',
            'command_visible': True,
            'command_promoted': True,
        }
    )

    my_addin.add_command(
        'Add Attribute',
        AttributeCommands.AddAttributeCommand,
        {
            'cmd_description': 'Select an object and manually add an attribute',
            'cmd_id': 'add_attributes_cmd',
            'workspace': 'FusionSolidEnvironment',
            'toolbar_panel_id': 'Attributes',
            'cmd_resources': 'command_icons',
            'command_visible': True,
            'command_promoted': True,
        }
    )

    my_addin.add_command(
        'Single Joint Info',
        AssemblyContextCommands.JointInfoCommand,
        {
            'cmd_description': 'Select a joint and see its information',
            'cmd_id': 'joint_info_cmd',
            'workspace': 'FusionSolidEnvironment',
            'toolbar_panel_id': 'Assembly',
            'cmd_resources': 'command_icons',
            'command_visible': True,
            'command_promoted': False,
        }
    )

    # TODO something, wrong, think need to put occurrence in top level context or joint's context to get proper result.
    # my_addin.add_command(
    #     'Component Joint Info',
    #     AssemblyContextCommands.AssemblyJointCommand,
    #     {
    #         'cmd_description': 'Select a component and see information about its joints',
    #         'cmd_id': 'component_joint_info_cmd',
    #         'workspace': 'FusionSolidEnvironment',
    #         'toolbar_panel_id': 'Assembly',
    #         'cmd_resources': 'command_icons',
    #         'command_visible': True,
    #         'command_promoted': False,
    #     }
    # )

    my_addin.add_command(
        'Assembly Context Info',
        AssemblyContextCommands.AssemblyContextCommand,
        {
            'cmd_description': 'Select an occurrence (component) and see information about its assembly context',
            'cmd_id': 'assembly_context_info_cmd',
            'workspace': 'FusionSolidEnvironment',
            'toolbar_panel_id': 'Assembly',
            'cmd_resources': 'command_icons',
            'command_visible': True,
            'command_promoted': True,
        }
    )

    my_addin.add_command(
        'Fake MetaData Document',
        NewNumbers.NewNumbers,
        {
            'cmd_description': 'Sets Description and assigns a sequence of part numbers starting with a random number',
            'cmd_id': 'clean_this_document_cmd',
            'workspace': 'FusionSolidEnvironment',
            'toolbar_panel_id': 'MetaData',
            'cmd_resources': 'command_icons',
            'command_visible': True,
            'command_promoted': True,
        }
    )

    # my_addin.add_command(
    #     'Cleanup Project',
    #     CleanUpDocuments.CleanUpDocuments,
    #     {
    #         'cmd_description': 'Updates metadata for all files in active project',
    #         'cmd_id': 'clean_all_documents_cmd',
    #         'workspace': 'FusionSolidEnvironment',
    #         'toolbar_panel_id': 'MetaData',
    #         'cmd_resources': 'command_icons',
    #         'command_visible': True,
    #         'command_promoted': False,
    #     }
    # )

    my_addin.add_command(
        'Write UI',
        Dump_UI.DumpUICommand,
        {
            'cmd_description': 'Write UI definitions to file',
            'cmd_id': 'dump_ui_cmd',
            'workspace': 'FusionSolidEnvironment',
            'toolbar_panel_id': 'UI',
            'cmd_resources': 'command_icons',
            'command_visible': True,
            'command_promoted': False,
        }
    )

    my_addin.add_command(
        'Write Panels',
        tab_panels_dump.DumpWorkspacePanels,
        {
            'cmd_description': 'Write just workspace and panel definitions to file',
            'cmd_id': 'dump_workspace_panels_cmd',
            'workspace': 'FusionSolidEnvironment',
            'toolbar_panel_id': 'UI',
            'cmd_resources': 'command_icons',
            'command_visible': True,
            'command_promoted': False,
        }
    )

    # my_addin.add_command(
    #     'Get Data Info',
    #     DataInfoCommand,
    #     {
    #         'cmd_description': 'Display Data Info for Current File',
    #         'cmd_id': 'data_cmd_1',
    #         'workspace': 'FusionSolidEnvironment',
    #         'toolbar_panel_id': 'Data',
    #         'cmd_resources': 'command_icons',
    #         'command_visible': True,
    #         'command_promoted': True,
    #     }
    # )

    # # General command showing inputs and user interaction
    # my_addin.add_command(
    #     'Sample Command 2',
    #     SampleCommand2,
    #     {
    #         'cmd_description': 'A simple example of a Fusion 360 Command with various inputs',
    #         'cmd_id': 'sample_cmd_2',
    #         'workspace': 'FusionSolidEnvironment',
    #         'toolbar_panel_id': 'Commands',
    #         'cmd_resources': 'command_icons',
    #         'command_visible': True,
    #         'command_promoted': False,
    #     }
    # )

    # Create an html palette to as an alternative UI
    my_addin.add_command(
        'Show Command Stream',
        CommandStreamPaletteShow,
        {
            'cmd_description': 'Show details about commands being executed in the UI',
            'cmd_id': 'command_stream_id',
            'workspace': 'FusionSolidEnvironment',
            'toolbar_panel_id': 'UI',
            'cmd_resources': 'palette_icons',
            'command_visible': True,
            'command_promoted': True,
            'palette_id': config.command_stream_palette_id,
            'palette_name': 'f360dever Command Stream',
            'palette_is_local': True,
            'palette_html_file_url': os.path.join('commands', 'palette_html', 'command_stream.html'),
            'palette_use_new_browser': True,
            'palette_is_visible': True,
            'palette_show_close_button': True,
            'palette_is_resizable': True,
            'palette_width': 500,
            'palette_height': 600,
        }
    )
    #
    # # Create an html palette to as an alternative UI
    # my_addin.add_command(
    #     'Get Authorization',
    #     AuthPaletteShow,
    #     {
    #         'cmd_description': 'Get Authorization for use with Forge',
    #         'cmd_id': 'auth_cmd_id',
    #         'workspace': 'FusionSolidEnvironment',
    #         'toolbar_panel_id': 'Data',
    #         'cmd_resources': 'forge_icons',
    #         'command_visible': True,
    #         'command_promoted': True,
    #         'palette_id': 'f360dever_auth_palette_id',
    #         'palette_name': 'f360dever Authorization Demo',
    #         'palette_is_local': False,
    #         'palette_html_file_url': config.auth_url,
    #         # 'palette_html_file_url': 'commands/palette_html/localAuth.html',
    #         'palette_use_new_browser': True,
    #         'palette_is_visible': True,
    #         'palette_show_close_button': True,
    #         'palette_is_resizable': True,
    #         'palette_width': 500,
    #         'palette_height': 600,
    #     }
    # )

    # Get Fusion 360 Projects from Forge API
    # my_addin.add_command(
    #     'Forge Projects',
    #     ForgeCommands.ForgeProjectsFromHubCommand,
    #     {
    #         'cmd_description': 'Get Fusion 360 Projects from Forge API',
    #         'cmd_id': 'ForgeProjectsCommand',
    #         'workspace': 'FusionSolidEnvironment',
    #         'toolbar_panel_id': 'Data',
    #         'cmd_resources': 'forge_icons',
    #         'command_visible': True,
    #         'command_promoted': False,
    #     }
    # )

    # my_addin.add_command(
    #     'Forge Folder Contents',
    #     ForgeCommands.ForgeFolderContentsCommand,
    #     {
    #         'cmd_description': "Get Folder Contents of active project's root folder from Forge API",
    #         'cmd_id': 'ForgeFoldersCommand',
    #         'workspace': 'FusionSolidEnvironment',
    #         'toolbar_panel_id': 'Data',
    #         'cmd_resources': 'forge_icons',
    #         'command_visible': True,
    #         'command_promoted': False,
    #     }
    # )

    # my_addin.add_command(
    #     'Forge Item Details',
    #     ForgeCommands.ForgeItemDetailsCommand,
    #     {
    #         'cmd_description': "Get Forge Item Details for active document",
    #         'cmd_id': 'ForgeItemCommand',
    #         'workspace': 'FusionSolidEnvironment',
    #         'toolbar_panel_id': 'Data',
    #         'cmd_resources': 'forge_icons',
    #         'command_visible': True,
    #         'command_promoted': False,
    #     }
    # )

    # my_addin.add_command(
    #     'Forge Version Details',
    #     ForgeCommands.ForgeVersionDetailsCommand,
    #     {
    #         'cmd_description': "Get Forge Version Details for active document",
    #         'cmd_id': 'ForgeVersionCommand',
    #         'workspace': 'FusionSolidEnvironment',
    #         'toolbar_panel_id': 'Data',
    #         'cmd_resources': 'forge_icons',
    #         'command_visible': True,
    #         'command_promoted': False,
    #     }
    # )

    # Send data from Fusion 360 to the palette
    my_addin.add_command(
        'Send Info to Palette',
        SamplePaletteSendCommand,
        {
            'cmd_description': 'Send data from a regular Fusion 360 command to a palette',
            'cmd_id': 'sample_palette_send',
            'workspace': 'FusionSolidEnvironment',
            'toolbar_panel_id': 'Palette',
            'cmd_resources': 'palette_icons',
            'command_visible': True,
            'command_promoted': False,
            'palette_id': 'sample_palette',
        }
    )

    # Create an html palette to as an alternative UI
    my_addin.add_command(
        'Sample Palette',
        CommandStreamPaletteShow,
        {
            'cmd_description': 'Show details about commands being executed in the UI',
            'cmd_id': 'sample_palette_id',
            'workspace': 'FusionSolidEnvironment',
            'toolbar_panel_id': 'Palette',
            'cmd_resources': 'palette_icons',
            'command_visible': True,
            'command_promoted': True,
            'palette_id': config.sample_palette_id,
            'palette_name': 'Sample Palette',
            'palette_is_local': True,
            'palette_html_file_url': os.path.join('commands', 'palette_html', 'f360dever.html'),
            'palette_use_new_browser': True,
            'palette_force_url_reload': True,
            'palette_force_url_home': False,
            'palette_enable_debug': True,
            'palette_is_visible': True,
            'palette_show_close_button': True,
            'palette_is_resizable': True,
            'palette_width': 500,
            'palette_height': 600,
        }
    )

    app = adsk.core.Application.cast(adsk.core.Application.get())
    ui = app.userInterface

    # Uncomment as necessary.  Running all at once can be overwhelming :)
    # my_addin.add_custom_event("f360dever_message_system", SampleCustomEvent1)

    # my_addin.add_document_event("f360dever_open_event", app.documentActivated, SampleDocumentEvent1)
    # my_addin.add_document_event("f360dever_close_event", app.documentClosed, SampleDocumentEvent2)

    # my_addin.add_workspace_event("f360dever_workspace_event", ui.workspaceActivated, SampleWorkspaceEvent1)

    # my_addin.add_web_request_event("f360dever_web_request_event", app.openedFromURL, SampleWebRequestOpened)

    my_addin.add_command_event("f360dever_command_event", ui.commandStarting, CommandStreamEvent)

    my_addin.add_command_event("f360dever_selection_event", ui.activeSelectionChanged, SelectionStreamEvent)

except:
    app = adsk.core.Application.get()
    ui = app.userInterface
    if ui:
        ui.messageBox('Initialization: {}'.format(traceback.format_exc()))

# Set to True to display various useful messages when debugging your app
debug = False


def run(context):
    my_addin.run_app()


def stop(context):
    my_addin.stop_app()
