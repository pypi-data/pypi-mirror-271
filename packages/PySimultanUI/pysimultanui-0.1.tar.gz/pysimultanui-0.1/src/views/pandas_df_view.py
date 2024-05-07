import pandas as pd
from typing import Type
from nicegui import Client, app, ui, events
from .type_view import TypeView
from .type_view_manager import TypeViewManager

from .. import core
from ..core.edit_dialog import ContentEditDialog

from SIMULTAN.Data.MultiValues import (SimMultiValueField3D, SimMultiValueField3DParameterSource, SimMultiValueBigTable,
                                       SimMultiValueBigTableHeader, SimMultiValueBigTableParameterSource)

from PySimultan2.multi_values import simultan_multi_value_big_table_to_pandas


class DataFrameView(TypeView):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    @property
    def component(self):
        return self._component

    @component.setter
    def component(self, value):
        self._component = value

    @ui.refreshable
    def ui_content(self):
        with ui.card().classes(f"{self.colors['item']} w-full h-full") as self.card:
            self.card.on('click', self.show_details)
            with ui.row().classes('bg-stone-100 w-full') as self.row:
                self.row.on('click', self.show_details)
                self.checkbox = ui.checkbox(on_change=self.select)
                with ui.row():
                    ui.label('Name:').props('font-weight=bold')
                    ui.input(value=self.component.Name).bind_value(self.component, 'Name')
                    ui.label('ID:').props('font-weight=bold')
                    with ui.row():
                        with ui.row():
                            ui.label(f'{self.component.Id.GlobalId.ToString()}')
                        with ui.row():
                            ui.label(f'{self.component.Id.LocalId}')

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
                    ui.label(f'{str(self.component.Id)}')

                ui.separator()

                table = ui.table.from_pandas(simultan_multi_value_big_table_to_pandas(self.component)
                                             ).classes('w-full h-full')

                with table.add_slot('top-left'):
                    def toggle() -> None:
                        table.toggle_fullscreen()
                        button.props('icon=fullscreen_exit' if table.is_fullscreen else 'icon=fullscreen')

                    button = ui.button('Toggle fullscreen', icon='fullscreen', on_click=toggle).props('flat')


class DataFrameManager(TypeViewManager):

    cls: pd.DataFrame = pd.DataFrame
    item_view_cls: Type[TypeView] = DataFrameView
    item_view_name = 'Dataframes'

    def button_create_ui_content(self):
        ui.button('Create new DataFrame', on_click=self.create_new_item, icon='add')

    def update_items(self) -> list[SimMultiValueBigTable]:
        if self.data_model is None:
            return []

        return [x for x in self.data_model.value_fields if type(x) == SimMultiValueBigTable]

    @ui.refreshable
    def add_item_to_view(self,
                         item: any,
                         raw_val=None):

        if isinstance(item, SimMultiValueBigTable):
            val_source = item
        elif isinstance(item, pd.DataFrame):
            val_source: SimMultiValueBigTable = raw_val.ValueSource.ValueField

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
