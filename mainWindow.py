# -*- coding: utf-8 -*-
import ctypes
import sys
import os
import logging
from WindowEventHandler.windowHandler import CustomQAbstractNativeEventFilter
import time

sys.path.append(os.path.abspath('..'))

import requests
from Warn import widget as WarnWidget
from PyQt5 import QtWidgets, QtCore, QtGui
from Login import LoginForm

from data import DataStore, DeviceInfo
from PyQt5.QtNetwork import QNetworkRequest
from DisplayWait import DisplayWorkerForm
from CallOverScreen import CallOverScreenWidget


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.can_close = True
        self.store = DataStore()
        self.settings = self.store.settings
        self.data = self.store.data
        self.device = DeviceInfo()
        self.session = requests.session()
        self.setWindowTitle("芜湖东站点名会系统")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(r':/FigureImage/resource/icon.png'),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.setWindowIcon(icon)
        self.setup_dock_widget()
        self.warn = WarnWidget.Warning(parent=self.dockWidget)
        self.dockWidget.setWidget(self.warn)
        self.login_form = LoginForm(parent=self)
        self.login_form.login_success.connect(self.login_success)
        self.setCentralWidget(self.login_form)
        sys.path.append(os.getcwd())

    def login_success(self):
        self.login_form.close()
        self.display_form = DisplayWorkerForm(parent=self)
        self.display_form._begin_call_over.connect(self.begin_call_over)
        self.setCentralWidget(self.display_form)

    def begin_call_over(self, data):

        self.display_form.close()
        self.call_over_form = CallOverScreenWidget(data=data, parent=self)
        self.setCentralWidget(self.call_over_form)
        self.call_over_form.over.connect(self.call_over_over)

    def call_over_over(self, id):
        self.call_over_form.close()
        from OverCall import OverCallWidget
        self.over_call_widget = OverCallWidget(self, id)
        self.setCentralWidget(self.over_call_widget)

    def setup_dock_widget(self):
        self.dockWidget = QtWidgets.QDockWidget(self)
        self.dockWidget.setFloating(True)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.dockWidget)
        self.dockWidget.setWindowOpacity(0.7)
        self.dockWidget.setTitleBarWidget(QtWidgets.QWidget())
        self.dockWidget.hide()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate

    def closeEvent(self, event, *args, **kwargs):
        if self.can_close:
            event.accept()
        else:
            QtWidgets.QMessageBox.warning(self, "警告", "后台正在处理数据，请勿关闭")
            event.ignore()


if __name__ == '__main__':
    try:
        app = QtWidgets.QApplication(sys.argv)
        qss = open('./OSXLite.qss').read()
        app.setStyleSheet(qss)
        mainWindow = MainWindow()
        mainWindow.show()
        mainWindow.showMaximized()
        sys.exit(app.exec_())
    except SystemExit:
        pass
    except BaseException:
        raise BaseException
