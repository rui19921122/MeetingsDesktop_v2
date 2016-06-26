from PyQt5 import QtWidgets, QtCore, QtGui
from functools import partial

class Warning(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Warning, self).__init__()
        self.parent = parent
        self.main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.main_layout)
        self.main_layout.setAlignment(QtCore.Qt.AlignTop)
        self.setMaximumWidth(500)
        self.setMinimumHeight(500)
        self.setGeometry(0, 0, 100, 100)

    def add_warn(self, message, type='warn', delay=3):
        self.parent.show()
        label = QtWidgets.QLabel()
        label.setAutoFillBackground(True)
        if type == 'warn':
            color = '#1DFFDF'
        else:
            color = '#1DFFDF'
        label.setStyleSheet('background-color:{};border-radius:10px'.format(color))
        label.setText(message)
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setMaximumHeight(200)
        label.setMinimumHeight(200)
        self.main_layout.addWidget(label)
        timer = QtCore.QTimer(self.parent)
        timer.start(delay * 1000)
        timer.timeout.connect(partial(self.remove_warn, timer=timer, label=label))

    def remove_warn(self, timer: QtCore.QTimer, label: QtWidgets.QLabel):
        timer.stop()
        label.setParent(None)
        label.destroy()
        if self.main_layout.count() == 0:
            self.parent.hide()
