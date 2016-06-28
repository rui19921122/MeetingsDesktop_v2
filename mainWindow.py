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

from data import DataStore
from HttpRequest.request import Fetch
from PyQt5.QtNetwork import QNetworkRequest


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.store = DataStore()
        self.settings = self.store.settings
        self.data = self.store.data
        self.session = requests.session()
        fetch = Fetch(parent=self)
        self.store.fetch = fetch
        self.fetch = fetch
        self.setWindowTitle("芜湖东站点名会系统")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(r':/FigureImage/resource/icon.png'),
                       QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.setWindowIcon(icon)
        self.setup_dock_widget()
        self.warn = WarnWidget.Warning(parent=self.dockWidget)
        self.dockWidget.setWidget(self.warn)
        login_form = LoginForm(parent=self)
        self.setCentralWidget(login_form)

    def setup_dock_widget(self):
        self.dockWidget = QtWidgets.QDockWidget(self)
        self.dockWidget.setFloating(True)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.dockWidget)
        self.dockWidget.setWindowOpacity(0.7)
        self.dockWidget.setTitleBarWidget(QtWidgets.QWidget())
        self.dockWidget.hide()

    def start_call_over(self):
        response = self.session.post(url=url_resolve.parse_url('api/call_over/begin-call-over/'))
        assert isinstance(response, requests.Response)
        if response.status_code == 200:
            self.call_over_data = response.json()
            # todo 新开线程处理后台传
            print(self.call_over_data)
            self.setCentralWidget(DisplayMainLogic.DisplayMainLogic(mainWindow=self))
        else:
            message = QtWidgets.QMessageBox.warning(self, "错误", str(response.json()), QtWidgets.QMessageBox.Yes)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1082, 731)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate

    def closeEvent(self, event, *args, **kwargs):
        if self.can_close:
            event.accept()
        else:
            QtWidgets.QMessageBox.warning(self, "警告", "后台正在处理数据，请勿关闭")
            event.ignore()
    def nativeEvent(self, eventType, message):
        print(eventType)
        print(message)
        return False, 0



if __name__ == '__main__':
    try:
        app = QtWidgets.QApplication(sys.argv)
        qss = open('./OSXLite.qss').read()
        app.setStyleSheet(qss)
        mainWindow = MainWindow()
        # eventFilter = CustomQAbstractNativeEventFilter()
        # mainWindow.installEventFilter(eventFilter)
        mainWindow.show()
        mainWindow.showMaximized()
        sys.exit(app.exec_())
    except BaseException:
        raise BaseException
