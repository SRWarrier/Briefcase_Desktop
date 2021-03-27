from PySide2 import QtWidgets, QtUiTools,QtCore, QtGui
import sys
import HomePage
import os
import numpy as np
from PIL import Image
from functions import getMasterdata, getCaptcha, getSignatories, prefillDIN
from functions import Database_Manager as db
from functions import pyside_dynamic
from functions.Gdrive import Gdrive
import requests_html
import sqlite3

session = requests_html.HTMLSession()

class Ui(QtWidgets.QWidget):
    def __init__(self, isSidebar = False):
        super(Ui, self).__init__()
        if isSidebar:
            pyside_dynamic.loadUi('Resources/ui/MasterdataToolBar.ui',self)
        else:
            pyside_dynamic.loadUi('Resources/ui/masterdata.ui',self)
        self.dbfilepath = 'Database/C3_DataBase.db'
        self.authorisedcapital = self.findChild(QtWidgets.QLineEdit, 'fill_Authcapital')
        self.noofmembers = self.findChild(QtWidgets.QLineEdit, 'fillMember')
        self.CIN = self.findChild(QtWidgets.QLineEdit, 'CIN')
        self.CompanyName = self.findChild(QtWidgets.QLineEdit, 'CompanyName')
        self.issuspended = self.findChild(QtWidgets.QLineEdit, 'fillSuspend')
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
        self.status = self.findChild(QtWidgets.QLineEdit, 'filLCompstatus')
        self.activestatus = self.findChild(QtWidgets.QLineEdit, 'fillActive')

        self.CINentry = self.findChild(QtWidgets.QLineEdit, 'CINField')
        self.Nameentry = self.findChild(QtWidgets.QLineEdit, 'NameField')
        self.PrefillButton = self.findChild(QtWidgets.QPushButton, 'Prefill')
        self.PrefillButton.clicked.connect(self.getMasterdata)
        
        self.show()

    def select_Company(self, data):
        self.dlg = QtWidgets.QDialog(self.Prefill)
        self.dlg.resize(471, 362)
        self.dlg.setStyleSheet("background-color: rgb(255, 255, 255);\n"
    "color: rgb(0, 0, 0);")
        self.dlg.setWindowTitle("Select a Company")
        self.dlg.gridLayout = QtWidgets.QGridLayout(self.dlg)
        self.dlg.gridLayout.setObjectName("gridLayout")
        self.dlg.label = QtWidgets.QLabel(self.dlg)
        self.dlg.label.setMaximumSize(QtCore.QSize(16777215, 12))
        self.dlg.label.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.dlg.label.setObjectName("label")
        self.dlg.label.setText("Multiple Companies Found!")
        self.dlg.gridLayout.addWidget(self.dlg.label, 0, 2, 1, 1)
        ButtonGroup=QtWidgets.QButtonGroup(self.dlg)
        for x in range(len(data['data'])):
            companyName=data['data'][x+1]['Name']
            Button= QtWidgets.QRadioButton(companyName)
            ButtonGroup.addButton(Button)
            self.dlg.gridLayout.addWidget(Button,x+1, 2, 1, 1)
        ButtonGroup.buttonClicked.connect(self.CompanyChoice)
        self.dlg.buttonBox = QtWidgets.QDialogButtonBox(self.dlg)
        self.dlg.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.dlg.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.dlg.buttonBox.setObjectName("buttonBox")
        self.dlg.gridLayout.addWidget(self.dlg.buttonBox, x+2, 2, 1, 1)
        self.dlg.buttonBox.accepted.connect(self.accept)
        self.dlg.buttonBox.rejected.connect(self.reject)
        self.dlg.show()

    def getMasterdata(self):
        test = 'Fail'
        if self.CINField.text()!='':
            if len(self.CINField.text())==21:
                test ="pass"
                data=getMasterdata.getMasterData(self.CINField.text().upper())
        elif self.CINField.text()=='' and self.NameField.text()!='':
            if len(self.NameField.text())>3:
                test = "pass"
                data=getMasterdata.getMasterData(self.NameField.text())
        else:
            self.Error("Please Enter valid CIN or Name before prefill")
        if test == "pass":
            if data['Status']=='Selection':
                self.selectionList = data
                self.select_Company(self.selectionList)
            elif data['Status']=='Success':
                self.JsonFile=data
                self.CINNum =data['data']['Masterdata']['company_cin']
                self.captcha()
                self.CINentry.setText(data['data']['Masterdata']['company_cin'])
                self.CIN.setText(data['data']['Masterdata']['company_cin'])
                self.Nameentry.setText(data['data']['Masterdata']['company_name'].title())
                self.CompanyName.setText(data['data']['Masterdata']['company_name'].title())
                self.roc.setText(data['data']['Masterdata']['company_roc'])
                self.registrationno.setText(data['data']['Masterdata']['company_registration_number'])
                self.category.setText(data['data']['Masterdata']['company_category'])
                self.subcategory.setText(data['data']['Masterdata']['company_subcategory'])
                self.companyclass.setText(data['data']['Masterdata']['company_class'])
                self.authorisedcapital.setText(data['data']['Masterdata']['company_authorized_capital'])
                self.paidupcapital.setText(data['data']['Masterdata']['company_paidup_capital'])
                self.noofmembers.setText(data['data']['Masterdata']['company_no_of_members'])
                self.dateofincorporation.setText(data['data']['Masterdata']['company_date_of_incorporation'])
                self.registeredaddress.setText(data['data']['Masterdata']['company_registered_address'].title())
                self.otheraddress.setText(data['data']['Masterdata']['company_other_than_regsitered_office'])
                self.companyemail.setText(data['data']['Masterdata']['company_email_id'])
                self.islisted.setText(data['data']['Masterdata']['company_listed'])
                self.activestatus.setText(data['data']['Masterdata']['company_active_status'])
                self.issuspended.setText(data['data']['Masterdata']['company_suspended'])
                self.status.setText(data['data']['Masterdata']['company_status'])
                if self.status.text()=='Strike Off':
                    Information = QtWidgets.QMessageBox.question(self, 'Information',
                                            f"{self.Nameentry.text()} is not an Active Company. ",
                                            QtWidgets.QMessageBox.Ok)
    def CompanyChoice(self,selected):
        for x in range(len(self.selectionList['data'])):
            if self.selectionList['data'][x+1]['Name'] == selected.text():
                self.Company_choice = self.selectionList['data'][x+1]['CIN']

    def accept(self):
        self.dlg.close()
        print(self.Company_choice)
        self.CINentry.setText(self.Company_choice)
        self.PrefillButton.click()

    def reject(self):
        self.dlg.close()
        
    def Error(self,Message):
        print(Message)

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




