# encoding: utf-8
from pyside import *
from bindable_base import *
from binding import *


class WindowViewModel(BindableBase):

    @property
    def label(self): return self.__label

    @label.setter
    def label(self, value):
        self._set_property('label', value)

    @property
    def edit(self): return self.__edit

    @edit.setter
    def edit(self, value):
        self._set_property('edit', value)

    def __init__(self):
        super(WindowViewModel, self).__init__(None)
        self.__label = u'aaa'
        self.__edit = u'aaa'


class Window(QMainWindow):

    @property
    def data_context(self): return self.__bindings.data_context

    @data_context.setter
    def data_context(self, value): self.__bindings.data_context = value

    def __init__(self):
        super(Window, self).__init__(None)
        self.__bindings = BoundPropertyUpdater()

    def setup_ui(self):
        w = QWidget(self)
        self.setCentralWidget(w)

        w.setLayout(QVBoxLayout())

        label = QLabel(self)
        w.layout().addWidget(label)

        edit = QLineEdit(self)
        w.layout().addWidget(edit)

        self.__bindings.add_binding('label', lambda x: label.setText(x), lambda: label.text())
        self.__bindings.add_binding('edit', lambda x: edit.setText(x), lambda: label.text(), edit.textChanged)

        return self



if __name__ == '__main__':
    app = QApplication([])
    window = Window().setup_ui()
    window.data_context = WindowViewModel()

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
