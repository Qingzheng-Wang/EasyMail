# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\2022-2023大三上学习笔记\计算机网络课程设计\Mail-System\SigninWindow.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(514, 496)
        Dialog.setMinimumSize(QtCore.QSize(514, 496))
        Dialog.setMaximumSize(QtCore.QSize(514, 496))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        Dialog.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(10)
        Dialog.setFont(font)
        Dialog.setContextMenuPolicy(QtCore.Qt.PreventContextMenu)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../dove1.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        self.labelServerAddress = QtWidgets.QLabel(Dialog)
        self.labelServerAddress.setGeometry(QtCore.QRect(120, 220, 61, 31))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.labelServerAddress.setFont(font)
        self.labelServerAddress.setObjectName("labelServerAddress")
        self.labelUsername = QtWidgets.QLabel(Dialog)
        self.labelUsername.setGeometry(QtCore.QRect(90, 270, 91, 31))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.labelUsername.setFont(font)
        self.labelUsername.setObjectName("labelUsername")
        self.lineEditUsername = QtWidgets.QLineEdit(Dialog)
        self.lineEditUsername.setGeometry(QtCore.QRect(190, 270, 251, 31))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(10)
        self.lineEditUsername.setFont(font)
        self.lineEditUsername.setText("")
        self.lineEditUsername.setObjectName("lineEditUsername")
        self.labelPassword = QtWidgets.QLabel(Dialog)
        self.labelPassword.setGeometry(QtCore.QRect(100, 320, 81, 31))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.labelPassword.setFont(font)
        self.labelPassword.setObjectName("labelPassword")
        self.lineEditPassword = QtWidgets.QLineEdit(Dialog)
        self.lineEditPassword.setGeometry(QtCore.QRect(190, 320, 251, 31))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(10)
        self.lineEditPassword.setFont(font)
        self.lineEditPassword.setText("")
        self.lineEditPassword.setObjectName("lineEditPassword")
        self.pushButtonSignin = QtWidgets.QPushButton(Dialog)
        self.pushButtonSignin.setGeometry(QtCore.QRect(220, 380, 91, 41))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.pushButtonSignin.setFont(font)
        self.pushButtonSignin.setObjectName("pushButtonSignin")
        self.labelDoveIcon = QtWidgets.QLabel(Dialog)
        self.labelDoveIcon.setGeometry(QtCore.QRect(70, 50, 121, 121))
        self.labelDoveIcon.setText("")
        self.labelDoveIcon.setPixmap(QtGui.QPixmap("../dove1.png"))
        self.labelDoveIcon.setObjectName("labelDoveIcon")
        self.labelEasyMail = QtWidgets.QLabel(Dialog)
        self.labelEasyMail.setGeometry(QtCore.QRect(220, 80, 191, 71))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(30)
        self.labelEasyMail.setFont(font)
        self.labelEasyMail.setObjectName("labelEasyMail")
        self.comboBoxServerAddress = QtWidgets.QComboBox(Dialog)
        self.comboBoxServerAddress.setGeometry(QtCore.QRect(190, 220, 251, 31))
        self.comboBoxServerAddress.setObjectName("comboBoxServerAddress")
        self.comboBoxServerAddress.addItem("")
        self.comboBoxServerAddress.addItem("")
        self.comboBoxServerAddress.addItem("")
        self.comboBoxServerAddress.addItem("")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "EasyMail"))
        self.labelServerAddress.setText(_translate("Dialog", "Server:"))
        self.labelUsername.setText(_translate("Dialog", "Username:"))
        self.labelPassword.setText(_translate("Dialog", "Password:"))
        self.pushButtonSignin.setText(_translate("Dialog", "Sign in"))
        self.labelEasyMail.setText(_translate("Dialog", "EasyMail"))
        self.comboBoxServerAddress.setItemText(0, _translate("Dialog", "QQ Mail"))
        self.comboBoxServerAddress.setItemText(1, _translate("Dialog", "WHU E-Mail"))
        self.comboBoxServerAddress.setItemText(2, _translate("Dialog", "163 Mail"))
        self.comboBoxServerAddress.setItemText(3, _translate("Dialog", "Gmail"))
