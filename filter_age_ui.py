# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'filter_age_ui.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(379, 67)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.dateTimeEdit = QtWidgets.QDateTimeEdit(Dialog)
        self.dateTimeEdit.setObjectName("dateTimeEdit")
        self.verticalLayout.addWidget(self.dateTimeEdit)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.confirmBtn = QtWidgets.QPushButton(Dialog)
        self.confirmBtn.setObjectName("confirmBtn")
        self.horizontalLayout.addWidget(self.confirmBtn)
        self.cancelBtn = QtWidgets.QPushButton(Dialog)
        self.cancelBtn.setObjectName("cancelBtn")
        self.horizontalLayout.addWidget(self.cancelBtn)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.confirmBtn.setText(_translate("Dialog", "Confirm"))
        self.cancelBtn.setText(_translate("Dialog", "Cancel"))
