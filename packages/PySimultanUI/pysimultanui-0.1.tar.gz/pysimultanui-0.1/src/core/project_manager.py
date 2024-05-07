import os
import asyncio
from copy import deepcopy
from typing import Optional, Type
from datetime import datetime
from nicegui import app, ui, events
from PySimultan2.data_model import DataModel
from PySimultan2.object_mapper import PythonMapper
from PySimultan2.files import FileInfo
from PySimultan2.geometry.geometry_base import GeometryModel
from PySimultan2 import config as py_simultan_config

from .. import core
from ..views.view_manager import ViewManager
from ..views.asset_view import AssetManager
from ..views.geometry_view import GeometryManager
from ..core.navigation import Navigation
# from ..views.geometry_view.geometry_file_manager import GeometryFileManager
# from ..views.asset_view.asset_manager import AssetManager

from ..app.project import content as project_content

import shutil


project_dir = os.environ.get('PROJECT_DIR', '/simultan_projects')
if not os.path.exists(project_dir):
    os.makedirs(project_dir)

app.add_static_files('/project', project_dir)


class NewProjectDialog(object):

    def __init__(self, *args, **kwargs):
        self.dialog = None
        self.parent = kwargs.get('parent', None)

    def validate_project_name(self, project_name):
        if not self.dialog.project_name_input.value.endswith('.simultan'):
            return "Project name must end with '.simultan'!"

    def ui_content(self):
        with ui.dialog() as dialog, ui.card():
            self.dialog = dialog
            with ui.row():
                project_name_input = ui.input('Project name',
                                              #validation=self.validate_project_name
                                              )
                ui.label('.simultan')

            user_name_input = ui.input('User name',
                                       value='admin',
                                       # validation=self.validate_project_name
                                       )
            password_input = ui.input('Password',
                                      value='admin',
                                      # validation=self.validate_project_name
                                      )

            dialog.project_name_input = project_name_input
            dialog.user_name_input = user_name_input
            dialog.password_input = password_input

            with ui.row():
                create_btn = ui.button('Create', on_click=self.new_project)
                ui.button('Cancel', on_click=dialog.close)

    def new_project(self, e: events.ClickEventArguments):
        self.dialog.close()

        project_path = f'{project_dir}/{self.dialog.project_name_input.value}.simultan'
        data_model = DataModel.create_new_project(project_path=project_path,
                                                  user_name=self.dialog.user_name_input.value,
                                                  password=self.dialog.password_input.value)
        data_model.save()
        data_model.cleanup()
        if isinstance(data_model, DataModel):
            ui.notify(f'Project {self.dialog.project_name_input.value} created!')
            self.parent.project_list.ui_content.refresh()
        else:
            ui.notify(f'Error creating project {self.dialog.project_name_input.value}!')


class ProjectView(object):

    def __init__(self, *args, **kwargs):

        self._selected: bool = False

        self.parent: Optional[ProjectList] = kwargs.get('parent', None)
        self.project: Optional[str] = kwargs.get('project', None)
        self.project_manager: Optional[ProjectManager] = kwargs.get('project_manager', None)

        self.checkbox: Optional[ui.checkbox] = None
        self.card: Optional[ui.item] = None

        self.selected = kwargs.get('selected', False)

    @property
    def selected(self) -> bool:
        return self._selected

    @selected.setter
    def selected(self, value: bool):
        self._selected = value
        self.ui_content.refresh()

    @property
    def size(self):
        return os.path.getsize(f'{project_dir}/{self.project}')

    @property
    def last_modified(self):
        return datetime.fromtimestamp(os.path.getmtime(f'{project_dir}/{self.project}'))

    @property
    def path(self):
        return f'{project_dir}/{self.project}'

    @property
    def project_dict(self):
        return {'size': self.size,
                'last_modified': self.last_modified,
                'path': self.path,
                'project': self.project,
                }

    @ui.refreshable
    def ui_content(self):
        with ui.item() as self.card:
            with ui.item_section():
                ui.label(self.project).classes('text-xl')
            with ui.item_section():
                if self.size < 1024:
                    ui.label(f'Size: {self.size:.2f} B')
                elif self.size < 1024 ** 2:
                    ui.label(f'Size: {self.size / 1024:.2f} kB')
                else:
                    ui.label(f'Size: {self.size / 1024 ** 2:.2f} MB')
            with ui.item_section():
                ui.label(f'Last modified: {self.last_modified}')

            if self.project.endswith('.simultan') and not self.project.startswith('~'):
                if self.selected:
                    with ui.item_section():
                        self.card.classes('bg-blue-5')
                        sel_button = ui.button('Close',
                                               icon='close',
                                               on_click=self.parent.close_project).classes('q-ml-auto')
                        sel_button.project = self
                        sel_button.project_item = self.card
                    with ui.item_section():
                        save_button = ui.button('Save',
                                                icon='save',
                                                on_click=self.parent.save_project).classes('q-ml-auto')
                        save_button.project = self

                else:
                    with ui.item_section():
                        sel_button = ui.button('Open',
                                               icon='file_open',
                                               on_click=self.parent.select_project).classes('q-ml-auto')
                        sel_button.project = self
                        sel_button.project_item = self.card
                    with ui.item_section():
                        dl_button = ui.button(icon='download',
                                              on_click=self.parent.download_project).classes('q-ml-auto')
                        dl_button.project = self

                    with ui.item_section():
                        del_button = ui.button(icon='delete',
                                               on_click=self.parent.delete_project).classes('q-ml-auto')
                        del_button.project = self
            else:
                with ui.item_section():
                    pass
                with ui.item_section():
                    dl_button = ui.button(icon='download',
                                          on_click=self.download_project).classes('q-ml-auto')
                    dl_button.project = self.project_dict
                with ui.item_section():
                    del_button = ui.button(icon='delete',
                                           on_click=self.parent.delete_project).classes('q-ml-auto')
                    del_button.project = self

    def download_project(self, e: events.ClickEventArguments):
        ui.download(f'project/{self.project}')


class ProjectList(object):

    def __init__(self, *args, **kwargs):
        self._projects = None
        self.selected_project = kwargs.get('selected_project', None)
        self.project_manager = kwargs.get('project_manager', None)
        self.project_views = kwargs.get('project_views', {})

        self.file_list = None

    @property
    def projects(self):
        if self._projects is None:
            self.projects = self.refresh_projects()
        return self._projects

    @projects.setter
    def projects(self, value):

        old_set = set(self._projects) if self._projects is not None else set()
        new_set = set(value) if value is not None else set()
        self._projects = value

        common_projects = old_set.intersection(new_set)
        new_projects = new_set.difference(common_projects)
        removed_projects = old_set.difference(common_projects)

        for project in new_projects:
            self.add_project_to_view(project)

        for project in removed_projects:
            if project in self.project_views:
                self.project_views[project].card.parent_slot.parent.remove(self.project_views[project].card)

    def refresh_projects(self):
        return os.listdir(project_dir)

    @property
    def selected_project(self):
        return app.storage.user['selected_project']

    @selected_project.setter
    def selected_project(self, value):
        app.storage.user['selected_project'] = value

    # @ui.refreshable
    # def ui_content(self):
    #     self.project_items = []
    #     with ui.card().classes('w-full h-full overflow-y-auto'):
    #         ui.label('Files:').classes('text-2xl')
    #
    #         projects = {}
    #
    #         with ui.list().classes('w-full h-full'):
    #             for project in os.listdir(project_dir):
    #                 with ui.item() as project_item:
    #                     self.project_items.append(project_item)
    #                     projects[project] = {'size': os.path.getsize(f'{project_dir}/{project}'),
    #                                          'last_modified': datetime.fromtimestamp(os.path.getmtime(f'{project_dir}/{project}')),
    #                                          'path': f'{project_dir}/{project}',
    #                                          'project': project,
    #                                          }
    #                     with ui.item_section():
    #                         ui.label(project)
    #                     with ui.item_section():
    #                         if projects[project]["size"] < 1024:
    #                             ui.label(f'Size: {projects[project]["size"]:.2f} B')
    #                         elif projects[project]["size"] < 1024**2:
    #                             ui.label(f'Size: {projects[project]["size"]/1024:.2f} kB')
    #                         else:
    #                             ui.label(f'Size: {projects[project]["size"]/1024**2:.2f} MB')
    #                     with ui.item_section():
    #                         ui.label(f'Last modified: {projects[project]["last_modified"]}')
    #
    #                     if project.endswith('.simultan') and not project.startswith('~'):
    #                         if self.selected_project is not None and project == self.selected_project['project']:
    #                             with ui.item_section():
    #                                 project_item.classes('bg-blue-10')
    #                                 sel_button = ui.button('Close',
    #                                                        icon='close',
    #                                                        on_click=self.close_project).classes('q-ml-auto')
    #                                 sel_button.project = projects[project]
    #                                 sel_button.project_item = project_item
    #                             with ui.item_section():
    #                                 save_button = ui.button('Save',
    #                                                         icon='save',
    #                                                         on_click=self.save_project).classes('q-ml-auto')
    #                                 save_button.project = projects[project]
    #
    #                         else:
    #                             with ui.item_section():
    #                                 sel_button = ui.button('Open',
    #                                                        icon='file_open',
    #                                                        on_click=self.select_project).classes('q-ml-auto')
    #                                 sel_button.project = projects[project]
    #                                 sel_button.project_item = project_item
    #                             with ui.item_section():
    #                                 dl_button = ui.button(icon='download',
    #                                                       on_click=self.download_project).classes('q-ml-auto')
    #                                 dl_button.project = project
    #
    #                             with ui.item_section():
    #                                 del_button = ui.button(icon='delete',
    #                                                        on_click=self.delete_project).classes('q-ml-auto')
    #                                 del_button.project = projects[project]
    #                     else:
    #                         with ui.item_section():
    #                             pass
    #                         with ui.item_section():
    #                             dl_button = ui.button(icon='download',
    #                                                   on_click=self.download_project).classes('q-ml-auto')
    #                             dl_button.project = project
    #                         with ui.item_section():
    #                             del_button = ui.button(icon='delete',
    #                                                    on_click=self.delete_project).classes('q-ml-auto')
    #                             del_button.project = projects[project]

    @ui.refreshable
    def ui_content(self):
        self.project_views = {}
        ui.label('Files:').classes('text-2xl')
        with ui.list().classes('w-full h-full') as self.file_list:
            for project in os.listdir(project_dir):
                project_view = ProjectView(project=project,
                                           selected=project == self.selected_project,
                                           project_manager=self.project_manager,
                                           parent=self)
                self.project_views[project] = project_view
                project_view.ui_content()

    def add_project_to_view(self, project: str):
        if project not in self.project_views:
            project_view = ProjectView(project=project,
                                       selected=project == self.selected_project,
                                       project_manager=self.project_manager,
                                       parent=self)
            self.project_views[project] = project_view
            with self.file_list:
                project_view.ui_content()

    def select_project(self, e: events.ClickEventArguments):
        self.selected_project = e.sender.project.project
        if self.project_manager is not None:
            self.project_manager.open_project(e)
        self.projects = self.refresh_projects()

    def close_project(self, e: events.ClickEventArguments):
        self.selected_project = None
        self.project_manager.close_project(e)
        self.projects = self.refresh_projects()

    def delete_project(self, e: events.ClickEventArguments):
        if os.path.isfile(e.sender.project.path):
            file = e.sender.project.path
            os.remove(file)
            ui.notify(f"Project {e.sender.project.project} deleted!")
            self.ui_content.refresh()
        elif os.path.isdir(e.sender.project.path):
            shutil.rmtree(e.sender.project.path)
            ui.notify(f"Project {e.sender.project.project} deleted!")
            self.ui_content.refresh()

    def save_project(self, e: events.ClickEventArguments):
        if self.project_manager.data_model is not None:
            self.project_manager.data_model.save()
            ui.notify(f"Project {e.sender.project.project} saved!")
        else:
            ui.notify(f"Project {e.sender.project.project} not saved! No project loaded!")

    def download_project(self, e: events.ClickEventArguments):
        ui.download(f'project/{e.sender.project.project}')


class ProjectManager(object):
    def __init__(self, *args, **kwargs):

        self._data_model: Optional[DataModel, None] = None
        self._view_manager: Optional[ViewManager, None] = None
        self._asset_manager: Optional[AssetManager, None] = None
        self._geometry_manager: Optional[GeometryManager, None] = None

        self._projects = None
        self.project_list = None
        self.mapped_data = None
        self.mapper: Optional[PythonMapper, None] = kwargs.get('mapper', core.mapper)

        self.view_manager = ViewManager(mapper=self.mapper, parent=self)
        self.asset_manager = AssetManager(data_model=self.data_model)
        self.geometry_manager = GeometryManager(mapper=self.mapper,
                                                project_manager=self,
                                                data_model=self.data_model)

        self.navigation = Navigation(view_manager=self.view_manager,
                                     asset_manager=self.asset_manager,
                                     geometry_manager=self.geometry_manager,
                                     )

        self.detail_view = None

        # self.geometry_file_manager = GeometryFileManager()
        # self.asset_manager = AssetManager()
        # FileInfo.__cls_type_view__ = self.asset_manager
        # core.geometry_file_manager = self.geometry_file_manager
        # core.asset_manager = self.asset_manager

    @property
    def data_model(self):
        return self._data_model

    @data_model.setter
    def data_model(self, value):
        self._data_model = value
        core.data_model = value

        if self._data_model is not None:
            app.add_static_files('/assets', self._data_model.project.ProjectUnpackFolder.FullPath)

        for item in [self.view_manager, self.asset_manager, self.geometry_manager, self.navigation]:
            if item is not None:
                item.data_model = value

    @property
    def view_manager(self) -> ViewManager:
        return self._view_manager

    @view_manager.setter
    def view_manager(self, value: Optional[ViewManager]):
        self._view_manager = value
        core.view_manager = value

    @property
    def asset_manager(self):
        return self._asset_manager

    @asset_manager.setter
    def asset_manager(self, value):
        self._asset_manager = value
        core.asset_manager = value

    @property
    def geometry_manager(self):
        return self._geometry_manager

    @geometry_manager.setter
    def geometry_manager(self, value):
        self._geometry_manager = value
        core.geometry_manager = value
        # orig_init = deepcopy(GeometryModel.__init__)
        #
        # def new_init(self, *args, **kwargs):
        #     orig_init(self, *args, **kwargs)
        #     # value.add_item_to_view(self)
        #
        # GeometryModel.__init__ = new_init

    @property
    def projects(self):
        # get list of files in project_dir
        self._projects = os.listdir(project_dir)
        return self._projects

    @property
    def selected_project(self):
        return self.project_list.selected_project

    def upload_project(self,
                       e: events.UploadEventArguments,
                       *args,
                       **kwargs):

        shutil.copyfileobj(e.content, open(f'{project_dir}/{e.name}', 'wb'))
        ui.notify(f'Project {e.name} uploaded!')
        self.project_list.ui_content.refresh()

    async def refresh_all_items(self, e):
        await self.view_manager.refresh_all_items()
        self.asset_manager.update_items_views()
        self.geometry_manager.update_items_views()
        self.navigation.ui_content.refresh()

    def ui_content(self):
        with core.project_tab:
            self.view_manager.ui_content()
            self.asset_manager.ui_content()
            self.geometry_manager.ui_content()
            self.navigation.ui_content()

            with ui.page_sticky(position='bottom-right', x_offset=20, y_offset=20):
                ui.button(on_click=self.refresh_all_items, icon='update').props('fab color=accent')

        self.project_list = ProjectList(project_manager=self,
                                        selected_project=app.storage.user.get('selected_project',
                                                                              None)
                                        )
        self.project_list.ui_content()

        new_project_dialog = NewProjectDialog(parent=self)
        new_project_dialog.ui_content()

        ui.button('New project', on_click=new_project_dialog.dialog.open).classes('max-w-full')

        ui.upload(label='Upload simultan project',
                  on_upload=self.upload_project).on(
            'finish', lambda: ui.notify('Finish!')
        ).classes('max-w-full')

    def open_project(self, e: events.ClickEventArguments):

        n = ui.notification(timeout=None)
        n.spinner = True
        n.message = f'Opening project {e.sender.project.project}'

        project_dict = e.sender.project.project_dict
        new_data_model = DataModel(project_path=project_dict['path'],
                                   user_name='admin',
                                   password='admin')
        self.mapped_data = new_data_model.get_typed_data(self.mapper, create_all=False)
        self.data_model = new_data_model
        py_simultan_config.default_mapper = self.mapper
        py_simultan_config.default_data_model = self.data_model
        e.sender.project.selected = True
        # self.project_list.ui_content.refresh()
        n.message = 'Done!'
        n.spinner = False
        # self.method(*args, **kwargs)
        n.dismiss()

        ui.notify(f'Project loaded with {len(self.mapped_data)} objects!')

    def close_project(self, e):
        if self.data_model is not None:
            self.data_model.cleanup()
        self.mapper.clear()
        self.mapped_data = []
        self.data_model = None
        py_simultan_config.default_data_model = None
        ui.notify('Project closed!')
        # self.project_list.ui_content.refresh()
        e.sender.project.selected = False

        # self.geometry_file_manager.geometry_models = []
        # project_content.refresh()
