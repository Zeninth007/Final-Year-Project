# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'filter_feature_ui.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(379, 99)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.contrastSpinbox = QtWidgets.QDoubleSpinBox(Dialog)
        self.contrastSpinbox.setMinimumSize(QtCore.QSize(300, 0))
        self.contrastSpinbox.setObjectName("contrastSpinbox")
        self.horizontalLayout.addWidget(self.contrastSpinbox)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.sharpnessSpinbox = QtWidgets.QDoubleSpinBox(Dialog)
        self.sharpnessSpinbox.setMinimumSize(QtCore.QSize(300, 0))
        self.sharpnessSpinbox.setObjectName("sharpnessSpinbox")
        self.horizontalLayout_2.addWidget(self.sharpnessSpinbox)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.confirmBtn = QtWidgets.QPushButton(Dialog)
        self.confirmBtn.setObjectName("confirmBtn")
        self.horizontalLayout_3.addWidget(self.confirmBtn)
        self.cancelBtn = QtWidgets.QPushButton(Dialog)
        self.cancelBtn.setObjectName("cancelBtn")
        self.horizontalLayout_3.addWidget(self.cancelBtn)
        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Contrast: "))
        self.label_2.setText(_translate("Dialog", "Blurriness: "))
        self.confirmBtn.setText(_translate("Dialog", "Confirm"))
        self.cancelBtn.setText(_translate("Dialog", "Cancel"))
