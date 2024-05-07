from contextlib import contextmanager
from .menue import menu
from nicegui import app, ui, context

from . import home
from . import project

from .. import core


@contextmanager
def frame(navtitle: str):

    """Custom page frame to share the same styling and behavior across all pages"""
    # ui.colors(primary='#da291c', secondary='#941c13', accent='#941c13', positive='#53B689')
    with ui.header().classes('justify-between h-20'):

        # ui.image('web_ui/src/static_files/A1_Digital_identifier_pos_RGB.png').classes('w-32')

        ui.label('PY Simultan').classes('font-bold text-white text-xl')

        # with ui.expansion('Menu', icon='select'):
        with ui.column():
            with ui.tabs() as tabs:
                ui.button('Mapped Classes', icon='checklist_rtl', on_click=lambda: left_drawer.toggle())
                ui.tab('Home', icon='home')
                ui.tab('Project', icon='edit')

                # ui.button(on_click=lambda: (app.storage.user.clear(),
                #                             ui.open('/login')),
                #           icon='logout').props('outline round').classes('text-black')
                #


                # with ui.button(icon='menu'):
                #     with ui.menu() as menu:
                #         ui.menu_item('Logout',
                #                      icon='logout',
                #                      on_click=lambda: (app.storage.user.clear(), ui.open('/login')))

                # ui.space()
                # if app.storage.user.get('username', False):
                #     ui.label(f'{app.storage.user["username"]}').classes('mr-auto text-2xl')

    with ui.left_drawer(bordered=True,
                        top_corner=False,
                        elevated=True,
                        fixed=True,
                        value=False).classes('bg-blue-100') as left_drawer:
        core.navigation_drawer = left_drawer

    # with ui.splitter() as splitter:
    #     with splitter.after:
    #         with ui.right_drawer(bordered=True,
    #                              top_corner=False,
    #                              elevated=True,
    #                              fixed=True,
    #                              value=False).classes('w-full h-full') as detail_drawer:
    #             with ui.card().classes('w-full h-full') as detail_view:
    #                 core.detail_view = detail_view

    with ui.tab_panels(tabs, value='Home').classes('w-full h-full'):
        with ui.tab_panel('Project').classes('w-full h-full') as project_full_tab:
            with ui.splitter(value=60, limits=(10, 90)).classes('w-full h-full') as splitter:
                with splitter.before:
                    context.client.content.classes('h-[95vh]')
                    core.project_tab = ui.scroll_area().classes('w-full h-full')
                with splitter.after:
                    core.detail_view = ui.card().classes('w-full h-full')

        core.home_tab = ui.tab_panel('Home').classes('w-full h-full')

    with core.home_tab:
        home.content()
