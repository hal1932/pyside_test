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

    def _set_property(self, name, value):
        old_value = getattr(self, name)
        if old_value == value:
            return False

        self.__dict__[name] = value
        self._on_property_changed(name)
        return True


    def _on_property_changed(self, name):
        value = getattr(self, name)
        e = PropertyChangedEventArgs(name, value)
        print 'property changed: {}, {}'.format(name, value)
        self.property_changed.emit(self, e)
