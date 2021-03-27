from PySide2 import QtWidgets, QtUiTools,QtCore, QtGui
import sys
import os
from functions import getForms, listForms
from functions import pyside_dynamic
import sqlite3



class Ui(QtWidgets.QWidget):
    def __init__(self):
        super(Ui, self).__init__()
        pyside_dynamic.loadUi('Resources/ui/GetForms.ui',self)
        self.CompanySelect = self.findChild(QtWidgets.QComboBox, 'CompanySelect')
        dbfilepath = 'Database/C3_DataBase.db'
        self.conn = sqlite3.connect(dbfilepath)
        self.cur = self.conn.cursor()
        CompanyListdb = self.cur.execute('SELECT "company_name" from Masterdata').fetchall()
        CompanyList=['']
        for item in CompanyListdb:
            CompanyList.append(item[0])
        self.CompanySelect.addItems(CompanyList)
        self.FormSelect = self.findChild(QtWidgets.QComboBox, 'FormSelect')
        self.FormDict = listForms.getForm()
        self.FormSelect.addItems(self.FormDict.keys())
        self.Purpose = self.findChild(QtWidgets.QLineEdit, 'Purpose')
        self.DownloadForm = self.findChild(QtWidgets.QPushButton, 'DownloadForm')
        self.DownloadForm.clicked.connect(self.download)
        self.show()


    def download(self):
        CompanySelection = self.CompanySelect.currentText()
        SelectedForm = self.FormSelect.currentText()
        Purpose = self.Purpose.text()
        getForms.getForm(self.FormDict,SelectedForm,CompanySelection,Purpose)
