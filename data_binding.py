# encoding: utf-8
from pyside import *
from bindable_base import *
from binding import *


class WindowViewModel(BindableBase):

    def __init__(self):
        super(WindowViewModel, self).__init__(None)
        self.label = ObservableProperty('label', self)
        self.edit = ObservableProperty('edit', self)
        self.edit1 = ObservableProperty('edit1', self)

        def edit_value_changed(value):
            print value
        self.edit.value_changed.connect(edit_value_changed)

        def edit1_value_changed(value):
            print value
        self.edit1.value_changed.connect(edit1_value_changed)


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

        edit1 = QLineEdit(self)
        w.layout().addWidget(edit1)

        self.__bindings.add_one_way('label', lambda x: label.setText(x))
        self.__bindings.add_two_way('edit', lambda x: edit.setText(x), lambda: edit.text(), edit.textChanged)
        self.__bindings.add_one_way_to_source('edit1', lambda: edit1.text(), edit1.textChanged)

        return self


if __name__ == '__main__':
    app = QApplication([])
    window = Window().setup_ui()
    window.data_context = WindowViewModel()

    window.data_context.label.value = str(0)

    def update_text():
        import time
        while True:
            time.sleep(1)
            value = window.data_context.label.value
            value = int(value) + 1
            window.data_context.label.value = str(value)
            window.data_context.edit.value = str(value)

    import threading
    t = threading.Thread(target=update_text)
    t.start()

    window.show()

    app.exec_()
