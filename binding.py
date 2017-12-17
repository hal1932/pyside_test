# encoding: utf-8
from pyside import *


class Binding(object):

    MODE_ONEWAY = 0
    MODE_TWOWAY = 1
    MODE_ONEWAYTOSOURCE = 2

    @property
    def mode(self): return self.__mode

    @property
    def setter(self): return self.__setter

    @property
    def getter(self): return self.__getter

    def __init__(self, mode, setter, getter):
        self.__mode = mode
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

    def add_one_way(self, name, setter):
        """
        ViewModel -> View
        """
        self.__bindings[name] = Binding(Binding.MODE_ONEWAY, setter, None)

    def add_two_way(self, name, setter, getter, on_changed):
        """
        ViewModel <-> View
        """
        self.__bindings[name] = Binding(Binding.MODE_TWOWAY, setter, getter)
        on_changed.connect(lambda: self.__on_property_changed(name))

    def add_one_way_to_source(self, name, getter, on_changed):
        """
        ViewModel <- View
        """
        self.__bindings[name] = Binding(Binding.MODE_ONEWAYTOSOURCE, None, getter)
        on_changed.connect(lambda: self.__on_property_changed(name))

    def __on_data_context_property_changed(self, sender, e):
        if e.name not in self.__bindings:
            return

        binding = self.__bindings[e.name]
        if binding.mode == Binding.MODE_ONEWAYTOSOURCE:
            return

        binding.setter(e.value)

    def __on_property_changed(self, name):
        if name not in self.__bindings:
            return

        binding = self.__bindings[name]
        if binding.mode == Binding.MODE_ONEWAY:
            return

        if name not in self.__data_context.__dict__:
            return

        prop = self.__data_context.__dict__[name]
        prop.value = binding.getter()
