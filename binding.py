# encoding: utf-8
from pyside import *


class Binding(object):

    @property
    def setter(self): return self.__setter

    @property
    def getter(self): return self.__getter

    def __init__(self, setter, getter):
        self.__setter = setter
        self.__getter = getter


class BoundPropertyUpdater(object):

    @property
    def data_context(self): return self.__data_context

    @data_context.setter
    def data_context(self, value):
        if self.__data_context is not None:
            self.__data_context.property_changed.disconnect(self.__on_data_context_property_changed)

        self.__data_context = value
        if self.__data_context is not None:
            self.__data_context.property_changed.connect(self.__on_data_context_property_changed)

    def __init__(self):
        self.__data_context = None
        self.__bindings = {}

    def add_binding(self, name, setter, getter, on_changed=None):
        self.__bindings[name] = Binding(setter, getter)
        if on_changed is not None:
            on_changed.connect(lambda: self.__on_property_changed(name))

    def __on_data_context_property_changed(self, sender, e):
        if e.name not in self.__bindings:
            return
        self.__bindings[e.name].setter(e.value)

    def __on_property_changed(self, name):
        if name not in self.__bindings:
            return

        if name not in type(self.__data_context).__dict__:
            return

        value = self.__bindings[name].getter()

        prop = type(self.__data_context).__dict__[name]
        prop.__set__(self.__data_context, value)
