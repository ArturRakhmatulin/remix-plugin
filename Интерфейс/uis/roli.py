# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'roli.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DialogRoli(object):
    def setupUi(self, DialogRoli):
        DialogRoli.setObjectName("DialogRoli")
        DialogRoli.resize(612, 247)
        self.label = QtWidgets.QLabel(DialogRoli)
        self.label.setGeometry(QtCore.QRect(0, 10, 611, 101))
        font = QtGui.QFont()
        font.setPointSize(57)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        font.setKerning(True)
        self.label.setFont(font)
        self.label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(DialogRoli)
        self.label_2.setGeometry(QtCore.QRect(60, 150, 201, 51))
        font = QtGui.QFont()
        font.setPointSize(25)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(DialogRoli)
        self.label_3.setGeometry(QtCore.QRect(200, 170, 431, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")

        self.retranslateUi(DialogRoli)
        QtCore.QMetaObject.connectSlotsByName(DialogRoli)

    def retranslateUi(self, DialogRoli):
        _translate = QtCore.QCoreApplication.translate
        DialogRoli.setWindowTitle(_translate("DialogRoli", "Dialog"))
        self.label.setText(_translate("DialogRoli", "роль"))
        self.label_2.setText(_translate("DialogRoli", "БАЛАНС:"))
        self.label_3.setText(_translate("DialogRoli", "1212321457900000000"))
