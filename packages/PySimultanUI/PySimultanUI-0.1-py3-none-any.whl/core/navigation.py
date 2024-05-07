from typing import Optional, Type
from nicegui import ui

from ..import core
from ..views.type_view_manager import TypeViewManager
from ..views.view_manager import ViewManager


class Navigation(object):
    def __init__(self, *args, **kwargs):

        self._view_manager = None

        self.data_model = kwargs.get('data_model', core.data_model)
        self.navigation_drawer = core.navigation_drawer
        self.view_manager: Optional[Type[ViewManager]] = kwargs.get('view_manager', core.view_manager)
        self.geometry_manager: Optional[Type[TypeViewManager]] = kwargs.get('geometry_manager', core.geometry_manager)
        self.asset_manager: Type[TypeViewManager] = kwargs.get('asset_manager')

    @property
    def view_manager(self):
        return self._view_manager

    @view_manager.setter
    def view_manager(self, value):
        self._view_manager = value

    @property
    def obj_mapper(self) -> core.PythonMapper:
        return self.view_manager.mapper

    @ui.refreshable
    def ui_content(self):
        with self.navigation_drawer:
            with ui.expansion(icon='format_list_bulleted',
                              text=f'Mapped Classes ({len(self.view_manager.cls_views)})').classes('w-full'):

                for cls, cls_view_dict in self.view_manager.cls_views.items():
                    item_view_manager = cls_view_dict.get('item_view_manager', None)
                    if item_view_manager is None:
                        continue
                    else:
                        with ui.row():
                            def add_link(cls, cls_view_dict):
                                taxonomy = cls._taxonomy if hasattr(cls, '_taxonomy') else cls.__name__
                                cls_instances = cls.cls_instances if hasattr(cls, 'cls_instances') else []

                                ui.link(f'{taxonomy} ({len(cls_instances)})',
                                        cls_view_dict['item_view_manager'].expansion
                                        ).bind_text_from(cls,
                                                         'cls_instances'
                                                         , lambda x: f'{cls._taxonomy} ({len(x)})')

                            add_link(cls, cls_view_dict)

            if self.geometry_manager.expansion is not None:
                ui.link('Geometry models', self.geometry_manager.expansion)

            if self.asset_manager.expansion is not None:
                ui.link('Assets', self.asset_manager.expansion)
