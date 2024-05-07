import shutil
from nicegui import ui, events
from . import AssetView
from PySimultan2.files import FileInfo, create_asset_from_file

from ..type_view_manager import TypeViewManager
from ... import core


class AssetManager(TypeViewManager):

    item_view_name = 'Assets'
    item_view_cls = AssetView
    cls = FileInfo

    def __init__(self, *args, **kwargs):
        self.mapper = kwargs.get('mapper', core.mapper)
        self.project_manager = kwargs.get('project_manager', core.project_manager)
        super().__init__(*args, **kwargs)

    def update_items(self) -> list[any]:
        if self.data_model is None:
            return []
        assets = self.data_model.project_data_manager.AssetManager.Resources
        return [FileInfo(resource_entry=asset) for asset in assets]

    def button_create_ui_content(self):
        ui.button('Upload new Asset', on_click=self.create_new_item)

    def create_new_item(self, event):
        if self.data_model is None:
            ui.notify('No data model selected! Please select a data model first.')
            return

        with ui.dialog() as dialog, ui.card():
            ui.upload(label='Upload asset',
                      on_upload=self.upload_project).on(
                'finish', lambda: ui.notify('Finish!')
            ).classes('max-w-full')
            ui.button('Cancel', on_click=lambda e: dialog.close()).classes('mt-4')

        dialog.open()

    def upload_project(self,
                       e: events.UploadEventArguments,
                       *args,
                       **kwargs):
        local_path = f'/tmp/{e.name}'
        shutil.copyfileobj(e.content, open(local_path, 'wb'))
        ui.notify(f'Project {e.name} uploaded!')
        new_fi = FileInfo(file_path=local_path)
        new_asset = create_asset_from_file(new_fi,
                                           data_model=self.data_model,
                                           tag=None)
        self.add_item_to_view(FileInfo(resource_entry=new_asset,
                                       data_model=self.data_model))
