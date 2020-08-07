import adsk.core
import traceback

from.startup import setup_app, cleanup_app, get_app_path
setup_app(__file__)

# TODO add command stream with parent control info (panel, tab, workspace, etc)

try:
    import config
    import apper

    # For UI Command and Selection Stream
    from .commands.CommandStreamEvents import CommandStreamEvent, SelectionStreamEvent

    # f360 Dever Commands
    from .commands.SamplePaletteCommand import CommandStreamPaletteShow
    from .commands import AttributeCommands
    from .commands import AssemblyContextCommands
    from .commands import NewNumbers
    from .commands import CleanUpDocuments
    from .commands import tab_panels_dump
    from .commands import Dump_UI

    # ************Samples**************
    # Basic Fusion 360 Command Base samples
    from .commands.SampleCommand1 import SampleCommand1
    from .commands.SampleCommand2 import SampleCommand2

    # Palette Command Base samples
    from .commands.SamplePaletteCommand import SamplePaletteSendCommand

    # Various Application event samples
    from .commands.SampleCustomEvent import SampleCustomEvent1
    from .commands.SampleDocumentEvents import SampleDocumentEvent1, SampleDocumentEvent2
    from .commands.SampleWorkspaceEvents import SampleWorkspaceEvent1
    from .commands.SampleWebRequestEvent import SampleWebRequestOpened
    from .commands.SampleActiveSelectionEvents import SampleActiveSelectionEvent1

# Create our addin definition object
    my_addin = apper.FusionApp(config.app_name, config.company_name, False)
    my_addin.root_path = get_app_path(__file__)

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



    #
    #
    # my_addin.add_command(
    #     'Sample Command 1',
    #     SampleCommand1,
    #     {
    #         'cmd_description': 'Hello World!',
    #         'cmd_id': 'sample_cmd_1',
    #         'workspace': 'FusionSolidEnvironment',
    #         'toolbar_panel_id': 'Commands',
    #         'cmd_resources': 'command_icons',
    #         'command_visible': True,
    #         'command_promoted': False,
    #     }
    # )
    #
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
        'Show Commands',
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
            'palette_html_file_url': 'commands/palette_html/command_stream.html',
            'palette_use_new_browser': True,
            'palette_is_visible': True,
            'palette_show_close_button': True,
            'palette_is_resizable': True,
            'palette_width': 500,
            'palette_height': 600,
        }
    )

    # # Send data from Fusion 360 to the palette
    # my_addin.add_command(
    #     'Send Info to Palette',
    #     SamplePaletteSendCommand,
    #     {
    #         'cmd_description': 'Send data from a regular Fusion 360 command to a palette',
    #         'cmd_id': 'sample_palette_send',
    #         'workspace': 'FusionSolidEnvironment',
    #         'toolbar_panel_id': 'Palette',
    #         'cmd_resources': 'palette_icons',
    #         'command_visible': True,
    #         'command_promoted': False,
    #         'palette_id': 'sample_palette',
    #     }
    # )

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
    cleanup_app(__file__)
