import shutil

from nicegui import ui, events
from . import GeometryView
from PySimultan2.geometry import GeometryModel

from ..type_view_manager import TypeViewManager
from ... import core


try:
    import FreeCAD
    freecad_supported = True

    from ...core.freecad_utils.tools import import_freecad

except ImportError:
    freecad_supported = False


class GeometryManager(TypeViewManager):

    item_view_name = 'Geometry Models'
    item_view_cls = GeometryView
    cls = GeometryModel

    def __init__(self, *args, **kwargs):
        self.mapper = kwargs.get('mapper', core.mapper)
        self.project_manager = kwargs.get('project_manager', core.project_manager)
        super().__init__(*args, **kwargs)

        self.new_model_dialog = None

    def update_items(self) -> list[any]:
        if self.data_model is None:
            return []

        return [GeometryModel(wrapped_object=x,
                              object_mapper=self.mapper,
                              data_model=self.data_model) for x in
                self.data_model.models.values()]

    def button_create_ui_content(self):
        ui.button('Create new', on_click=self.create_new_model)

    @ui.refreshable
    def ui_content(self):

        with ui.expansion(icon='format_list_bulleted',
                          text=f'{self.item_view_name if self.item_view_name is not None else self.cls._taxonomy} '
                               f'({len(self.items)})').classes('w-full h-full') as self.expansion:

            self.expansion.bind_text_from(self,
                                          'items',
                                          lambda x: f'{self.item_view_name} ({len(x)})'
                                          )

            self.methods_ui_content()

            # with ui.expansion(icon='format_list_bulleted', text='Methods').classes('w-full h-full'):
            #     with ui.list().classes('w-full h-full'):
            #         if freecad_supported:
            #             with ui.item().classes('w-full h-full'):
            #                 with ui.item_section().classes('w-full h-full'):
            #                     ui.label('Import from file')
            #                 with ui.item_section().classes('w-full h-full'):
            #                     ui.button('Import', on_click=self.import_from_file).classes('q-ml-auto')

            self.items_ui_element = ui.row().classes('w-full h-full')

            if len(self.items) == 0:
                with self.items_ui_element:
                    ui.label('No items to display')
            else:
                for item in self.items:
                    self.add_item_to_view(item)

            with ui.row().classes('w-full h-full'):
                self.button_create_ui_content()

        # super().ui_content()

    def create_new_model(self):
        def create_new_model_action():
            try:
                new_model = GeometryModel(data_model=core.project_manager.data_model,
                                          name=self.new_model_dialog.project_name.value)
                self._geometry_models = None
                self._geometry_model_views = None
                self.new_model_dialog.close()
                ui.notify('New model created', type='positive')
                self.add_item_to_view(new_model)
            except Exception as e:
                ui.notify(f'Error creating new model: {e}', type='negative')

        with ui.dialog() as self.new_model_dialog, ui.card():
            ui.label('Create new geometry model')
            self.new_model_dialog.project_name = ui.input('Name')
            with ui.row().classes('justify-between'):
                ui.button('Create', on_click=create_new_model_action)
                ui.button('Cancel', on_click=self.new_model_dialog.close)

        self.new_model_dialog.open()

    def import_from_file(self):
        # check if only one model is selected:
        if len(self.selected_items) != 1:
            ui.notify('Please select exactly one model to import to', type='negative')
            return

        # create dialog to upload file
        with ui.dialog() as dialog, ui.card():
            dialog.scale_input = ui.input(label='Scale Model', value='0.001').classes('w-full')

            upload = ui.upload(label='Upload asset',
                               on_upload=lambda e: self.upload_geometry(e, dialog=dialog)).on(
                'finish', lambda: ui.notify('Finish!')
            ).classes('max-w-full')
            upload.scale_input = dialog.scale_input
            ui.button('Cancel', on_click=lambda e: dialog.close()).classes('mt-4')
        dialog.open()

    def upload_geometry(self,
                        e: events.UploadEventArguments,
                        dialog: ui.dialog,
                        *args,
                        **kwargs):

        dialog.close()

        try:
            local_path = f'/tmp/{e.name}'
            shutil.copyfileobj(e.content, open(local_path, 'wb'))
            ui.notify(f'Project {e.name} uploaded!')

            # open file in FreeCAD
            doc = FreeCAD.open(local_path)
            num_created = import_freecad(doc=doc,
                                         geo_model=self.selected_items[0],
                                         data_model=self.data_model,
                                         object_mapper=core.mapper,
                                         scale=float(e.sender.scale_input.value))

            ui.notify(f'Imported {num_created[0]} Vertices, '
                      f'{num_created[1]} Edges, '
                      f'{num_created[2]} EdgeLoops, '
                      f'{num_created[3]} Faces, '
                      f'{num_created[4]} Volumes.', type='positive')

            # create new geometry model
            self.selected_items[0].__ui_element__.ui_content.refresh()
        except Exception as e:
            ui.notify(f'Error uploading file: {e}', type='negative')

    def methods_ui_content(self):
        with ui.expansion(icon='code', text='Methods').classes('w-full h-full bg-stone-300'):
            with ui.list().classes('w-full h-full'):
                if freecad_supported:
                    with ui.row().classes('w-full h-full'):
                        ui.label('Import from file')
                        ui.button('Import', on_click=self.import_from_file).classes('q-ml-auto')
