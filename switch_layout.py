# encoding: utf-8
from PySide.QtCore import *
from PySide.QtGui import *


def box(cls, *items):
    layout = cls()
    for item in items:
        if isinstance(item, QWidget):
            layout.addWidget(item)
        elif isinstance(item, QLayout):
            layout.addLayout(item)
    return layout

def hbox(*items): return box(QHBoxLayout, *items)
def vbox(*items): return box(QVBoxLayout, *items)

def group(*items):
    group = QGroupBox()
    group.setLayout(vbox(*items))
    return group

def button(label, clicked=None):
    item = QPushButton()
    item.setText(label)
    if clicked is not None:
        item.clicked.connect(clicked)
    return item


class Window(QMainWindow):

    def __init__(self):
        super(Window, self).__init__(parent=None)

    def setup_ui(self):
        w = QWidget()
        w.setLayout(vbox(
            hbox(
                button(u'vbox', lambda: self.__switch_to(vbox)),
                button(u'hbox', lambda: self.__switch_to(hbox))
            ),
            vbox()
        ))
        self.setCentralWidget(w)

        self.__add_items(w.layout().itemAt(1))

        return self

    def __add_items(self, layout):
        for i in xrange(3):
            layout.addWidget(group(
                button(str(i)),
                hbox(*[button('{}-{}'.format(i, j)) for j in xrange(3)])
            ))

    def __switch_to(self, factory):
        target_layout = self.centralWidget().layout().itemAt(1)

        new_layout = factory()

        '''
        while target_layout.count() > 0:
            item = target_layout.takeAt(0)
            if item.widget() is not None:
                new_layout.addWidget(item.widget())
            elif item.layout() is not None:
                new_layout.addLayout(item.layout())
        target_layout.deleteLater()
        '''

        self.__add_items(new_layout)

        queue = [target_layout]

        while len(queue) > 0:
            layout = queue.pop(0)
            layout.deleteLater()

            while layout.count() > 0:
                item = layout.takeAt(0)
                if item.widget() is not None:
                    item.widget().deleteLater()
                if item.layout() is not None:
                    queue.append(item.layout())

        target_layout.parent().addLayout(new_layout)


if __name__ == '__main__':
    app = QApplication([])
    window = Window().setup_ui()
    window.show()
    app.exec_()
