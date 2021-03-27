from PySide2 import QtWidgets, QtUiTools,QtCore, QtGui
import sys
import HomePage
import os
import numpy as np
from PIL import Image
from functions import getMasterdata, getCaptcha, getSignatories, prefillDIN, PrefillCharge
from functions import Database_Manager as db
from functions import pyside_dynamic
from functions.Gdrive import Gdrive
import requests_html
import sqlite3


session = requests_html.HTMLSession()

class Ui(QtWidgets.QWidget):
    def __init__(self):
        super(Ui, self).__init__()
        pyside_dynamic.loadUi('Resources/ui/EditSignatories.ui',self)
        self.dbfilepath = 'Database/C3_DataBase.db'
        self.Nameentry = self.findChild(QtWidgets.QComboBox, 'CompanySelect')
        self.conn = sqlite3.connect(self.dbfilepath)
        self.cur = self.conn.cursor()
        CompanyListdb = self.cur.execute('SELECT "company_name" from Masterdata').fetchall()
        CompanyList=['']
        for item in CompanyListdb:
            CompanyList.append(item[0])
        self.Nameentry.addItems(CompanyList)
        self.Nameentry.activated.connect(self.fillTable)
        self.DirectorInfo = self.findChild(QtWidgets.QTableWidget, 'DirectorInfo')
        self.savebutton = self.findChild(QtWidgets.QPushButton, 'savebutton')
        self.savebutton.clicked.connect(self.confirmSignatories)
        self.prefillButton = self.findChild(QtWidgets.QPushButton, 'Prefill')
        self.prefillButton.clicked.connect(self.warning)
        self.show()


    def fillTable(self):
        self.currentselection = self.Nameentry.currentText()
        self.CINNum = self.cur.execute(f'SELECT company_cin from Masterdata WHERE company_name = "{self.currentselection}"').fetchall()[0][0]
        SignatoriesList = self.cur.execute(f'SELECT * from Signatories WHERE company_cin = {repr(self.CINNum)}').fetchall()
        self.DirectorInfo.setRowCount(len(SignatoriesList))
        for x in range(len(SignatoriesList)):
            for y in range(len(SignatoriesList[x])):
                if not y+1==len(SignatoriesList[x]):
                    item = QtWidgets.QTableWidgetItem()
                    self.DirectorInfo.setItem(x, y, item)
                    item.setText(str(SignatoriesList[x][y+1]))
                    self.DirectorInfo.resizeRowsToContents()

    def warning(self):
        self.warnMessage = QtWidgets.QMessageBox()
        self.warnMessage.setWindowTitle("Information")
        self.warnMessage.setText(f'All Signatories details would be refreshed to MCA Masterdata. Do you want to continue?')
        self.warnMessage.setModal(False)
        self.AddSignatoriesButtion = QtWidgets.QPushButton()
        self.AddSignatoriesButtion.setText('Yes')
        self.AddSignatoriesButtion.clicked.connect(self.captcha)
        self.warnMessage.addButton(self.AddSignatoriesButtion, QtWidgets.QMessageBox.YesRole)
        self.warnMessage.show()
        
    def captcha(self):
        self.captchaWindow = QtWidgets.QWidget()
        pyside_dynamic.loadUi('Resources/ui/captcha.ui',self.captchaWindow)
        #self.captchaWindow.move(300,300)
        self.captchaView = self.captchaWindow.findChild(QtWidgets.QLabel, 'captchaview')
        self.getCaptcha()
        self.CaptchaInput = self.captchaWindow.findChild(QtWidgets.QLineEdit, 'captchainput')
        self.SubmitButton = self.captchaWindow.findChild(QtWidgets.QPushButton, 'submit')
        self.SubmitButton.clicked.connect(self.getSignatories)
        self.refreshButton = self.captchaWindow.findChild(QtWidgets.QPushButton, 'refresh')
        self.refreshButton.clicked.connect(self.getCaptcha)
        self.captchaWindow.show()


    def getCaptcha(self):
        capcthaImage = getCaptcha.getMCA_Captcha(session)
        pixmap = QtGui.QPixmap()
        pixmap.loadFromData(capcthaImage)
        self.captchaView.setScaledContents(True)
        self.captchaView.setPixmap(pixmap)
        self.captchaView.setAlignment(QtCore.Qt.AlignVCenter)
        self.captchaView.setAlignment(QtCore.Qt.AlignHCenter)
        

    def getSignatories(self):
        self.signatoriesinfo = getSignatories.getSignatory(session, self.CINNum,captcha = self.CaptchaInput.text())
        if self.signatoriesinfo['Status']=='Failed':
            self.getCaptcha()
        else:
            self.captchaWindow.close()
            try:
                for x in range(len(self.signatoriesinfo['data'])):
                    DIN = self.signatoriesinfo['data'][x+1]['DIN/DPIN/PAN']
                    DINData = prefillDIN.prefillDIN(DIN)
                    if isinstance(DINData,dict):
                        self.signatoriesinfo['data'][x+1]={**self.signatoriesinfo['data'][x+1],**DINData}
                self.signatoriesdetails = self.signatoriesinfo['data']
                self.DirectorInfo.setRowCount(len(self.signatoriesdetails))
                for x in range(len(self.signatoriesdetails)):
                    DirectInfo = list(self.signatoriesdetails[x+1].values())
                    for y in range(len(self.signatoriesdetails[x+1])):
                        item = QtWidgets.QTableWidgetItem()
                        self.DirectorInfo.setItem(x, y, item)
                        item.setText(str(DirectInfo[y]))
                self.DirectorInfo.resizeRowsToContents()    
            except IndexError as e:
                print(e)
                pass


    def confirmSignatories(self):
        SignatoriesList=[]
        for x in range(self.DirectorInfo.rowCount()):
                m=[]
                m.append(self.CINNum)
                for y in range(self.DirectorInfo.columnCount()):
                    try:
                        m.append(self.DirectorInfo.item(x,y).text())
                    except:
                        m.append('')
                SignatoriesList.append(tuple(m))
        print(m)
        db.updateSignatories(SignatoriesList)
        Message = QtWidgets.QMessageBox(self)
        Message.setWindowTitle("Information")
        Message.setText(f'Signatories has been updated')
        Message.setModal(False)
        self.AddSignatoriesButtion = QtWidgets.QPushButton()
        self.AddSignatoriesButtion.setText('Done')
        self.AddSignatoriesButtion.clicked.connect(self.dashboard)
        Message.addButton(self.AddSignatoriesButtion, QtWidgets.QMessageBox.YesRole)
        Message.show()

    def dashboard(self):
        self.close()
        Ui()
