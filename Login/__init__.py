from .LoginForm import Ui_Form
from PyQt5 import QtWidgets, QtCore, QtGui, QtNetwork
from Warn import widget
from mainWindow import MainWindow
from HttpRequest.requests import HttpRequest
from DisplayWait import DisplayWorkerForm


class LoginForm(QtWidgets.QWidget, Ui_Form):
    login_success = QtCore.pyqtSignal()
    def __init__(self, parent: MainWindow):
        super(LoginForm, self).__init__()
        self.parent = parent
        self.setupUi(self)
        # self.LoginButton.setDisabled(True)
        self.FigureButton.setDisabled(True)
        self.LoginButton.clicked.connect(self.HandleLoginButtonClicked)
        self.password.textChanged.connect(self.handle_password_change)
        self.FigureButton.setDisabled(True)
        self.LoginButton.setDisabled(True)

    def handle_password_change(self):
        length = len(self.password.text())
        if length < 3:
            self.LoginButton.setDisabled(True)
            self.FigureButton.setDisabled(True)
        else:
            self.LoginButton.setDisabled(False)
            self.FigureButton.setDisabled(False)

    def HandleLoginButtonClicked(self):
        username = self.username.text()
        password = self.password.text()
        if len(username) < 1:
            self.parent.warn.add_warn('请输入用户名')
            self.username.setText('')
            self.password.setText('')
        else:
            thread = HttpRequest(parent=self.parent, url='api/v2/auth/login/', method='post',
                                 data={'username': username,
                                       'password': password})
            thread.failed.connect(lambda message: self.parent.warn.add_warn(message))
            thread.success.connect(lambda message: self.login_success.emit())
            thread.start()
            # self.parent.fetch.post('/api/v2/auth/login/', data={'username': username, 'password': password})

    def handle_reply(self, data):
        print(data)

