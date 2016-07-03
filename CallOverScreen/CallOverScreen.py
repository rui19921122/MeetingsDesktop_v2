# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'CallOverScreen.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(966, 688)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.TitleLabel = QtWidgets.QLabel(Form)
        self.TitleLabel.setMinimumSize(QtCore.QSize(0, 100))
        self.TitleLabel.setMaximumSize(QtCore.QSize(16777215, 100))
        self.TitleLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.TitleLabel.setObjectName("TitleLabel")
        self.verticalLayout_2.addWidget(self.TitleLabel)
        self.DisplayLayout = QtWidgets.QStackedWidget(Form)
        self.DisplayLayout.setObjectName("DisplayLayout")
        self.verticalLayout_2.addWidget(self.DisplayLayout)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.Back = QtWidgets.QPushButton(Form)
        self.Back.setMinimumSize(QtCore.QSize(150, 0))
        self.Back.setObjectName("Back")
        self.horizontalLayout_3.addWidget(self.Back)
        self.Forward_2 = QtWidgets.QPushButton(Form)
        self.Forward_2.setMinimumSize(QtCore.QSize(150, 0))
        self.Forward_2.setObjectName("Forward_2")
        self.horizontalLayout_3.addWidget(self.Forward_2)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.horizontalLayout.setStretch(0, 10)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.TitleLabel.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:18pt;\">芜湖东站点名会</span></p></body></html>"))
        self.Back.setText(_translate("Form", "前一条"))
        self.Forward_2.setText(_translate("Form", "后一条"))

