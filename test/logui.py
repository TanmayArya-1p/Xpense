# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Login.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Loginform(object):
    def setupUi(self, Loginform):
        Loginform.setObjectName("Loginform")
        Loginform.resize(179, 258)
        Loginform.setStyleSheet("background-color: rgb(25, 25, 25);\n"
"")
        self.username = QtWidgets.QLineEdit(Loginform)
        self.username.setGeometry(QtCore.QRect(40, 50, 113, 20))
        self.username.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.username.setText("")
        self.username.setObjectName("username")
        self.password = QtWidgets.QLineEdit(Loginform)
        self.password.setGeometry(QtCore.QRect(40, 80, 113, 20))
        self.password.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.password.setText("")
        self.password.setObjectName("password")
        self.gauth = QtWidgets.QPushButton(Loginform)
        self.gauth.setGeometry(QtCore.QRect(50, 160, 75, 23))
        self.gauth.setStyleSheet("color: rgb(0,0,0);\n"
"background-color: rgb(255,255,255);\n"
"font: 8pt \"Leelawadee\";\n"
"\n"
"border-style: outset;\n"
"border-width: 2px;\n"
"border-radius: 7px;")
        self.gauth.setObjectName("gauth")
        self.cancel = QtWidgets.QPushButton(Loginform)
        self.cancel.setGeometry(QtCore.QRect(50, 200, 75, 23))
        self.cancel.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 8pt \"Leelawadee\";\n"
"\n"
"border-style: outset;\n"
"border-width: 2px;\n"
"border-radius: 7px;")
        self.cancel.setObjectName("cancel")
        self.login = QtWidgets.QToolButton(Loginform)
        self.login.setGeometry(QtCore.QRect(50, 120, 75, 23))
        self.login.setStyleSheet("\n"
"color: rgb(0,0,0);\n"
"background-color: rgb(255,255,255);\n"
"font: 8pt \"Leelawadee\";\n"
"\n"
"border-style: outset;\n"
"border-width: 2px;\n"
"border-radius: 7px;\n"
"")
        self.login.setObjectName("login")
        self.logo = QtWidgets.QLabel(Loginform)
        self.logo.setGeometry(QtCore.QRect(70, 0, 41, 41))
        self.logo.setText("")
        self.logo.setPixmap(QtGui.QPixmap("../../../Downloads/LOGO.jpg"))
        self.logo.setScaledContents(True)
        self.logo.setObjectName("logo")

        self.retranslateUi(Loginform)
        QtCore.QMetaObject.connectSlotsByName(Loginform)

    def retranslateUi(self, Loginform):
        _translate = QtCore.QCoreApplication.translate
        Loginform.setWindowTitle(_translate("Loginform", "Login"))
        self.username.setPlaceholderText(_translate("Loginform", "Username"))
        self.password.setPlaceholderText(_translate("Loginform", "Password"))
        self.gauth.setText(_translate("Loginform", "Gmail Login"))
        self.cancel.setText(_translate("Loginform", "Cancel"))
        self.login.setText(_translate("Loginform", "Login"))
