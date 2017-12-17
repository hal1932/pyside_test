# encoding: utf-8
from pyside import *
import trace


class PropertyChangedEventArgs(object):

    @property
    def name(self): return self.__name

    @property
    def value(self): return self.__value

    def __init__(self, name, value):
        self.__name = name
        self.__value = value


class BindableBase(QObject):

    property_changed = Signal(QObject, PropertyChangedEventArgs)

    def __init__(self, parent=None):
        super(BindableBase, self).__init__(parent)

    def set_property(self, name, value):
        old_value = getattr(self, name)
        if old_value == value:
            return False

        self.__dict__[name] = value
        self._on_property_changed(name)
        return True


    def on_property_changed(self, name, new_value=None):
        prop = getattr(self, name)
        e = PropertyChangedEventArgs(name, prop.value)
        print 'property changed: {}, {}'.format(name, prop.value)
        self.property_changed.emit(self, e)


class ObservableProperty(QObject):

    value_changed = Signal(object)

    @property
    def value(self): return self.__value

    @value.setter
    def value(self, new_value):
        if new_value == self.value:
            return
        self.__value = new_value
        self.parent().on_property_changed(self.__name, new_value)
        self.value_changed.emit(new_value)

    def __init__(self, name, parent):
        super(ObservableProperty, self).__init__(parent=parent)
        self.__name = name
        self.__value = None
