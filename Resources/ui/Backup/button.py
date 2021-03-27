# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Button.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 300)
        self.ButtonPanel = QtWidgets.QWidget(Form)
        self.ButtonPanel.setGeometry(QtCore.QRect(50, 90, 321, 81))
        self.ButtonPanel.setStyleSheet("border-radius:30;\n"
"background-color: rgb(113, 42, 255);")
        self.ButtonPanel.setObjectName("ButtonPanel")
        self.gridLayout = QtWidgets.QGridLayout(self.ButtonPanel)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.Icon = QtWidgets.QLabel(self.ButtonPanel)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Icon.sizePolicy().hasHeightForWidth())
        self.Icon.setSizePolicy(sizePolicy)
        self.Icon.setMaximumSize(QtCore.QSize(101, 16777215))
        self.Icon.setStyleSheet("background-color: rgb(255, 255, 127);")
        self.Icon.setText("")
        self.Icon.setPixmap(QtGui.QPixmap("../Icon/company.png"))
        self.Icon.setAlignment(QtCore.Qt.AlignCenter)
        self.Icon.setObjectName("Icon")
        self.gridLayout.addWidget(self.Icon, 0, 0, 1, 1)
        self.Button = QtWidgets.QPushButton(self.ButtonPanel)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Button.sizePolicy().hasHeightForWidth())
        self.Button.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.Button.setFont(font)
        self.Button.setStyleSheet("color: rgb(255, 255, 255);")
        self.Button.setFlat(True)
        self.Button.setObjectName("Button")
        self.gridLayout.addWidget(self.Button, 0, 1, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.Button.setText(_translate("Form", "COMPANY AUDIT"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
