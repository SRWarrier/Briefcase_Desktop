# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ShareholdersTable.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(772, 300)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.TabWidget = QtWidgets.QTabWidget(Form)
        font = QtGui.QFont()
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.TabWidget.setFont(font)
        self.TabWidget.setObjectName("TabWidget")
        self.equity = QtWidgets.QWidget()
        self.equity.setObjectName("equity")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.equity)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.tableWidget = QtWidgets.QTableWidget(self.equity)
        font = QtGui.QFont()
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.tableWidget.setFont(font)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        self.gridLayout_2.addWidget(self.tableWidget, 0, 0, 1, 1)
        self.TabWidget.addTab(self.equity, "")
        self.gridLayout.addWidget(self.TabWidget, 0, 0, 1, 1)

        self.retranslateUi(Form)
        self.TabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Form", "Name"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Form", "Father\'s Name"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Form", "Address"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("Form", "Natinality"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("Form", "No of Shares"))
        self.TabWidget.setTabText(self.TabWidget.indexOf(self.equity), _translate("Form", "Equity"))
