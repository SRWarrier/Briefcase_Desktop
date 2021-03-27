from PySide2 import QtWidgets, QtUiTools,QtCore, QtGui
import sys
import HomePage
import os
import numpy as np
from PIL import Image
from functions import getMasterdatainExcel, getCaptcha, getSignatories, prefillDIN, PrefillCharge
from functions import Database_Manager as db
from COMPANIES import ClientManager
from functions import pyside_dynamic
from functions.Gdrive import Gdrive
import requests_html
import json
import hashlib
import webbrowser
import pickle

session = requests_html.HTMLSession()

class Ui(QtWidgets.QWidget):
    def __init__(self):
        super(Ui, self).__init__()
        pyside_dynamic.loadUi('Resources/ui/AddCompany.ui',self)
        self.is_shareholders_attached = False
        self.addFileWidget.setHidden(True)
        self.CINText = self.findChild(QtWidgets.QLineEdit, 'fillCIN')
        self.NameText = self.findChild(QtWidgets.QLineEdit, 'fillName')
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
        self.CINentry = self.findChild(QtWidgets.QLineEdit, 'CINField')
        self.Nameentry = self.findChild(QtWidgets.QLineEdit, 'NameField')
        self.PrefillButton = self.findChild(QtWidgets.QPushButton, 'Prefill')
        #Custom Context Menu
        self.HoldingTable.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.HoldingTable.customContextMenuRequested.connect(self.userTableContextMenu)

        self.SubsidiaryTable.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.SubsidiaryTable.customContextMenuRequested.connect(self.userTableContextMenu)

        self.AssociateTable.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.AssociateTable.customContextMenuRequested.connect(self.userTableContextMenu)

        self.ShareholderTable.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.ShareholderTable.customContextMenuRequested.connect(self.userTableContextMenu)

        self.contactDisplay.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.contactDisplay.customContextMenuRequested.connect(self.userTableContextMenu)
        
        # Click Mapping
        self.PrefillButton.clicked.connect(self.getMasterdata)
        self.AddPerson.clicked.connect(self.addrow)
        self.save = self.findChild(QtWidgets.QPushButton, 'Save')
        self.save.clicked.connect(self.AddMasterdata)
        self.addHolding.clicked.connect(self.addrow)
        self.addAssociate.clicked.connect(self.addrow)
        self.addSubsidiary.clicked.connect(self.addrow)
        self.addShareholder.clicked.connect(self.addrow)
        self.addFile.clicked.connect(self.addShareholdersfile)
        self.reset = self.findChild(QtWidgets.QPushButton, 'Reset')
        self.reset.clicked.connect(self.clearEntryFields)
        self.information.linkActivated.connect(self.filebrowse)
        self.removeFile.clicked.connect(self.removesharholderfile)
        self.addDocument.clicked.connect(self.getDocument)
        self.clientManager.clicked.connect(self.ClientManagerButton)


    def ClientManagerButton(self):
        sender = self.sender()
        parent = sender.parent().parent().parent()
        layout = parent.layout()
        clearLayout(layout)
        Home = parent.parent()
        titleCard = Home.findChild(QtWidgets.QLabel,"WidgetTitleText")
        titleCard.setStyleSheet("background-color: rgb(117,134,166); color: rgb(255,255,255)")
        titleCard.setText("Client Manager")
        CurrentWidget = ClientManager.Ui()
        parent.layout().addWidget(CurrentWidget, *(0,0))
        
    def removesharholderfile(self):
        self.information.setText('')
        self.is_shareholders_attached = False
        self.addFileWidget.setHidden(True)
        

    def addShareholdersfile(self):
        self.shareholderfile = QtWidgets.QFileDialog.getOpenFileName(self,"Open Shareholders List")[0]
        if self.shareholderfile!='':
            self.ShareholderTable.setRowCount(0)
            self.is_shareholders_attached = True
            filename = os.path.basename(self.shareholderfile)
            self.addFileWidget.setHidden(False)
            self.information.setText(f'You have added <a href = {repr(self.shareholderfile)}>{self.shareholderfile}</a> for shareholders')

    def getDocument(self):
        self.getDocumentWidget = QtWidgets.QWidget()
        pyside_dynamic.loadUi('Resources/ui/getDocument.ui',self.getDocumentWidget)
        self.getDocumentWidget.BrowseButton.clicked.connect(self.getDocumentFile)
        self.getDocumentWidget.Submit.clicked.connect(self.addDocumentWidget)
        self.getDocumentWidget.Cancel.clicked.connect(self.closeWidget)
        self.getDocumentWidget.show()

    def getDocumentFile(self):
        self.DocumFile = QtWidgets.QFileDialog.getOpenFileName(self,"Add Document")[0]
        self.getDocumentWidget.fileName.setText(os.path.basename(self.DocumFile))
        self.getDocumentWidget.activateWindow()
        

    def closeWidget(self):
        self.getDocumentWidget.close()
        
        
    def addDocumentWidget(self,Label="hello",Document="test"):
        Label = self.getDocumentWidget.DocLable.text()
        if Label=='':
            QtWidgets.QMessageBox.critical(self, "No document Label Set", "Please set a description to identify the document")
            self.getDocumentWidget.activateWindow()
        elif self.getDocumentWidget.fileName.text()=='':
            QtWidgets.QMessageBox.critical(self, "No File selected", "Please select a document")
            self.getDocumentWidget.activateWindow()
        else:
            Document = self.DocumFile
            self.getDocumentWidget.close()
            widget = QtWidgets.QWidget()
            layout = QtWidgets.QHBoxLayout()
            row = self.documentLayout.rowCount()
            file = QtWidgets.QLabel(Document)
            font = QtGui.QFont()
            font.setFamily("Open Sans")
            font.setPointSize(10)
            font.setStyleStrategy(QtGui.QFont.PreferAntialias)
            file.setFont(font)
            layout.addWidget(file)
            
            deleteButton = QtWidgets.QPushButton()
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(deleteButton.sizePolicy().hasHeightForWidth())
            deleteButton.setSizePolicy(sizePolicy)
            deleteButton.setMaximumSize(QtCore.QSize(120, 30))
            font = QtGui.QFont()
            font.setFamily("Open Sans")
            font.setPointSize(10)
            font.setStyleStrategy(QtGui.QFont.PreferAntialias)
            deleteButton.setFont(font)
            deleteButton.clicked.connect(self.deleteWidget)
            deleteButton.setStyleSheet("background-color: rgb(255, 0, 0);\n"
    "color: rgb(255, 255, 255);\n"
    "border-radius:10;")
            deleteButton.setText('Delete')
            layout.addWidget(deleteButton)

            label = QtWidgets.QLabel()
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(label.sizePolicy().hasHeightForWidth())
            label.setSizePolicy(sizePolicy)
            font = QtGui.QFont()
            font.setFamily("Open Sans")
            font.setPointSize(10)
            font.setStyleStrategy(QtGui.QFont.PreferAntialias)
            label.setFont(font)
            label.setText(Label)
            layout.setContentsMargins(100, 0, 0, 0)
            widget.setMinimumSize(QtCore.QSize(120, 30))
            widget.setLayout(layout)
            self.documentLayout.insertRow(row,label, widget)

    def deleteWidget(self):
        Confirmation = QtWidgets.QMessageBox.question(self, "Delete?", "Do you want to delete the document? \n[This will not delete the file]")
        if Confirmation.name.decode()=='Yes':
            widget = self.sender().parent()
            row = self.documentLayout.getWidgetPosition(widget)[0]
            #widget.setParent(None)
            self.documentLayout.removeRow(row)
            
    def userTableContextMenu(self, pos):
        Table =(self.sender())
        x,y = pos.x(), pos.y()
        it = Table.indexAt(pos) 
        if it is None: return
        menu = QtWidgets.QMenu()
        command = menu.addAction("Delete Row")
        action = menu.exec_(Table.viewport().mapToGlobal(pos))
        if action == command:
            Table.removeRow(it.row())

        
    def addrow(self):
        sender =(self.sender())
        if sender.objectName()=='addShareholder':
            if self.is_shareholders_attached:
                QtWidgets.QMessageBox.critical(self, "Conflict?", "You have added a file for shareholders. To enter in table, remove the file and proceed.")
                return None
            Tab=sender.parent().parent()
        else:
            Tab=sender.parent()
        Table = Tab.findChild(QtWidgets.QTableWidget)
        rowPosition = Table.rowCount()
        Table.insertRow(rowPosition)
        
    def select_Company(self, data):
        self.dlg = QtWidgets.QDialog()
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
                data=getMasterdatainExcel.getMasterdataExcel(CIN = self.CINField.text().upper())
        elif self.CINField.text()=='' and self.NameField.text()!='':
            if len(self.NameField.text())>3:
                test = "pass"
                data=getMasterdatainExcel.getMasterdataExcel(Name = self.NameField.text())
        else:
            self.Error("Please Enter valid CIN or Name before prefill")
        if test == "pass":
            if data['Status']=='Selection':
                self.selectionList = data
                self.select_Company(self.selectionList)
            elif data['Status']=='Success':
                self.JsonFile=data
                self.hashfile = hashlib.md5(json.dumps(data).encode('utf-8')).hexdigest()
                self.CINNum =data['data']['Masterdata']['CIN']
                self.CINentry.setText(data['data']['Masterdata']['CIN'])
                self.CINText.setText(data['data']['Masterdata']['CIN'])
                self.Nameentry.setText(data['data']['Masterdata']['Company / LLP Name'].title())
                self.NameText.setText(data['data']['Masterdata']['Company / LLP Name'].title())
                self.roc.setText(data['data']['Masterdata']['ROC Code'])
                self.registrationno.setText(str(data['data']['Masterdata']['Registration Number']))
                self.category.setText(data['data']['Masterdata']['Company Category'])
                self.subcategory.setText(data['data']['Masterdata']['Company SubCategory'])
                self.companyclass.setText(data['data']['Masterdata']['Class of Company '])
                self.authorisedcapital.setText(str(data['data']['Masterdata']['Authorised Capital(Rs)']))
                self.paidupcapital.setText(str(data['data']['Masterdata']['Paid up Capital(Rs)']))
                #self.noofmembers.setText(str(data['data']['Masterdata']['Number of Members(Applicable in case of company without Share Capital)']))
                self.dateofincorporation.setText(data['data']['Masterdata']['Date of Incorporation'])
                self.registeredaddress.setText(data['data']['Masterdata']['Registered Address'].title())
                #self.otheraddress.setText(data['data']['Masterdata']['company_other_than_regsitered_office'])
                self.companyemail.setText(data['data']['Masterdata']['Email Id'])
                self.islisted.setText(data['data']['Masterdata']['Whether Listed or not'])
##                self.activestatus.setText(data['data']['Masterdata']['company_active_status'])
##                self.issuspended.setText(data['data']['Masterdata']['company_suspended'])
                status = (data['data']['Masterdata']['Company Status(for efiling)'])
                if status=='Strike Off':
                    Information = QtWidgets.QMessageBox.question(self, 'Information',
                                            f"{self.Nameentry.text()} is not an Active Company. ",
                                            QtWidgets.QMessageBox.Ok)
                else:
                    self.captcha()
            else:
                print(data['Status'])
                QtWidgets.QMessageBox.information(None, 'Information', 'No Company found!!')

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
        sender =(self.sender())
        Home = getParent(sender,'HomePage')
        try:
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
            self.Toast = Home.findChild(QtWidgets.QFrame,"toasts")
            self.Toast.setHidden(not self.Toast.isHidden())
            self.Toast.layout().addWidget(self.captchaWindow)
        except:
            QtWidgets.QMessageBox.critical(self, "No Internet Connection", "Please check internet connection")


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
            self.Toast.setHidden(not self.Toast.isHidden())
            try:
                for x in range(len(self.signatoriesinfo['data'])):
                    DIN = self.signatoriesinfo['data'][x+1]['DIN/DPIN/PAN']
                    DINData = None
                    if len(DIN)==8:
                        DINData = prefillDIN.prefillDIN(DIN)
                        Signatory = self.signatoriesinfo['data'][x+1]
                    if isinstance(DINData,dict):
                        self.signatoriesinfo['data'][x+1]={**self.signatoriesinfo['data'][x+1],**DINData}
                self.signatoriesdetails = self.signatoriesinfo['data']
                self.DirectorInfo.setRowCount(len(self.signatoriesdetails))
                for x in range(len(self.signatoriesdetails)):
                    DirectInfo = list(self.signatoriesdetails[x+1].values())
                    if len(Signatory)<7:
                        if len(DirectInfo)>10:
                            DirectInfo.insert(2,DirectInfo[13])
                        else:
                            DirectInfo.insert(2,'-')
                    for y in range(len(self.signatoriesdetails[x+1])):
                        item = QtWidgets.QTableWidgetItem()
                        self.DirectorInfo.setItem(x, y, item)
                        item.setText(str(DirectInfo[y]))
                for col in range(self.DirectorInfo.columnCount()):
                    self.DirectorInfo.horizontalHeader().setSectionResizeMode(col, QtWidgets.QHeaderView.ResizeToContents)
                
            except:
                pass

    def AddMasterdata(self):
        #FieldDefinition
        try:
            companyCIN = self.JsonFile['data']['Masterdata']['CIN']
            companyName = self.JsonFile['data']['Masterdata']['Company / LLP Name'].title()
            authorisedcapital=self.authorisedcapital.text()
            paidupcapital=self.paidupcapital.text()
            category=self.category.text()
            subcategory=self.subcategory.text()
            registeredaddress=self.registeredaddress.text().title()
            dateofincorporation=self.dateofincorporation.text()
            companyclass=self.companyclass.text()
            companyemail=self.companyemail.text()
            islisted=self.islisted.text()
            roc=self.roc.text().lower().replace('roc-','Registrar of Companies, ').title().replace('Of','of')
            registrationno=self.registrationno.text()
            gst=self.GSTIN.text()
            pan=self.PAN.text()
            phone = self.fillTele.text()
            refer = self.fillReference.text()
            
            masterdatafields=[companyCIN,companyName,roc,registrationno,category,subcategory,
                              companyclass,authorisedcapital,paidupcapital,dateofincorporation,
                              registeredaddress,companyemail,islisted,pan,gst,phone,refer,
                              self.hashfile]

            db.updateMasterdata(masterdatafields)
            self.confirmSignatories()
            self.SavContacts()
            self.saveShareholders()
            self.saveHolding()
            self.saveSubsidiary()
            self.saveAssociate()
            self.saveDocuments()
            Message = QtWidgets.QMessageBox(self)
            Message.setWindowTitle("Information")
            Message.setText(f'{companyName} added to clients list.')
            Message.setModal(False)
            self.doneButtion = QtWidgets.QPushButton()
            self.doneButtion.setText('Done')
            self.doneButtion.clicked.connect(self.done)
            Message.addButton(self.doneButtion, QtWidgets.QMessageBox.YesRole)
            Message.show()
        except Exception as e:
            print(e)
            buttonReply = QtWidgets.QMessageBox.warning(self, "Prefill!?","Please use Prefill to fill in data.")
            if buttonReply == QtWidgets.QMessageBox.Yes:
                print('Yes clicked.')
            else:
                print('No clicked.')
       


    def confirmSignatories(self):
        SignatoriesList=[]
        for x in range(self.DirectorInfo.rowCount()):
                m=[]
                m.append(self.JsonFile['data']['Masterdata']['CIN'])
                for y in range(self.DirectorInfo.columnCount()):
                    try:
                        m.append(self.DirectorInfo.item(x,y).text())
                    except:
                        m.append('')
                SignatoriesList.append(tuple(m))
        db.updateSignatories(SignatoriesList)


    def saveShareholders(self):
        ShareholdersList=[]
        if self.is_shareholders_attached:
            m=[]
            m.append(self.JsonFile['data']['Masterdata']['CIN'])
            m.extend('-'*6)
            m.append(self.shareholderfile)
            ShareholdersList.append(tuple(m))
        else:
            for x in range(self.ShareholderTable.rowCount()):
                    m=[]
                    m.append(self.JsonFile['data']['Masterdata']['CIN'])
                    for y in range(self.ShareholderTable.columnCount()):
                        try:
                            m.append(self.ShareholderTable.item(x,y).text())
                        except:
                            m.append('')
                    if not m[1]=='':
                        m.append('')
                        ShareholdersList.append(tuple(m))
        if not len(ShareholdersList)==0:
            db.updateShareholders(ShareholdersList)

    def saveHolding(self):
        HoldingList=[]
        for x in range(self.HoldingTable.rowCount()):
                m=[]
                m.append(self.JsonFile['data']['Masterdata']['CIN'])
                for y in range(self.HoldingTable.columnCount()):
                    try:
                        m.append(self.HoldingTable.item(x,y).text())
                    except:
                        m.append('')
                if not m[1]=='':
                    HoldingList.append(tuple(m))
        if not len(HoldingList)==0:
            db.updateHolding(HoldingList)


    def saveSubsidiary(self):
        SubsidiaryList=[]
        for x in range(self.SubsidiaryTable.rowCount()):
                m=[]
                m.append(self.JsonFile['data']['Masterdata']['CIN'])
                for y in range(self.SubsidiaryTable.columnCount()):
                    try:
                        m.append(self.SubsidiaryTable.item(x,y).text())
                    except:
                        m.append('')
                if not m[1]=='':
                    SubsidiaryList.append(tuple(m))
        if not len(SubsidiaryList)==0:
            db.updateSubsidiary(SubsidiaryList)

    def saveAssociate(self):
        AssociateList=[]
        for x in range(self.AssociateTable.rowCount()):
                m=[]
                m.append(self.JsonFile['data']['Masterdata']['CIN'])
                for y in range(self.AssociateTable.columnCount()):
                    try:
                        m.append(self.AssociateTable.item(x,y).text())
                    except:
                        m.append('')
                if not m[1]=='':
                    AssociateList.append(tuple(m))
        if not len(AssociateList)==0:
            db.updateAssociate(AssociateList)

    def saveDocuments(self):
        DocumentList=[]
        for x in range(self.documentLayout.rowCount()):
                m=[]
                m.append(self.JsonFile['data']['Masterdata']['CIN'])
                label = self.documentLayout.itemAt(x,QtWidgets.QFormLayout.LabelRole).widget().text()
                m.append(label)
                widget = self.documentLayout.itemAt(x,QtWidgets.QFormLayout.FieldRole).widget()
                file = widget.findChild(QtWidgets.QLabel).text()
                m.append(file)
                DocumentList.append(tuple(m))
        if not len(DocumentList)==0:
            db.updateDocuments(DocumentList)
        

    def clearEntryFields(self):
        try:
            self.CINentry.setText('')
            self.CINText.setText('')
            self.Nameentry.setText('')
            self.NameText.setText('')
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
            self.PAN.setText('')
            self.GSTIN.setText('')
            self.status.setText('')
            self.phonemo.setText('')
            self.refer.setText('')
            self.DirectorInfo.setRowCount(0)
            self.contactDisplay.setRowCount(0)
            self.contactDisplay.setRowCount(1)
            self.tabWidget.setCurrentIndex(0)
        except:
            pass

        
    def SavContacts(self):
        ContactsList=[]
        for x in range(self.contactDisplay.rowCount()):
                m=[]
                m.append(self.JsonFile['data']['Masterdata']['CIN'])
                for y in range(self.contactDisplay.columnCount()):
                    try:
                        m.append(self.contactDisplay.item(x,y).text())
                    except:
                        m.append('')
                if not m[1]=='':
                    ContactsList.append(tuple(m))
        if not len(ContactsList)==0:
            db.updateContacts(ContactsList)

    def done(self):
        self.clearEntryFields()
        mainScreen = self.parent().parent()
        print(mainScreen)
        
    def filebrowse(self,text):
        os.startfile(text)

def getParent(widget, parent):
    for x in range(20):
        widParent = widget.parent()
        if widParent.objectName()==parent:
            return widParent
        else:
            widget = widParent
    return None     

def clearLayout(layout):
    while layout.count():
        child = layout.takeAt(0)
        if child.widget() is not None:
            child.widget().deleteLater()
        elif child.layout() is not None:
            clearLayout(child.layout())
