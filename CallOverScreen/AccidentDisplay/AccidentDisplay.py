# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AccidentDisplay.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(586, 472)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.TextLabel = QtWidgets.QLabel(Form)
        self.TextLabel.setTextFormat(QtCore.Qt.RichText)
        self.TextLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.TextLabel.setObjectName("TextLabel")
        self.verticalLayout.addWidget(self.TextLabel)
        self.Content = QtWidgets.QLabel(Form)
        self.Content.setAlignment(QtCore.Qt.AlignCenter)
        self.Content.setObjectName("Content")
        self.verticalLayout.addWidget(self.Content)
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.listWidget = QtWidgets.QListWidget(Form)
        self.listWidget.setViewMode(QtWidgets.QListView.ListMode)
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout.addWidget(self.listWidget)
        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 10)
        self.verticalLayout.setStretch(2, 1)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.TextLabel.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:18pt;\">TextLabel</span></p></body></html>"))
        self.Content.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:28pt;\">TextLabel</span></p></body></html>"))
        self.label_3.setText(_translate("Form", "附件：(双击可打开链接）"))
        self.listWidget.setSortingEnabled(False)

