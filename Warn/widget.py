from PyQt5 import QtWidgets, QtCore, QtGui
from functools import partial


class Warning(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Warning, self).__init__()
        self.parent = parent
        self.pal = QtGui.QPalette()
        self.pal.setColor(QtGui.QPalette.Background, QtGui.QColor(200, 253, 123, 100))
        self.setPalette(self.pal)
        self.main_layout = QtWidgets.QVBoxLayout()
        self.button = QtWidgets.QPushButton('add')
        self.main_layout.addWidget(self.button)
        self.setLayout(self.main_layout)

    def add_warn(self, message):
        label = QtWidgets.QLabel()
        label.setText(message)
        label.setPalette(self.pal)
        label.setAlignment(QtCore.Qt.AlignCenter)
        self.main_layout.addWidget(label)
        timer = QtCore.QTimer(self.parent)
        timer.start(5000)
        timer.timeout.connect(partial(self.remove_warn, timer=timer, label=label))

    def remove_warn(self, timer: QtCore.QTimer, label: QtWidgets.QLabel):
        timer.stop()
        label.setParent(None)
        label.destroy()
