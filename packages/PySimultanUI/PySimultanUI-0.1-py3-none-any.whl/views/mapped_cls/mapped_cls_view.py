from nicegui import ui
from numpy import ndarray
from pandas import DataFrame

from ..type_view import TypeView
from nicegui import ui, events

from ... import core
from ...core.edit_dialog import ContentEditDialog
from PySimultan2.simultan_object import SimultanObject

from ..parameter_view import ParameterView


class ContentItemView(object):
    def __init__(self, *args, **kwargs):
        self.component: SimultanObject = kwargs.get('component')
        self.parent = kwargs.get('parent')
        self.content = kwargs.get('content')

    @property
    def view_manager(self):
        return self.parent.view_manager

    @ui.refreshable
    def ui_content(self):
        with ui.item().classes('w-full h-full'):
            with ui.item_section():
                ui.label(f'{self.content.name}:')

            val = getattr(self.component, self.content.property_name)
            if isinstance(val, SimultanObject):
                ui_simultan_object_ref(val, self)
            elif isinstance(val, (int, float, str)):
                with ui.item_section():
                    raw_val = self.component.get_raw_attr(self.content.property_name)
                    ParameterView(component=val,
                                  raw_val=raw_val,
                                  content=self.content,
                                  parent=self.parent, taxonomy=self.content).ui_content()

            elif isinstance(val, (ndarray, DataFrame)):
                ui_ndarray_ref(val, self)
            else:
                if val is None:
                    with ui.item_section():
                        ui.label('None')
                with ui.item_section():
                    if hasattr(val, 'name'):
                        ui.label(f'{val.name}:')
                    else:
                        ui.label('No Name')
                with ui.item_section():
                    if hasattr(val, 'id'):
                        ui.label(f'{val.id}:')
                    else:
                        ui.label('No ID')
                with ui.item_section():
                    button = ui.button(on_click=self.edit,
                                       icon='edit').classes('q-ml-auto')
                    button.item = val
                    button.content = self.content

    def edit(self, event):
        edit_dialog = ContentEditDialog(component=event.sender.item,
                                        parent=self.parent,
                                        content=event.sender.content)
        edit_dialog.create_edit_dialog()


def ui_simultan_object_ref(val: SimultanObject,
                           parent: ContentItemView):
    if val.__ui_element__ is None:
        cls_view = parent.view_manager.cls_views.get(val.__class__, None)[
            'item_view_manager'] if parent.view_manager.cls_views.get(val.__class__,
                                                                    None) is not None else None
        if cls_view is None:
            cls_view = parent.view_manager.create_mapped_cls_view_manager(taxonomy=val.__class__._taxonomy)[
                'item_view_manager']
            if cls_view is None:
                ui.label(f'No View for this class: {val.__class__}')
                return
        try:
            cls_view.add_item_to_view(val)
        except KeyError:
            with ui.item_section():
                ui.label(f'No View for this class: {val.__class__}')
    if val.__ui_element__ is None:
        ui.label(f'No View for this object: {str(val), val.__class__}')
        return

    with ui.item_section():
        if val.__ui_element__ is not None:
            ui.label(val.name)
    with ui.item_section():
        ui.button(on_click=lambda e: val.__ui_element__.show_details(previous=parent.component),
                  icon='launch').classes('q-ml-auto')
    with ui.item_section():
        with ui.row():
            ui.label(f'{val.id.GlobalId.ToString()}')
        with ui.row():
            ui.label(f'{val.id.LocalId}')
    with ui.item_section():
        edit_btn = ui.button(on_click=parent.edit, icon='edit').classes('q-ml-auto')
        edit_btn.item = val
        edit_btn.content = parent.content


def ui_ndarray_ref(val: (ndarray, DataFrame),
                   parent: ContentItemView):
    raw_val = parent.component.get_raw_attr(parent.content.property_name)

    def get_ui_element():
        ui_element = parent.view_manager.cls_views[val.__class__]['item_view_manager'].item_views.get(
            str(raw_val.ValueSource.ValueField.Id), None)
        return ui_element

    ui_element = get_ui_element()

    if ui_element is None:
        parent.view_manager.cls_views[val.__class__]['item_view_manager'].add_item_to_view(val, raw_val)
    ui_element = get_ui_element()

    with ui.item_section():
        ui.label(raw_val.ValueSource.ValueField.Name)
    with ui.item_section():
        ui.button(on_click=lambda e: ui_element.show_details(previous=parent.component),
                  icon='launch').classes('q-ml-auto')
    with ui.item_section():
        ui.label(f'{raw_val.ValueSource.ValueField.Id}')
    with ui.item_section():
        edit_btn = ui.button(on_click=parent.edit, icon='edit').classes('q-ml-auto')
        edit_btn.item = val
        edit_btn.content = parent.content


class ContentView(object):

    def __init__(self, *args, **kwargs):
        self.component: SimultanObject = kwargs.get('component')
        self.parent = kwargs.get('parent')
        self.card = None
        self.row = None

        self.content_item_views: dict[str: ContentItemView] = {}

    @property
    def view_manager(self):
        return self.parent.view_manager

    @ui.refreshable
    def ui_content(self):
        with ui.expansion(icon='format_list_bulleted', text='Content', value=True).classes('w-full h-full') as exp:
            with ui.list().classes('w-full h-full'):
                for content in self.component._taxonomy_map.content:
                    if self.content_item_views.get(content.property_name) is None:
                        self.content_item_views[content.property_name] = ContentItemView(component=self.component,
                                                                                         parent=self.parent,
                                                                                         content=content)
                    self.content_item_views[content.property_name].ui_content()
                    ui.separator()


class MappedClsView(TypeView):

    colors = {'item': 'bg-stone-100',
              'cls_color': 'bg-stone-300',
              'selected': 'bg-blue-200'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def view_manager(self):
        return self.parent.view_manager

    @ui.refreshable
    def ui_content(self):
        # with ui.list().classes('w-full h-full').props('bordered separator'):
        #     with ui.item(on_click=self.show_details).classes('w-full h-full') as self.card:
        #         with ui.item_section().classes('q-ml-auto'):
        #             self.checkbox = ui.checkbox().classes('q-ml-auto')
        #         with ui.item_section().classes('w-full h-full'):
        #             ui.input(label='Name', value=self.component.name).bind_value(self.component, 'name')
        #         with ui.item_section().classes('w-full h-full'):
        #             ui.label(f'{str(self.component.id)}')

        with ui.card().classes(f"{self.colors['item']} w-full h-full") as self.card:
            self.card.on('click', self.show_details)
            with ui.row().classes(f"{self.colors['item']} w-full") as self.row:
                self.row.on('click', self.show_details)
                self.checkbox = ui.checkbox(on_change=self.select)
                ui.input(label='Name', value=self.component.name).bind_value(self.component, 'name')
                with ui.row():
                    with ui.row():
                        ui.label(f'{self.component.id.GlobalId.ToString()}')
                    with ui.row():
                        ui.label(f'{self.component.id.LocalId}')

                # with ui.item_section():
                #     ui.button(on_click=self.show_details, icon='launch').classes('q-ml-auto')
            # self.content_view.ui_content()

    def show_details(self, *args, **kwargs):
        TypeView.show_details(self)
        core.detail_view.clear()
        with core.detail_view as detail_view:
            if kwargs.get('previous', None) is not None:
                with ui.row():
                    ui.button(on_click=lambda e: kwargs.get('previous').__ui_element__.show_details(previous=self),
                              icon='arrow_back').classes('q-mr-md')

            with ui.card().classes('w-full h-full'):
                with ui.item().classes('w-full h-full'):
                    with ui.item_section():
                        ui.input(label='Name', value=self.component.name).bind_value(self.component, 'name')
                    with ui.item_section():
                        ui.label(f'{str(self.component.id)}')
                content_view = ContentView(component=self.component, parent=self)
                content_view.ui_content()
