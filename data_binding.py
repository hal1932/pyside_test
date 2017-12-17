# encoding: utf-8
from PySide.QtCore import *
from PySide.QtGui import *


class WindowViewModel(QObject):

    property_changed = Signal(QObject, object)

    @property
    def label(self): return self.__label

    @label.setter
    def label(self, value):
        if value != self.__label:
            old_value = self.__label
            self.__label = value
            self.on_property_changed('label', old_value)

    @property
    def edit(self): return self.__edit

    @edit.setter
    def edit(self, value):
        if value != self.edit:
            old_value = self.__edit
            self.__edit = value
            self.on_property_changed('edit', old_value)

    def __init__(self):
        super(WindowViewModel, self).__init__(None)
        self.__label = u'aaa'
        self.__edit = u'aaa'

    def on_property_changed(self, name, old_value):
        new_value = getattr(self, name)
        print 'property changed: {}, {} -> {}'.format(name, old_value, new_value)
        self.property_changed.emit(self, (name, new_value))


class Window(QMainWindow):

    @property
    def data_context(self): return self.__data_context

    def __init__(self):
        super(Window, self).__init__(None)
        self.__data_context = WindowViewModel()
        self.__data_context.property_changed.connect(self.__on_data_context_property_changed)
        self.__bindings = {}

    def setup_ui(self):
        w = QWidget(self)
        self.setCentralWidget(w)

        w.setLayout(QVBoxLayout())

        label = QLabel(self)
        w.layout().addWidget(label)

        edit = QLineEdit(self)
        w.layout().addWidget(edit)

        self.__bindings['label'] = {
            'setter': lambda x: label.setText(x),
            'getter': lambda: label.text()
        }
        self.__bindings['edit'] = {
            'setter': lambda x: edit.setText(x),
            'getter': lambda: edit.text(),
        }
        # edit.textChanged[str].connect(lambda x: self.__on_property_changed('edit', x))
        edit.textChanged.connect(lambda: self.__on_property_changed('edit'))

        return self

    def __on_data_context_property_changed(self, sender, data):
        name, value = data
        if name not in self.__bindings:
            return
        self.__bindings[name]['setter'](value)

    def __on_property_changed(self, name):
        if name not in self.__bindings:
            return

        if name not in type(self.__data_context).__dict__:
            return

        value = self.__bindings[name]['getter']()

        prop = type(self.__data_context).__dict__[name]
        prop.__set__(self.__data_context, value)



if __name__ == '__main__':
    app = QApplication([])
    window = Window().setup_ui()

    window.data_context.label = str(0)

    def update_text():
        import time
        while True:
            time.sleep(1)
            value = window.data_context.label
            value = int(value) + 1
            window.data_context.label = str(value)
            window.data_context.edit = str(value)

    import threading
    t = threading.Thread(target=update_text)
    t.start()

    window.show()

    app.exec_()
