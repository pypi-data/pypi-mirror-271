import pandas as pd
import asyncio
import numpy as np
from copy import copy
from nicegui import ui, run
from typing import Optional

from .type_view_manager import TypeViewManager
from .type_view import TypeView
from .. import core
from ..core import PythonMapper

from .mapped_cls.mapped_cls_manager import MappedClsManager
from .mapped_cls.mapped_cls_view import MappedClsView


from .component_list_view.component_list_manager import ComponentListManager
from .component_list_view.component_list_view import ComponentListView

from .component_dict_view import ComponentDictManager, ComponentDictView

from .pandas_df_view import DataFrameView, DataFrameManager
from .numpy_view import NDArrayView, NDArrayManager

from PySimultan2.simultan_object import SimultanObject


class ViewManager(object):

    def __init__(self, *args, **kwargs):

        self._data_model = None

        self.mapper = kwargs.get('mapper', core.mapper)
        self.cls_views: dict[str:TypeViewManager, str:TypeView] = {}
        self.data_model = kwargs.get('data_model', None)
        self.parent = kwargs.get('parent', None)

    def register(self,
                 cls: type,
                 type_view: type[TypeView],
                 item_view_manager: Optional[TypeViewManager] = None,):

        self.cls_views[cls] = {'item_view_manager': item_view_manager, 'type_view': type_view}
        cls.item_view_manager = item_view_manager
        cls.type_view = type_view

    @property
    def data_model(self):
        return self._data_model

    @data_model.setter
    def data_model(self, value):
        self._data_model = value

        for cls, cls_view_dict in self.cls_views.items():
            item_view_manager = cls_view_dict.get('item_view_manager', None)
            if item_view_manager is None:
                continue
            else:
                item_view_manager.data_model = value

    def get_view(self, cls: type):
        return self.cls_views[cls]

    def create_mapped_cls_view_manager(self, taxonomy: str) -> Optional[TypeViewManager]:
        cls = self.mapper.get_mapped_class(taxonomy)

        if self.cls_views.get(cls, None) is None:
            new_tvm = MappedClsManager(mapper=self.mapper)
            new_tvm.cls = self.mapper.get_mapped_class(taxonomy)
            # old__init__ = copy(new_tvm.cls.__init__)
            #
            # def __init__(self, *args, **kwargs):
            #     old__init__(self, *args, **kwargs)
            #     new_tvm.add_item_to_view(self)
            #
            # new_tvm.cls.__init__ = __init__

            new_tvm.item_view_cls = MappedClsView
            new_tvm.item_view_name = taxonomy
            new_tvm.view_manager = self
            self.cls_views[new_tvm.cls] = {'item_view_manager': new_tvm, 'type_view': MappedClsView}

            with core.project_tab:
                new_tvm.ui_content()

        return self.cls_views.get(cls, None)

    @ui.refreshable
    def ui_content(self):

        core.method_mapper.ui_content()

        def add_new_init_method(tvm: TypeViewManager):
            old__init__ = copy(tvm.cls.__init__)

            def __init__(self, *args, **kwargs):
                old__init__(self, *args, **kwargs)
                tvm.add_item_to_view(self)

            tvm.cls.__init__ = __init__

        for taxonomy, cls in self.mapper.registered_classes.items():

            mapped_cls = self.mapper.get_mapped_class(taxonomy)

            if taxonomy == 'ComponentList':
                new_tvm = ComponentListManager(mapper=self.mapper)
                new_tvm.item_view_cls = ComponentListView

            elif taxonomy == 'ComponentDict':
                new_tvm = ComponentDictManager(mapper=self.mapper)
                new_tvm.item_view_cls = ComponentDictView

            elif self.cls_views.get(cls, None) is None:
                new_tvm = MappedClsManager(mapper=self.mapper)
                new_tvm.item_view_cls = MappedClsView

            else:
                new_tvm = self.cls_views.get(cls, None)['item_view_manager']

            if new_tvm is None:
                continue

            new_tvm.cls = mapped_cls
            # add_new_init_method(new_tvm)
            new_tvm.item_view_name = taxonomy
            new_tvm.view_manager = self
            self.cls_views[new_tvm.cls] = {'item_view_manager': new_tvm, 'type_view': new_tvm.item_view_cls}
            new_tvm.ui_content()

        df_manager = DataFrameManager(mapper=self.mapper)
        self.cls_views[pd.DataFrame] = {'item_view_manager': df_manager, 'type_view': DataFrameView}
        df_manager.ui_content()

        np_manager = NDArrayManager(mapper=self.mapper)
        self.cls_views[np.ndarray] = {'item_view_manager': np_manager, 'type_view': NDArrayView}
        np_manager.ui_content()

    async def refresh_all_items(self):

        n = ui.notification(timeout=None)
        n.spinner = True
        n.message = 'Updating all items...'

        for tvm_dict in self.cls_views.values():
            tvm: Optional[TypeViewManager, None] = tvm_dict.get('item_view_manager', None)
            if tvm is None:
                continue
            print(f'Updating items of {tvm.item_view_name}...')
            n.message = f'Updating items of {tvm.item_view_name}...'
            tvm.update_items_views()

        ui.notify('All items updated!', type='positive')

        n.message = 'Updating all items done!'
        n.type = 'positive'
        n.spinner = False
        await asyncio.sleep(2)

        # self.method(*args, **kwargs)
        n.dismiss()
