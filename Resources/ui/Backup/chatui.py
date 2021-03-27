# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'chat.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(461, 658)
        Form.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.Title = QtWidgets.QLabel(Form)
        self.Title.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        font.setPointSize(11)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.Title.setFont(font)
        self.Title.setAlignment(QtCore.Qt.AlignCenter)
        self.Title.setObjectName("Title")
        self.gridLayout.addWidget(self.Title, 0, 0, 1, 1)
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setMaximumSize(QtCore.QSize(16777215, 50))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(6, 6, 6, 6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.attachment = QtWidgets.QToolButton(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.attachment.sizePolicy().hasHeightForWidth())
        self.attachment.setSizePolicy(sizePolicy)
        self.attachment.setMaximumSize(QtCore.QSize(50, 50))
        self.attachment.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color:rgb(255,143,0);\n"
"border-radius:10;")
        self.attachment.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../Icon/folder.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.attachment.setIcon(icon)
        self.attachment.setIconSize(QtCore.QSize(32, 32))
        self.attachment.setObjectName("attachment")
        self.horizontalLayout.addWidget(self.attachment)
        self.message = QtWidgets.QTextEdit(self.widget)
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        font.setPointSize(9)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.message.setFont(font)
        self.message.setStyleSheet("color: rgb(20, 20, 20);\n"
"border-radius:10;\n"
"border :2px solid;\n"
"border-top-color: rgb(74, 159, 255);\n"
"border-left-color: rgb(64, 159, 255);\n"
"border-right-color: rgb(38, 134, 206);\n"
"border-bottom-color: rgb(49, 122, 194);\n"
"")
        self.message.setFrameShape(QtWidgets.QFrame.Panel)
        self.message.setFrameShadow(QtWidgets.QFrame.Raised)
        self.message.setObjectName("message")
        self.horizontalLayout.addWidget(self.message)
        self.send = QtWidgets.QPushButton(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.send.sizePolicy().hasHeightForWidth())
        self.send.setSizePolicy(sizePolicy)
        self.send.setMaximumSize(QtCore.QSize(120, 16777215))
        self.send.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color:rgb(0,150,136);\n"
"border-radius:10;")
        self.send.setObjectName("send")
        self.horizontalLayout.addWidget(self.send)
        self.gridLayout.addWidget(self.widget, 2, 0, 1, 1)
        self.ChatWindow = QtWidgets.QWidget(Form)
        self.ChatWindow.setStyleSheet("color: rgb(20, 20, 20);\n"
"border-radius:10;\n"
"border :2px solid;\n"
"border-top-color: rgb(74, 159, 255);\n"
"border-left-color: rgb(64, 159, 255);\n"
"border-right-color: rgb(38, 134, 206);\n"
"border-bottom-color: rgb(49, 122, 194);\n"
"")
        self.ChatWindow.setObjectName("ChatWindow")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.ChatWindow)
        self.gridLayout_2.setObjectName("gridLayout_2")
        spacerItem = QtWidgets.QSpacerItem(20, 555, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.ChatWindow, 1, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.Title.setText(_translate("Form", "Chat Room"))
        self.send.setText(_translate("Form", "Send"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
