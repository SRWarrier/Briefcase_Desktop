# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/MeetingsManager.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1425, 416)
        Form.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.frame_2 = QtWidgets.QFrame(Form)
        self.frame_2.setMinimumSize(QtCore.QSize(0, 30))
        self.frame_2.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setFamily("Georgia")
        font.setPointSize(10)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.frame_2.setFont(font)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(self.frame_2)
        font = QtGui.QFont()
        font.setFamily("Georgia")
        font.setPointSize(10)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.radioButton = QtWidgets.QRadioButton(self.frame_2)
        font = QtGui.QFont()
        font.setFamily("Georgia")
        font.setPointSize(10)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.radioButton.setFont(font)
        self.radioButton.setChecked(True)
        self.radioButton.setObjectName("radioButton")
        self.horizontalLayout_2.addWidget(self.radioButton)
        self.frame_3 = QtWidgets.QFrame(self.frame_2)
        font = QtGui.QFont()
        font.setFamily("Georgia")
        font.setPointSize(10)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.frame_3.setFont(font)
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame_3)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.commitee = QtWidgets.QRadioButton(self.frame_3)
        font = QtGui.QFont()
        font.setFamily("Georgia")
        font.setPointSize(10)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.commitee.setFont(font)
        self.commitee.setObjectName("commitee")
        self.horizontalLayout.addWidget(self.commitee)
        self.board = QtWidgets.QRadioButton(self.frame_3)
        font = QtGui.QFont()
        font.setFamily("Georgia")
        font.setPointSize(10)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.board.setFont(font)
        self.board.setCheckable(True)
        self.board.setChecked(False)
        self.board.setAutoRepeat(False)
        self.board.setObjectName("board")
        self.horizontalLayout.addWidget(self.board)
        self.EGM = QtWidgets.QRadioButton(self.frame_3)
        font = QtGui.QFont()
        font.setFamily("Georgia")
        font.setPointSize(10)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.EGM.setFont(font)
        self.EGM.setObjectName("EGM")
        self.horizontalLayout.addWidget(self.EGM)
        self.AGM = QtWidgets.QRadioButton(self.frame_3)
        font = QtGui.QFont()
        font.setFamily("Georgia")
        font.setPointSize(10)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.AGM.setFont(font)
        self.AGM.setObjectName("AGM")
        self.horizontalLayout.addWidget(self.AGM)
        self.horizontalLayout_2.addWidget(self.frame_3)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.addMeeting = QtWidgets.QPushButton(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.addMeeting.sizePolicy().hasHeightForWidth())
        self.addMeeting.setSizePolicy(sizePolicy)
        self.addMeeting.setMinimumSize(QtCore.QSize(120, 0))
        self.addMeeting.setMaximumSize(QtCore.QSize(120, 16777215))
        self.addMeeting.setSizeIncrement(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("Georgia")
        font.setPointSize(10)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.addMeeting.setFont(font)
        self.addMeeting.setStyleSheet("background-color:rgb(0, 170, 0);\n"
"color: rgb(255, 255, 255);\n"
"border-radius:10")
        self.addMeeting.setObjectName("addMeeting")
        self.horizontalLayout_2.addWidget(self.addMeeting)
        self.addNotice = QtWidgets.QPushButton(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.addNotice.sizePolicy().hasHeightForWidth())
        self.addNotice.setSizePolicy(sizePolicy)
        self.addNotice.setMinimumSize(QtCore.QSize(120, 0))
        self.addNotice.setMaximumSize(QtCore.QSize(120, 16777215))
        font = QtGui.QFont()
        font.setFamily("Georgia")
        font.setPointSize(10)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.addNotice.setFont(font)
        self.addNotice.setStyleSheet("background-color:rgb(0, 170, 0);\n"
"color: rgb(255, 255, 255);\n"
"border-radius:10")
        self.addNotice.setObjectName("addNotice")
        self.horizontalLayout_2.addWidget(self.addNotice)
        self.addMinute = QtWidgets.QPushButton(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.addMinute.sizePolicy().hasHeightForWidth())
        self.addMinute.setSizePolicy(sizePolicy)
        self.addMinute.setMinimumSize(QtCore.QSize(120, 0))
        self.addMinute.setMaximumSize(QtCore.QSize(120, 16777215))
        font = QtGui.QFont()
        font.setFamily("Georgia")
        font.setPointSize(10)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.addMinute.setFont(font)
        self.addMinute.setStyleSheet("background-color:rgb(0, 170, 0);\n"
"color: rgb(255, 255, 255);\n"
"border-radius:10")
        self.addMinute.setObjectName("addMinute")
        self.horizontalLayout_2.addWidget(self.addMinute)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.gridLayout.addWidget(self.frame_2, 0, 0, 1, 1)
        self.scrollArea = QtWidgets.QScrollArea(Form)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.meetingArea = QtWidgets.QWidget()
        self.meetingArea.setGeometry(QtCore.QRect(0, 0, 1405, 360))
        self.meetingArea.setObjectName("meetingArea")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.meetingArea)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.meetingTable = QtWidgets.QTableWidget(self.meetingArea)
        self.meetingTable.setObjectName("meetingTable")
        self.meetingTable.setColumnCount(7)
        self.meetingTable.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Georgia")
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        item.setFont(font)
        self.meetingTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Georgia")
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        item.setFont(font)
        self.meetingTable.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Georgia")
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        item.setFont(font)
        self.meetingTable.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Georgia")
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        item.setFont(font)
        self.meetingTable.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Georgia")
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        item.setFont(font)
        self.meetingTable.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Georgia")
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        item.setFont(font)
        self.meetingTable.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Georgia")
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        item.setFont(font)
        self.meetingTable.setHorizontalHeaderItem(6, item)
        self.meetingTable.horizontalHeader().setStretchLastSection(True)
        self.verticalLayout.addWidget(self.meetingTable)
        self.scrollArea.setWidget(self.meetingArea)
        self.gridLayout.addWidget(self.scrollArea, 1, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "Filters:"))
        self.radioButton.setText(_translate("Form", "None"))
        self.commitee.setText(_translate("Form", "Committee Meeting"))
        self.board.setText(_translate("Form", "Board Meeting"))
        self.EGM.setText(_translate("Form", "Extra Ordinary General Meeting"))
        self.AGM.setText(_translate("Form", "Annual General Meeting"))
        self.addMeeting.setText(_translate("Form", "Add Meeting"))
        self.addNotice.setText(_translate("Form", "Add Notice"))
        self.addMinute.setText(_translate("Form", "Add Minute"))
        item = self.meetingTable.horizontalHeaderItem(0)
        item.setText(_translate("Form", "Date"))
        item = self.meetingTable.horizontalHeaderItem(1)
        item.setText(_translate("Form", "Type"))
        item = self.meetingTable.horizontalHeaderItem(2)
        item.setText(_translate("Form", "Financial Year"))
        item = self.meetingTable.horizontalHeaderItem(3)
        item.setText(_translate("Form", "Prepared By"))
        item = self.meetingTable.horizontalHeaderItem(4)
        item.setText(_translate("Form", "Checked By"))
        item = self.meetingTable.horizontalHeaderItem(5)
        item.setText(_translate("Form", "Notice"))
        item = self.meetingTable.horizontalHeaderItem(6)
        item.setText(_translate("Form", "Minutes"))
