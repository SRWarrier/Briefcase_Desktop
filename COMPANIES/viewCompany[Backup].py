from PySide2 import QtWidgets, QtUiTools,QtCore, QtGui
import sys
import HomePage
import os
from functions import pyside_dynamic
#from functions.Gdrive import Gdrive
import requests_html
import sqlite3
import pandas as pd


session = requests_html.HTMLSession()

class Ui(QtWidgets.QWidget):
    def __init__(self):
        super(Ui, self).__init__()
        pyside_dynamic.loadUi('../Resources/ui/viewCompany.ui',self)
        self.dbfilepath = 'Database/C3_DataBase.db'
        self.authorisedcapital = self.findChild(QtWidgets.QLineEdit, 'fill_Authcapital')
        self.companyemail = self.findChild(QtWidgets.QLineEdit, 'fill_Comp_email')
        self.dateofincorporation = self.findChild(QtWidgets.QLineEdit, 'fill_DateofIncorp')
        self.roc = self.findChild(QtWidgets.QLineEdit, 'fill_ROC')
        self.registeredaddress = self.findChild(QtWidgets.QLineEdit, 'fill_RegAdd')
        self.registrationno = self.findChild(QtWidgets.QLineEdit, 'fill_RegNo')
        self.islisted = self.findChild(QtWidgets.QLineEdit, 'fill_listed')
        self.paidupcapital = self.findChild(QtWidgets.QLineEdit, 'fill_paidup')
        self.category = self.findChild(QtWidgets.QLineEdit, 'fillcategory')
        self.companyclass = self.findChild(QtWidgets.QLineEdit, 'fillclass')
        self.otheraddress = self.findChild(QtWidgets.QLineEdit, 'fillfill_OtherAddress')
        self.subcategory = self.findChild(QtWidgets.QLineEdit, 'fillsubcategory')
        self.PAN = self.findChild(QtWidgets.QLineEdit, 'PanFill')
        self.GSTIN = self.findChild(QtWidgets.QLineEdit, 'GSTFill')
        self.CINentry = self.findChild(QtWidgets.QLineEdit, 'CIN')
        self.CompanyName = self.findChild(QtWidgets.QLineEdit, 'CompanyName')
        self.Nameentry = self.findChild(QtWidgets.QComboBox, 'CompanySelect')
        self.conn = sqlite3.connect(self.dbfilepath)
        self.cur = self.conn.cursor()
        CompanyListdb = self.cur.execute('SELECT "company_name" from Masterdata').fetchall()
        CompanyList=['']
        for item in CompanyListdb:
            CompanyList.append(item[0])
        self.Nameentry.addItems(CompanyList)
        self.Nameentry.activated.connect(self.getdata)
        #self.show()

    def getdata(self):
        CurrentSelection = self.Nameentry.currentText()
        self.Masterdata = self.cur.execute(f'SELECT * from Masterdata WHERE company_name = "{CurrentSelection}"').fetchall()[0]
        self.authorisedcapital.setText(self.Masterdata[7])
        self.dateofincorporation.setText(self.Masterdata[10])
        self.roc.setText(self.Masterdata[2])
        self.registeredaddress.setText(self.Masterdata[11])
        self.registrationno.setText(self.Masterdata[3])
        self.islisted.setText(self.Masterdata[14])
        self.paidupcapital.setText(self.Masterdata[8])
        self.category.setText(self.Masterdata[4])
        self.companyclass.setText(self.Masterdata[6])
        self.otheraddress.setText(self.Masterdata[12])
        self.subcategory.setText(self.Masterdata[5])
        self.PAN.setText(self.Masterdata[18])
        self.GSTIN.setText(self.Masterdata[19])
        self.CINentry.setText(self.Masterdata[0])
        self.CompanyName.setText(self.Masterdata[1])
        self.companyemail.setText(self.Masterdata[13])
        self.CINNum = self.cur.execute(f'SELECT company_cin from Masterdata WHERE company_name = "{CurrentSelection}"').fetchall()[0][0]
        SignatoriesList = self.cur.execute(f'SELECT * from Signatories WHERE company_cin = {repr(self.CINNum)}').fetchall()
        self.DirectorInfo.setRowCount(len(SignatoriesList))
        for x in range(len(SignatoriesList)):
            for y in range(len(SignatoriesList[x])):
                if not y+1==len(SignatoriesList[x]):
                    item = QtWidgets.QTableWidgetItem()
                    item.setFlags(QtCore.Qt.ItemIsEnabled)
                    self.DirectorInfo.setItem(x, y, item)
                    item.setText(str(SignatoriesList[x][y+1]))
                    self.DirectorInfo.resizeRowsToContents()        
        ContactList = self.cur.execute(f'SELECT * from Contacts WHERE company_cin = {repr(self.CINNum)}').fetchall()
        self.contactDisplay.setRowCount(len(ContactList))
        for x in range(len(ContactList)):
            for y in range(len(ContactList[x])):
                if not y+1==len(ContactList[x]):
                    item = QtWidgets.QTableWidgetItem()
                    item.setFlags(QtCore.Qt.ItemIsEnabled)
                    self.contactDisplay.setItem(x, y, item)
                    item.setText(str(ContactList[x][y+1]))
                    self.contactDisplay.resizeRowsToContents()
        header  = self.DirectorInfo.horizontalHeader()
        for col in range(self.DirectorInfo.columnCount()):
            header.setSectionResizeMode(col, QtWidgets.QHeaderView.ResizeToContents)
            
