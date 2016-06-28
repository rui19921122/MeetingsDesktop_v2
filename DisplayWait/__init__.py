from .Display import Ui_DisplayWorker
from PyQt5 import QtWidgets, QtCore, QtGui, QtNetwork,QtMultimedia
from Warn import widget
from mainWindow import MainWindow
from HttpRequest.requests import HttpRequest


class DisplayWorkerForm(QtWidgets.QWidget, Ui_DisplayWorker):
    def __init__(self, parent: MainWindow):
        super(DisplayWorkerForm, self).__init__()
        self.setupUi(self)
        self.parent = parent


