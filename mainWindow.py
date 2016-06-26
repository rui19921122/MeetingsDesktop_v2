# -*- coding: utf-8 -*-
import sys
import os

import time

sys.path.append(os.path.abspath('..'))

import requests
from Warn import widget as WarnWidget
from PyQt5 import QtWidgets, QtCore, QtGui

from data import DataStore


class MainWindow(QtWidgets.QMainWindow):
	def __init__(self):
		super(MainWindow, self).__init__()
		self.store = DataStore()
		self.settings = self.store.settings
		self.data = self.store.data
		self.setWindowTitle("芜湖东站点名会系统")
		icon = QtGui.QIcon()
		icon.addPixmap(QtGui.QPixmap(r'..\resource\icon.png'),
					   QtGui.QIcon.Normal,
					   QtGui.QIcon.Off)
		self.setWindowIcon(icon)
		self.warn = WarnWidget.Warning(parent=self.dockWidget)
		self.warn.add_warn('5151')
        self.setup_dock_widget()

	def setup_dock_widget(self):
        self.dockWidget = QtWidgets.QDockWidget(self)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.dockWidget)
        self.dockWidget.setWidget(self.warn)
        self.dockWidget.setFeatures(
            QtWidgets.QDockWidget.NoDockWidgetFeatures
        )
        self.dockWidget.setTitleBarWidget(QtWidgets.QWidget())


	def login_commit(self, username, password, boolean):
		response = self.session.post(url=url_resolve.parse_url('api/auth/login/'),
									 data={'email': '',
										   'password': password,
										   'username': username
										   })
		""":type :requests.Response """
		if response.status_code == 200:
			_get_detail_response = self.session.get(url=url_resolve.parse_url('api/menu/get-user-detail'))
			self.username = _get_detail_response.json().get('name')
			self.department = _get_detail_response.json().get('department')
			if boolean:
				self.setCentralWidget(
					FigureCollectionLogic.FigureCollectionLogic(main_window=self, session=self.session))
			else:
				self.setCentralWidget(DisplayLogic.DisplayStarting(session=self.session, main_window=self))
		else:
			message = QtWidgets.QMessageBox.warning(self, "错误", str(response.json()), QtWidgets.QMessageBox.Yes)

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


if __name__ == '__main__':
	app = QtWidgets.QApplication(sys.argv)
	qss = open('./OSXLite.qss').read()
	app.setStyleSheet(qss)
	mainWindow = MainWindow()
	mainWindow.show()
	mainWindow.showMaximized()
	sys.exit(app.exec_())
