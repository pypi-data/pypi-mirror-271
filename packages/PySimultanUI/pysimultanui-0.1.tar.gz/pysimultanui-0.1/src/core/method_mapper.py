import asyncio
from ..config import logger
from .. import core
from nicegui import ui, run
from .tools import ConfirmationDialog


class UnknownClass(object):
    def __init__(self, *args, **kwargs):
        self.cls_name: type = kwargs.get('cls_name', 'Unknown class')
        self.cls: type = kwargs.get('cls', None)
        self.mapper = kwargs.get('mapper', None)


class UnmappedMethod(object):

    def __init__(self, *args, **kwargs):
        self.name: str = kwargs.get('name', 'Unnamed method')
        self.method = kwargs.get('method')
        self.args: list[str] = kwargs.get('args')       # list with description of the arguments
        self.kwargs: dict[str:str] = kwargs.get('kwargs')       # dict with description of the keyword arguments

    def ui_content(self):
        with ui.item().classes('w-full h-full'):
            with ui.item_section():
                ui.label(self.name)
            with ui.item_section():
                ui.button(on_click=self.run, icon='play_circle').classes('q-ml-auto')

    async def run(self, *args, **kwargs):

        if core.project_manager.data_model is None:
            ui.notify('No project loaded!', type='negative')
            return

        n = ui.notification(timeout=None)
        n.spinner = True
        n.message = f'Running method {self.name}'
        try:
            await run.io_bound(self.method, *args, **kwargs)
            n.type = 'positive'
            n.message = f'Successfully ran method {self.name}!'
            n.spinner = False
            await asyncio.sleep(1)
            n.dismiss()
        except Exception as e:
            n.message = f'Error running method {self.name}: {e}'
            n.spinner = False
            await asyncio.sleep(2)
            n.dismiss()


class MappedMethod(object):

    def __init__(self, *args, **kwargs):
        self.name: str = kwargs.get('name', 'Unnamed method')
        self.method = kwargs.get('method')
        self.cls: type = kwargs.get('cls')
        self.args: list[str] = kwargs.get('args')       # list with description of the arguments
        self.kwargs: dict[str:str] = kwargs.get('kwargs')       # dict with description of the keyword arguments

    def ui_content(self):
        with ui.item():
            with ui.item_section():
                ui.label(self.name)
            with ui.item_section():
                ui.button(on_click=self.run, icon='play_circle').classes('q-ml-auto')

    async def run(self, *args, **kwargs):

        if core.project_manager.data_model is None:
            ui.notify('No project loaded!', type='negative')
            return

        selected_instances = [instance for instance in self.cls.cls_instances if instance.__ui_element__.selected]
        if not selected_instances:
            ui.notify('No instances selected!')
            return

        def additional_content_fcn():
            ui.label('Selected instances:')
            for instance in selected_instances:
                with ui.row():
                    ui.label(f'{instance.name} ({instance.id})')

        result = await ConfirmationDialog(f'Are you sure you want to run {self.name}?',
                                          'Yes',
                                          'No',
                                          additional_content_fcn=additional_content_fcn)

        if result == 'Yes':
            n = ui.notification(timeout=None)
            n.spinner = True
            n.message = f'Running method {self.name} of {self.cls.__name__}'
            logger.info(f'Running method {self.name} of {self.cls.__name__}')
            await asyncio.sleep(0.01)
            for instance in selected_instances:
                await run.io_bound(self.method, instance, *args, **kwargs)
                #
                # self.method(instance, *self.args, **self.kwargs)
                instance.__ui_element__.ui_content.refresh()
                # getattr(instance, self.name)(*self.args, **self.kwargs)
                # self.method(instance, *self.args, **self.kwargs)
            ui.notify(f'Method {self.name} run on {len(selected_instances)} instances!')
            n.message = 'Done!'
            n.spinner = False
            await asyncio.sleep(1)
            # self.method(*args, **kwargs)
            n.dismiss()


class MethodMapper(object):

    def __init__(self, *args, **kwargs):

        self.mapped_methods = {}
        self.unmapped_methods = []
        self.mapper = kwargs.get('mapper', None)
        self.card = None

    def register_method(self,
                        method: callable,
                        name='unnamed_method',
                        args=(),
                        kwargs={},
                        cls: type = None):
        if cls is None:
            self.unmapped_methods.append(UnmappedMethod(name=name,
                                                        method=method,
                                                        args=args,
                                                        kwargs=kwargs))
            return

        if cls not in self.mapped_methods:
            self.mapped_methods[cls] = []
        self.mapped_methods[cls].append(MappedMethod(cls=cls,
                                                     name=name,
                                                     method=method,
                                                     args=args,
                                                     kwargs=kwargs))

    @ui.refreshable
    def ui_content(self):
        with ui.card().classes('w-full h-full'):
            with ui.expansion(icon='public',
                              text='Global Methods').classes('w-full h-full') as self.card:
                with ui.list().classes('w-full h-full'):
                    for unmapped_method in self.unmapped_methods:
                        with ui.item().classes('w-full h-full'):
                            unmapped_method.ui_content()

    def resolve_classes(self):

        mapped_methods = self.mapped_methods.copy()

        for cls, methods in self.mapped_methods.items():
            if isinstance(cls, UnknownClass):
                for method in methods:
                    new_cls = self.mapper.mapped_classes.get(method.method.__qualname__.split('.')[-2], None)
                    if new_cls is None:
                        continue
                    method.cls = new_cls
                    if new_cls not in mapped_methods:
                        mapped_methods[new_cls] = []
                    mapped_methods[new_cls].append(method)
                    mapped_methods[cls].remove(method)

        self.mapped_methods = mapped_methods


method_mapper = MethodMapper()


def mapped_method(name=None, *args, **kwargs):

    dat_dict = {}
    dat_dict['name'] = name

    def wrapper(func):
        # vars(sys.modules[func.__module__])[func.__qualname__.split('.')
        method_mapper.register_method(method=func,
                                      name=dat_dict['name'],
                                      args=args,
                                      kwargs=kwargs,
                                      cls=UnknownClass(cls_name=func.__qualname__))
        return func
    return wrapper
