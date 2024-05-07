import numpy as np
import pandas as pd
from typing import Type
from nicegui import Client, app, ui, events
from .type_view import TypeView
from .type_view_manager import TypeViewManager

from .. import core
from ..core.edit_dialog import ContentEditDialog

from SIMULTAN.Data.MultiValues import (SimMultiValueField3D, SimMultiValueField3DParameterSource, SimMultiValueBigTable,
                                       SimMultiValueBigTableHeader, SimMultiValueBigTableParameterSource)

from PySimultan2.multi_values import simultan_multi_value_field_3d_to_numpy


class NDArrayView(TypeView):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.content = kwargs.get('content', None)
        self.array = None
        self.dim_slider = None
        self.table = None

    @ui.refreshable
    def table_ui_content(self):

        if self.array.shape.__len__() > 2:
            disp_array = self.array[int(self.dim_slider.value if self.dim_slider is not None else 0), :, :]
        else:
            disp_array = self.array

        self.table = ui.table.from_pandas(pd.DataFrame(disp_array)
                                          ).classes('w-full h-full')
        with self.table.add_slot('top-left'):
            def toggle() -> None:
                self.table.toggle_fullscreen()
                button.props('icon=fullscreen_exit' if self.table.is_fullscreen else 'icon=fullscreen')

            button = ui.button('Toggle fullscreen', icon='fullscreen', on_click=toggle).props('flat')

    @ui.refreshable
    def ui_content(self):

        with ui.card().classes(f"{self.colors['item']} w-full h-full") as self.card:
            self.card.on('click', self.show_details)
            with ui.row().classes('bg-stone-100 w-full') as self.row:
                self.row.on('click', self.show_details)
                self.checkbox = ui.checkbox(on_change=self.select)
                ui.label(f'{self.component.Id}')
                ui.label(f'{self.component.Name}')

        # with ui.card().classes('w-full h-full').props('color="blue-800" keep-color') as self.card:
        #     with ui.list().classes('w-full h-full'):
        #         with ui.item():
        #             with ui.item_section().classes('max-w-40'):
        #                 self.checkbox = ui.checkbox()
        #             with ui.item_section():
        #                 with ui.item():
        #                     with ui.item_section():
        #                         ui.label(f'ID:').props('font-weight=bold')
        #                     with ui.item_section():
        #                         ui.label(f'{self.component.Id}')
        #                 with ui.item():
        #                     with ui.item_section():
        #                         ui.label(f'Name:').props('font-weight=bold')
        #                     with ui.item_section():
        #                         ui.label(f'{self.component.Name}')

    def show_details(self, *args, **kwargs):
        TypeView.show_details(self)

        core.detail_view.clear()
        with core.detail_view as detail_view:
            with ui.card().classes('w-full h-full'):
                if kwargs.get('previous', None) is not None:
                    with ui.row():
                        ui.button(on_click=lambda e: kwargs.get('previous').__ui_element__.show_details(previous=self),
                                  icon='arrow_back').classes('q-mr-md')

                with ui.row():
                    ui.input(label='Name',
                             value=self.component.Name).classes('w-full h-full').bind_value(self.component,
                                                                                            'Name')
                with ui.row():
                    ui.label('ID:')
                    with ui.row():
                        with ui.row():
                            ui.label(f'{self.component.Id.GlobalId.ToString()}')
                        with ui.row():
                            ui.label(f'{self.component.Id.LocalId}')

                ui.separator()

                self.array = simultan_multi_value_field_3d_to_numpy(self.component)
                self.table_ui_content()

                with ui.card().classes('w-full h-full'):
                    ui.label('Select dimension to display:')
                    self.dim_slider = ui.slider(min=0, max=self.array.shape[0] - 1,
                                                step=1,
                                                value=0,
                                                on_change=self.table_ui_content.refresh)
                    ui.input('dim_slider',
                             value='0').bind_value(self.dim_slider,
                                                   'value',
                                                   forward=lambda x: int(x),
                                                   backward=lambda x: str(x))


class NDArrayManager(TypeViewManager):

    cls: np.ndarray = np.ndarray
    item_view_cls: Type[TypeView] = NDArrayView
    item_view_name = 'ND Arrays'

    def update_items(self) -> list[SimMultiValueField3D]:
        if self.data_model is None:
            return []
        return [x for x in self.data_model.value_fields if type(x) == SimMultiValueField3D]

    def button_create_ui_content(self):
        ui.button('Create new ND-Array', on_click=self.create_new_item, icon='add')

    @ui.refreshable
    def add_item_to_view(self,
                         item: any,
                         raw_val=None):

        if isinstance(item, SimMultiValueField3D):
            val_source = item
        elif isinstance(item, np.ndarray):
            val_source: SimMultiValueField3D = raw_val.ValueSource.ValueField

        if self.items_ui_element is None:
            return

        if val_source not in self.items:
            self.items.append(val_source)
        item_view = self.item_views.get(str(val_source.Id), None)

        if item_view is None:
            item_view = self.item_view_cls(component=val_source,
                                           parent=self)
            self.item_views[str(val_source.Id)] = item_view
            with self.items_ui_element:
                item_view.ui_content()
        else:
            if item_view.card.parent_slot.parent.parent_slot.parent is not self.items_ui_element:
                with self.items_ui_element:
                    item_view.ui_content()
        return item_view
