# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AddResolution.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(737, 498)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../Icon/logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Form.setWindowIcon(icon)
        Form.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.gridLayout_2 = QtWidgets.QGridLayout(Form)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label = QtWidgets.QLabel(Form)
        self.label.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        self.label.setFont(font)
        self.label.setStyleSheet("background-color: rgb(129,199,132);\n"
"color: rgb(255, 255, 255);")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.widget = QtWidgets.QWidget(Form)
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        self.widget.setFont(font)
        self.widget.setObjectName("widget")
        self.formLayout = QtWidgets.QFormLayout(self.widget)
        self.formLayout.setObjectName("formLayout")
        self.DescriptonLabel = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.DescriptonLabel.setFont(font)
        self.DescriptonLabel.setObjectName("DescriptonLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.DescriptonLabel)
        self.DescriptionInput = QtWidgets.QLineEdit(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.DescriptionInput.sizePolicy().hasHeightForWidth())
        self.DescriptionInput.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        self.DescriptionInput.setFont(font)
        self.DescriptionInput.setObjectName("DescriptionInput")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.DescriptionInput)
        self.TitleLabel = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.TitleLabel.setFont(font)
        self.TitleLabel.setObjectName("TitleLabel")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.TitleLabel)
        self.TitleInput = QtWidgets.QLineEdit(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.TitleInput.sizePolicy().hasHeightForWidth())
        self.TitleInput.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        self.TitleInput.setFont(font)
        self.TitleInput.setObjectName("TitleInput")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.TitleInput)
        self.NarrationLabel = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.NarrationLabel.setFont(font)
        self.NarrationLabel.setObjectName("NarrationLabel")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.NarrationLabel)
        self.NarrationInput = QtWidgets.QTextEdit(self.widget)
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        self.NarrationInput.setFont(font)
        self.NarrationInput.setObjectName("NarrationInput")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.NarrationInput)
        self.ResolutionLabel = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.ResolutionLabel.setFont(font)
        self.ResolutionLabel.setObjectName("ResolutionLabel")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.ResolutionLabel)
        self.ResolutionInput = QtWidgets.QTextEdit(self.widget)
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        self.ResolutionInput.setFont(font)
        self.ResolutionInput.setObjectName("ResolutionInput")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.ResolutionInput)
        self.label_2 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        font.setBold(True)
        font.setWeight(75)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.summary = QtWidgets.QTextEdit(self.widget)
        self.summary.setObjectName("summary")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.summary)
        self.gridLayout_2.addWidget(self.widget, 1, 0, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(Form)
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.textBrowser = QtWidgets.QTextBrowser(self.groupBox)
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.textBrowser.setFont(font)
        self.textBrowser.setObjectName("textBrowser")
        self.gridLayout.addWidget(self.textBrowser, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.groupBox, 2, 0, 1, 1)
        self.ButtonGroup = QtWidgets.QWidget(Form)
        self.ButtonGroup.setMinimumSize(QtCore.QSize(0, 30))
        self.ButtonGroup.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        self.ButtonGroup.setFont(font)
        self.ButtonGroup.setObjectName("ButtonGroup")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.ButtonGroup)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.AddVariables = QtWidgets.QPushButton(self.ButtonGroup)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.AddVariables.sizePolicy().hasHeightForWidth())
        self.AddVariables.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.AddVariables.setFont(font)
        self.AddVariables.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color:rgb(0,150,136);\n"
"border-radius:10;")
        self.AddVariables.setObjectName("AddVariables")
        self.horizontalLayout_3.addWidget(self.AddVariables)
        self.gridLayout_2.addWidget(self.ButtonGroup, 3, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Add Resolution"))
        self.label.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:14pt; font-weight:600;\">ADD RESOLUTION</span></p></body></html>"))
        self.DescriptonLabel.setText(_translate("Form", "<html><head/><body><p><span style=\" font-weight:600;\">Description</span></p></body></html>"))
        self.TitleLabel.setText(_translate("Form", "<html><head/><body><p><span style=\" font-weight:600;\">Title</span></p></body></html>"))
        self.NarrationLabel.setText(_translate("Form", "<html><head/><body><p><span style=\" font-weight:600;\">Narration</span></p></body></html>"))
        self.ResolutionLabel.setText(_translate("Form", "<html><head/><body><p><span style=\" font-weight:600;\">Resolution</span></p></body></html>"))
        self.label_2.setText(_translate("Form", "Agenda Note"))
        self.groupBox.setTitle(_translate("Form", "Instruction"))
        self.textBrowser.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Open Sans\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\';\">Add variable within {--} brackets. </span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\';\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-weight:600; text-decoration: underline;\">Naming Guidelines</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-weight:600; text-decoration: underline;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\';\">1. Do not use Space for variable. Instead use underscore \'_\'.</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\';\">2. Variable will be used for query from user. Use sensible variable name.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\';\"><br /></p></body></html>"))
        self.AddVariables.setText(_translate("Form", "Add Variables"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
