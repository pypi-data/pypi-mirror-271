from nicegui import ui
from ..type_view import TypeView


class AssetView(TypeView):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def asset(self):
        return self.component

    @ui.refreshable
    def ui_content(self):
        with ui.card().classes('w-full h-full').props('color="blue-800" keep-color') as self.card:
            with ui.item().classes('w-full h-full'):
                with ui.item_section():
                    self.checkbox = ui.checkbox()
                with ui.item_section():
                    ui.label(self.asset.name)
                with ui.item_section():
                    ui.label(str(self.asset.file_size / 1024))
                with ui.item_section():
                    ui.label(str(self.asset.last_modified))
                with ui.item_section():
                    dl_button = ui.button(icon='download', on_click=self.download).classes('q-ml-auto')

    def download(self, event):
        ui.download(f'assets/{self.asset.name}')
