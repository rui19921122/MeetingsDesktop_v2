from .LoginForm import Ui_Form
from PyQt5 import QtWidgets, QtCore, QtGui
from Warn import widget


class LoginForm(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super(LoginForm, self).__init__()
        self.setupUi(self)
