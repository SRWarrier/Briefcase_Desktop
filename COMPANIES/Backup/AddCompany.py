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


session = requests_html.HTMLSession()

class Ui(QtWidgets.QWidget):
    def __init__(self):
        super(Ui, self).__init__()
        pyside_dynamic.loadUi('../Resources/ui/AddClient.ui',self)
        self.dbfilepath = '../../Database/C3_DataBase.db'
        self.InFrame = self.findChild(QtWidgets.QGridLayout, 'FormLayout')
        self.authorisedcapital = self.findChild(QtWidgets.QLineEdit, 'fill_Authcapital')
        self.noofmembers = self.findChild(QtWidgets.QLineEdit, 'fillMember')
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
        self.PAN = self.findChild(QtWidgets.QLineEdit, 'PanFill')
        self.GSTIN = self.findChild(QtWidgets.QLineEdit, 'GSTFill')

        self.CINentry = self.findChild(QtWidgets.QLineEdit, 'CINField')
        self.Nameentry = self.findChild(QtWidgets.QLineEdit, 'NameField')
        self.PrefillButton = self.findChild(QtWidgets.QPushButton, 'Prefill')
        self.PrefillButton.clicked.connect(self.getMasterdata)
        
        self.save = self.findChild(QtWidgets.QPushButton, 'Save')
        self.save.clicked.connect(self.AddMasterdata)

        self.reset = self.findChild(QtWidgets.QPushButton, 'Reset')
        self.reset.clicked.connect(self.clearEntryFields)
        
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
                self.CINentry.setText(data['data']['Masterdata']['company_cin'])
                self.Nameentry.setText(data['data']['Masterdata']['company_name'].title())
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

    def AddMasterdata(self):
        #FieldDefinition
        try:
            companyCIN = self.JsonFile['data']['Masterdata']['company_cin']
            companyName = self.JsonFile['data']['Masterdata']['company_name'].title()
            authorisedcapital=self.authorisedcapital.text()
            noofmembers=self.noofmembers.text()
            issuspended=self.issuspended.text()
            companyemail=self.companyemail.text()
            dateofincorporation=self.dateofincorporation.text()
            roc=self.roc.text().lower().replace('roc-','Registrar of Companies, ').title().replace('Of','of')
            registeredaddress=self.registeredaddress.text().title()
            registrationno=self.registrationno.text()
            islisted=self.islisted.text()
            paidupcapital=self.paidupcapital.text()
            category=self.category.text()
            companyclass=self.companyclass.text()
            otheraddress=self.otheraddress.text().title()
            subcategory=self.subcategory.text()
            status=self.status.text()
            activestatus=self.activestatus.text()
            gst=self.GSTIN.text()
            pan=self.PAN.text()

            masterdatafields=[companyCIN,companyName,roc,registrationno,category,subcategory,
                              companyclass,authorisedcapital,paidupcapital,noofmembers,dateofincorporation,
                              registeredaddress,otheraddress,companyemail,islisted,activestatus,
                              issuspended,status,pan,gst]

            db.updateMasterdata(masterdatafields)
            Message = QtWidgets.QMessageBox(self)
            Message.setWindowTitle("Information")
            Message.setText(f'{companyName} has been added to the database')
            Message.setModal(False)
            self.AddSignatoriesButtion = QtWidgets.QPushButton()
            self.AddSignatoriesButtion.setText('Add Signatories')
            self.AddSignatoriesButtion.clicked.connect(self.getCaptcha)
            Message.addButton(self.AddSignatoriesButtion, QtWidgets.QMessageBox.YesRole)
            Message.show()
        except Exception as e:
            print(e)
            buttonReply = QtWidgets.QMessageBox.warning(self, "Prefill!?","Please use Prefill to fill in data.")
##        if buttonReply == QtWidgets.QMessageBox.Yes:
##            print('Yes clicked.')
##        else:
##            print('No clicked.')
       

        
    def updateDatabase(self):
        if self.status.text()=='Strike Off':
            Information = QtWidgets.QMessageBox.question(self, 'Information',
                                    f"{self.Nameentry.text()} has been Struk Off and cannot be added to Client List",
                                    QtWidgets.QMessageBox.Ok)

        else:
            try:
                if self.aliasconfirmed:
                    masterdata = self.JsonFile['data']['Masterdata']
                    msdata = masterdata.values()
                    db.updateMasterdata(list(msdata))
##                    homefolder = os.getcwd()
##                    os.chdir('Tools/Gdrive')
##                    drive =Gdrive.Authenticate()
##                    Gdrive.updateFile(drive,self.dbfilepath,'C3 Software')
##                    os.chdir(homefolder)
                    Message = QtWidgets.QMessageBox(self)
                    Message.setWindowTitle("Information")
                    Message.setText('Database Updated')
                    self.Backmodal = QtWidgets.QPushButton()
                    self.Backmodal.setText("Back to Home")
                    self.Backmodal.clicked.connect(self.GobackToHomePage)
                    self.AddNew = QtWidgets.QPushButton()
                    self.AddNew.setText("Add Another")
                    self.AddNew.clicked.connect(self.clearEntryFields)
                    Message.addButton(self.AddNew, QtWidgets.QMessageBox.YesRole)
                    Message.addButton(self.Backmodal, QtWidgets.QMessageBox.NoRole)
                    Message.show()
                    

                    print('db updated')
                else:
                    masterdata = self.JsonFile['data']['Masterdata']
                    msdata = masterdata.values()
                    db.updateMasterdata(list(msdata))
                    signatories = self.captcha_ui.returnDict()['data']
                    DirectorsList =[]
                    for x in range(len(signatories)):
                        tempdict =[self.JsonFile['data']['Masterdata']['CIN']]
                        for item in signatories[x+1].values():
                            tempdict.append(item)
                        tempdict.insert(3,'')
                        DirectorsList.append(tuple(tempdict))
                    db.updateSignatories(DirectorsList)
##                    homefolder = os.getcwd()
##                    os.chdir('Tools/Gdrive')
##                    drive =Gdrive.Authenticate()
##                    Gdrive.updateFile(drive,self.dbfilepath,'C3 Software')
##                    os.chdir(homefolder)
                    Message = QtWidgets.QMessageBox(self)
                    Message.setWindowTitle("Information")
                    Message.setText('Database Updated')
                    self.Backmodal = QtWidgets.QPushButton()
                    self.Backmodal.setText("Back to Home")
                    self.Backmodal.clicked.connect(self.GobackToHomePage)
                    self.AddNew = QtWidgets.QPushButton()
                    self.AddNew.setText("Add Another")
                    self.AddNew.clicked.connect(self.clearEntryFields)
                    Message.addButton(self.AddNew, QtWidgets.QMessageBox.YesRole)
                    Message.addButton(self.Backmodal, QtWidgets.QMessageBox.NoRole)
                    Message.show()
                
            except Exception as e:
                print(e)


    
                   


    

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

    def clearEntryFields(self):
        try:
            self.CINentry.setText('')
            self.Nameentry.setText('')
            self.roc.setText('')
            self.registrationno.setText('')
            self.category.setText('')
            self.subcategory.setText('')
            self.companyclass.setText('')
            self.authorisedcapital.setText('')
            self.paidupcapital.setText('')
            self.noofmembers.setText('')
            self.dateofincorporation.setText('')
            self.registeredaddress.setText('')
            self.otheraddress.setText('')
            self.companyemail.setText('')
            self.islisted.setText('')
            self.activestatus.setText('')
            self.issuspended.setText('')
            self.lastagm.setText('')
            self.lastbalancesheet.setText('')
            self.status.setText('')
            self.aliasconfirmed=False
        except:
            pass


    def getCaptcha(self):
        self.captchawindow = QtWidgets.QDialog(self)
        self.captcha_ui = Ui_Captcha()
        self.captcha_ui.setupUi(self.captchawindow,self.JsonFile,self)
        self.captchawindow.show()

    def openSignatories(self,jsonFile):
        if self.status.text()=='Strike Off':
            Information = QtWidgets.QMessageBox.question(self, 'Information',
                                    f"{self.Nameentry.text()} has no signatories ",
                                    QtWidgets.QMessageBox.Ok)
         

class SignatoriesManager(QtWidgets.QWidget):
    def __init__(self):
        super(SignatoriesManager, self).__init__()
        pyside_dynamic.loadUi('../Resources/ui/Signatories.ui', self)
        self.DirectorInfo = self.findChild(QtWidgets.QTableWidget, 'DirectorInfo')
        self.savebutton = self.findChild(QtWidgets.QPushButton, 'savebutton')

        
        
class Ui_Captcha(object):
    def setupUi(self, Captcha, data,mainWindow):
        self.captchaWindow = Captcha
        self.mainWindow = mainWindow
        self.JsonFile = data
        pyside_dynamic.loadUi('../Resources/ui/captcha.ui',self.captchaWindow)
        self.captchaWindow.move(300,300)
        self.CINNum = data['data']['Masterdata']['company_cin']
        self.captchaView = self.captchaWindow.findChild(QtWidgets.QLabel, 'captchaview')
        self.getCaptcha()
        self.CaptchaInput = self.captchaWindow.findChild(QtWidgets.QLineEdit, 'captchainput')
        self.SubmitButton = self.captchaWindow.findChild(QtWidgets.QPushButton, 'submit')
        self.SubmitButton.clicked.connect(self.getSignatories)
        self.refreshButton = self.captchaWindow.findChild(QtWidgets.QPushButton, 'refresh')
        self.refreshButton.clicked.connect(self.getCaptcha)


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
            clearLayout(self.mainWindow.InFrame)
            self.signatories_ui = SignatoriesManager()
            self.mainWindow.InFrame.addWidget(self.signatories_ui, *(0,0))
            try:
                for x in range(len(self.signatoriesinfo['data'])):
                    DIN = self.signatoriesinfo['data'][x+1]['DIN/DPIN/PAN']
                    DINData = prefillDIN.prefillDIN(DIN)
                    if isinstance(DINData,dict):
                        self.signatoriesinfo['data'][x+1]={**self.signatoriesinfo['data'][x+1],**DINData}
                self.signatoriesdetails = self.signatoriesinfo['data']
                self.signatories_ui.DirectorInfo.setRowCount(len(self.signatoriesdetails))
                self.signatories_ui.CompanyName.setText(self.JsonFile['data']['Masterdata']['company_name'])
                for x in range(len(self.signatoriesdetails)):
                    DirectInfo = list(self.signatoriesdetails[x+1].values())
                    for y in range(len(self.signatoriesdetails[x+1])):
                        item = QtWidgets.QTableWidgetItem()
                        self.signatories_ui.DirectorInfo.setItem(x, y, item)
                        try:
                            item.setText(str(DirectInfo[y].title()))
                        except:
                            item.setText(str(DirectInfo[y]))
                self.signatories_ui.DirectorInfo.resizeRowsToContents()    
            except IndexError as e:
                print(e)
                pass
            
            self.signatories_ui.savebutton.clicked.connect(self.confirmSignatories)
            self.signatories_ui.show()

    def confirmSignatories(self):
        SignatoriesList=[]
        for x in range(self.signatories_ui.DirectorInfo.rowCount()):
                m=[]
                m.append(self.JsonFile['data']['Masterdata']['company_cin'])
                for y in range(self.signatories_ui.DirectorInfo.columnCount()):
                    try:
                        m.append(self.signatories_ui.DirectorInfo.item(x,y).text())
                    except:
                        m.append('')
                SignatoriesList.append(tuple(m))
        db.updateSignatories(SignatoriesList)
        Message = QtWidgets.QMessageBox(self.signatories_ui)
        Message.setWindowTitle("Information")
        Message.setText(f'Signatories has been added to the database')
        Message.setModal(False)
        self.AddSignatoriesButtion = QtWidgets.QPushButton()
        self.AddSignatoriesButtion.setText('Add Contacts')
        self.AddSignatoriesButtion.clicked.connect(self.addContacts)
        Message.addButton(self.AddSignatoriesButtion, QtWidgets.QMessageBox.YesRole)
        Message.show()

        
    def addContacts(self):
        clearLayout(self.mainWindow.InFrame)
        ContactsView = QtWidgets.QWidget()
        pyside_dynamic.loadUi('../Resources/ui/contactPerson.ui',ContactsView)
        self.contactDisplay = ContactsView.findChild(QtWidgets.QTableWidget, 'Display')
        self.SaveButton = ContactsView.findChild(QtWidgets.QPushButton, 'Save')
        self.SaveButton.clicked.connect(self.SavContacts)
        self.AddButton = ContactsView.findChild(QtWidgets.QPushButton, 'AddPerson')
        self.AddButton.clicked.connect(self.addrow)
        self.mainWindow.InFrame.addWidget(ContactsView, *(0,0))
        ContactsView.show()

    def addrow(self):
        rowPosition = self.contactDisplay.rowCount()
        self.contactDisplay.insertRow(rowPosition)
        
    def SavContacts(self):
        ContactsList=[]
        for x in range(self.contactDisplay.rowCount()):
                m=[]
                m.append(self.JsonFile['data']['Masterdata']['company_cin'])
                for y in range(self.contactDisplay.columnCount()):
                    try:
                        m.append(self.contactDisplay.item(x,y).text())
                    except:
                        m.append('')
                if not m[1]=='':
                    ContactsList.append(tuple(m))
        if not len(m)==0:
            db.updateContacts(ContactsList)
        Message = QtWidgets.QMessageBox(self.contactDisplay)
        Message.setWindowTitle("Information")
        if len(m)==0:
            Message.setText('Contact List empty. No contact added to the Company')
        else:
            Message.setText(f'Contacts has been added to the database')
        Message.setModal(False)
        self.doneButtion = QtWidgets.QPushButton()
        self.doneButtion.setText('Done')
        self.doneButtion.clicked.connect(self.done)
        Message.addButton(self.doneButtion, QtWidgets.QMessageBox.YesRole)
        Message.show()

    def done(self):
        clearLayout(self.mainWindow.InFrame)
        self.mainWindow.InFrame.addWidget(Ui(), *(0,0))
        
        
    def returnDict(self):
        return self.signatoriesinfo

def clearLayout(layout):
    while layout.count():
        child = layout.takeAt(0)
        if child.widget() is not None:
            child.widget().deleteLater()
        elif child.layout() is not None:
            clearLayout(child.layout())
