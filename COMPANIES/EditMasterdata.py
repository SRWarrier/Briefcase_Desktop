from PySide2 import QtWidgets, QtUiTools,QtCore, QtGui
import sys
import HomePage
import os
import numpy as np
import sqlite3
import datetime
from functions import getMasterdata
from functions import Database_Manager as db
from functions import pyside_dynamic
from functions.Gdrive import Gdrive
import requests_html


session = requests_html.HTMLSession()

class Ui(QtWidgets.QWidget):
    def __init__(self):
        super(Ui, self).__init__()
        pyside_dynamic.loadUi('Resources/ui/EditMasterdata.ui',self)
        self.dbfilepath = 'Database/C3_DataBase.db'
        self.InFrame = self.findChild(QtWidgets.QGridLayout, 'FormLayout')
        self.authorisedcapital = self.findChild(QtWidgets.QLineEdit, 'fill_Authcapital')
        self.companyemail = self.findChild(QtWidgets.QLineEdit, 'fill_Comp_email')
        self.roc = self.findChild(QtWidgets.QLineEdit, 'fill_ROC')
        self.registeredaddress = self.findChild(QtWidgets.QLineEdit, 'fill_RegAdd')
        self.paidupcapital = self.findChild(QtWidgets.QLineEdit, 'fill_paidup')
        self.category = self.findChild(QtWidgets.QLineEdit, 'fillcategory')
        self.otheraddress = self.findChild(QtWidgets.QLineEdit, 'fillfill_OtherAddress')
        self.subcategory = self.findChild(QtWidgets.QLineEdit, 'fillsubcategory')
        self.PAN = self.findChild(QtWidgets.QLineEdit, 'PanFill')
        self.GSTIN = self.findChild(QtWidgets.QLineEdit, 'GSTFill')
        self.CINentry = self.findChild(QtWidgets.QLineEdit, 'CINField')
        self.CompanyName = self.findChild(QtWidgets.QLineEdit, 'companyName')
        self.Nameentry = self.findChild(QtWidgets.QComboBox, 'NameField')
        self.conn = sqlite3.connect(self.dbfilepath)
        self.cur = self.conn.cursor()
        CompanyListdb = self.cur.execute('SELECT "company_name" from Masterdata').fetchall()
        CompanyList=['']
        for item in CompanyListdb:
            CompanyList.append(item[0])
        self.Nameentry.addItems(CompanyList)
        self.Nameentry.activated.connect(self.getdata)
        self.PrefillButton = self.findChild(QtWidgets.QPushButton, 'Prefill')
        self.PrefillButton.clicked.connect(self.getMasterdata)
        
        self.save = self.findChild(QtWidgets.QPushButton, 'Save')
        self.save.clicked.connect(self.AddMasterdata)

        self.reset = self.findChild(QtWidgets.QPushButton, 'Reset')
        self.reset.clicked.connect(self.canceledit)
        
        self.show()

    def getMasterdata(self):
        data=getMasterdata.getMasterData(self.CINentry.text().upper())
        self.JsonFile=data
        self.CompanyName.setText(data['data']['Masterdata']['company_name'])
        self.roc.setText(data['data']['Masterdata']['company_roc'])
        self.category.setText(data['data']['Masterdata']['company_category'])
        self.subcategory.setText(data['data']['Masterdata']['company_subcategory'])
        self.authorisedcapital.setText(data['data']['Masterdata']['company_authorized_capital'])
        self.paidupcapital.setText(data['data']['Masterdata']['company_paidup_capital'])
        self.registeredaddress.setText(data['data']['Masterdata']['company_registered_address'].title())
        self.otheraddress.setText(data['data']['Masterdata']['company_other_than_regsitered_office'])
        self.companyemail.setText(data['data']['Masterdata']['company_email_id'])



    def getdata(self):
        CurrentSelection = self.Nameentry.currentText()
        self.Masterdata = self.cur.execute(f'SELECT * from Masterdata WHERE company_name = "{CurrentSelection}"').fetchall()[0]
        self.authorisedcapital.setText(self.Masterdata[7])
        self.companyemail.setText(self.Masterdata[13])
        self.roc.setText(self.Masterdata[2])
        self.registeredaddress.setText(self.Masterdata[11])
        self.paidupcapital.setText(self.Masterdata[8])
        self.CompanyName.setText(self.Masterdata[1])
        self.category.setText(self.Masterdata[4])
        self.otheraddress.setText(self.Masterdata[12])
        self.subcategory.setText(self.Masterdata[5])
        self.PAN.setText(self.Masterdata[18])
        self.GSTIN.setText(self.Masterdata[19])
        self.CINentry.setText(self.Masterdata[0])

        
    def AddMasterdata(self):
        #FieldDefinition
        AuthorisedCapital = self.authorisedcapital.text()
        companyemail=self.companyemail.text()
        roc=self.roc.text()
        registeredaddress=self.registeredaddress.text()
        paidupcapital=self.paidupcapital.text()
        CompanyName=self.CompanyName.text()
        category=self.category.text()
        otheraddress=self.otheraddress.text()
        subcategory=self.subcategory.text()
        PAN=self.PAN.text()
        GSTIN=self.GSTIN.text()
        CINentry=self.CINentry.text()
        updatedate=datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d %H:%M:%S')
        self.cur.execute(f'UPDATE Masterdata SET company_name={repr(CompanyName)},company_roc={repr(roc)},company_category={repr(category)},\
                        company_subcategory={repr(subcategory)}, company_authorized_capital={AuthorisedCapital}, company_paidup_capital = {paidupcapital}\
                        ,company_registered_address = {repr(registeredaddress)},company_other_than_regsitered_office = {repr(otheraddress)},\
                        company_email_id = {repr(companyemail)},company_pan = {repr(PAN)}, company_gstin = {repr(GSTIN)}, company_last_update ={repr(updatedate)} \
                        WHERE company_cin={repr(CINentry)}')
        self.cur.close()
        self.conn.commit()
        Message = QtWidgets.QMessageBox(self)
        Message.setWindowTitle("Information")
        Message.setText(f'{CompanyName} has been updated')
        Message.buttonClicked.connect(self.canceledit)
        Message.setModal(False)
        Message.show()


    def canceledit(self):
        self.close()
        Homepage.ui.show()
