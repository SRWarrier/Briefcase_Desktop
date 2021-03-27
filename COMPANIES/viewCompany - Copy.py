from PySide2 import QtWidgets, QtUiTools,QtCore, QtGui
import sys
import os
from functions import pyside_dynamic
#from functions.Gdrive import Gdrive
import requests_html
import sqlite3
import pandas as pd
import datetime
from dateutil.relativedelta import relativedelta
from functions import getDirDetails,getCaptcha,getCharges
from COMPANIES import ClientManager
import pickle


session = requests_html.HTMLSession()

class Ui(QtWidgets.QWidget):
    def __init__(self,DirectorDIN):
        super(Ui, self).__init__()
        pyside_dynamic.loadUi('../Resources/ui/viewCompany.ui',self)
        with open('Config','rb') as f:
            Config = pickle.loads(f.read())
            f.close()
        self.home = self.parent().parent()
        print(self.home)
        self.CIN = DirectorDIN
        self.dbfilepath = os.path.join(Config['Database'],'C3_DataBase.db')
        self.conn = sqlite3.connect(self.dbfilepath)
        self.cur = self.conn.cursor()
        self.CompanyBasicInfo = self.cur.execute(f'SELECT * from Masterdata WHERE company_cin = "{DirectorDIN}"').fetchall()[0]
        self.CompanyDirectorsInfo = self.cur.execute(f'SELECT * from Signatories WHERE company_cin = "{DirectorDIN}"').fetchall()
        self.CompanyShareholdersInfo = self.cur.execute(f'SELECT * from Shareholders WHERE company_cin = "{DirectorDIN}"').fetchall()
        self.CompanyAssociateCompaniesInfo = self.cur.execute(f'SELECT * from AssociateCompanies WHERE company_cin = "{DirectorDIN}"').fetchall()
        self.CompanySubsidiaryCompaniesInfo = self.cur.execute(f'SELECT * from SubsidiaryCompanies WHERE company_cin = "{DirectorDIN}"').fetchall()
        self.CompanyDocuments = self.cur.execute(f'SELECT * from documents WHERE company_cin = "{DirectorDIN}"').fetchall()
        self.CompanyHoldingCompaniesInfo = self.cur.execute(f'SELECT * from HoldingCompanies WHERE company_cin = "{DirectorDIN}"').fetchall()
        self.CompanyContactsInfo = self.cur.execute(f'SELECT * from Contacts WHERE company_cin = "{DirectorDIN}"').fetchall()
        self.CompanyNameTitle.setText(self.CompanyBasicInfo[1].upper())
        if len(self.CompanyBasicInfo)>0:
            self.Sidebar.layout().addWidget(self.createButton('Basic Info',self.BasicInfo))
        if len(self.CompanyDirectorsInfo)>0:
            self.Sidebar.layout().addWidget(self.createButton('Signatories',self.Signatories))
        if len(self.CompanyShareholdersInfo)>0:
            self.Sidebar.layout().addWidget(self.createButton('Shareholders',self.Shareholders))
        if len(self.CompanyHoldingCompaniesInfo)>0:
            self.Sidebar.layout().addWidget(self.createButton('Holding Cos.',self.Holding))
        if len(self.CompanySubsidiaryCompaniesInfo)>0:
            self.Sidebar.layout().addWidget(self.createButton('Subsidiaries', self.Subsidiary))
        if len(self.CompanyAssociateCompaniesInfo)>0:
            self.Sidebar.layout().addWidget(self.createButton('Associate Cos.', self.Associate))
        if len(self.CompanyContactsInfo)>0:
            self.Sidebar.layout().addWidget(self.createButton('Contacts',self.Contacts))
        print(self.CompanyDocuments)
        if len(self.CompanyDocuments)>0:
            self.Sidebar.layout().addWidget(self.createButton('Documents',self.Documents))
        self.Sidebar.layout().addWidget(self.createButton('Charges', self.Charges))
        self.Sidebar.layout().addWidget(self.createButton('Filings', self.Filings))
        self.Sidebar.layout().addWidget(self.createButton('Activities', self.Activities))
        self.Sidebar.layout().addItem(QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding))
        self.Sidebar.layout().addWidget(self.createButton('Client Manager', self.ClientManagerButton))
        self.BasicInfo()


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
        
        
    def createButton(self,Text,Fn):
        button = QtWidgets.QPushButton()
        button.setStyleSheet("background-color: rgb(179, 55, 113);border-radius:10; color: rgb(255,255,255)")
        button.setText(Text.upper())
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        button.setSizePolicy(sizePolicy)
        button.setMinimumSize(QtCore.QSize(0, 30))
        button.setMaximumSize(QtCore.QSize(1665476, 30))
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        font.setPointSize(11)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        button.setFont(font)
        button.clicked.connect(Fn)
        return button

    def BasicInfo(self):
        Widget = QtWidgets.QWidget()
        pyside_dynamic.loadUi('../Resources/ui/CompanyBasicInfo.ui',Widget)
        Widget.CIN.setText(self.CompanyBasicInfo[0])
        Widget.CompanyName.setText(self.CompanyBasicInfo[1])
        Widget.ROC.setText(self.CompanyBasicInfo[2])
        Widget.RegNo.setText(self.CompanyBasicInfo[3])
        Widget.Category.setText(self.CompanyBasicInfo[4])
        Widget.SubCategory.setText(self.CompanyBasicInfo[5])
        Widget.Class.setText(self.CompanyBasicInfo[6])
        Widget.AuthorizedCapital.setText(self.CompanyBasicInfo[7])
        Widget.PaidupCapital.setText(self.CompanyBasicInfo[8])
        DOI = self.CompanyBasicInfo[9]
        dtDate = datetime.datetime.strptime(DOI,"%d/%m/%Y")
        Datedelta = relativedelta(datetime.datetime.now(),dtDate)
        Widget.DateofIncorporation.setText(DOI+f"  ({Datedelta.years} Years, {Datedelta.months} Months, {Datedelta.days} Days)")
        Widget.RegisteredAddress.setText(self.CompanyBasicInfo[10])
        Widget.emailID.setText(self.CompanyBasicInfo[11])
        Widget.Listed.setText(self.CompanyBasicInfo[12]) 
        Widget.PAN.setText(self.CompanyBasicInfo[13])
        Widget.GST.setText(self.CompanyBasicInfo[14])
        Widget.TelePhone.setText(self.CompanyBasicInfo[15])
        Widget.ReferredBy.setText(self.CompanyBasicInfo[16])
        Widget.LastUpdate.setText(self.CompanyBasicInfo[-1])
        self.DisplayArea.layout().addWidget(Widget,*(0,0))
    
    def Signatories(self):
        self.SignaWidget = QtWidgets.QWidget()
        pyside_dynamic.loadUi('../Resources/ui/DirectorsInfo.ui',self.SignaWidget)
        self.SignaWidget.ExtendedInfo.setHidden(True)
        Count=0
        for Director in self.CompanyDirectorsInfo:
            DirectorBanner = self.DirectorBanner(Count,Director[2],Director[1],Director[4])
            self.SignaWidget.BasicInfoWindow.layout().addWidget(DirectorBanner)
            Count+=1
        self.SignaWidget.BasicInfoWindow.layout().addItem(QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding))
        self.DisplayArea.layout().addWidget(self.SignaWidget,*(0,0))

    def hideExtendWindow(self):
        self.SignaWidget.ExtendedInfo.setHidden(True)

    def Shareholders(self):
        if not self.CompanyShareholdersInfo[0][7]!='':
            tablist = ['equity']
            Widget = QtWidgets.QWidget()
            pyside_dynamic.loadUi('../Resources/ui/ShareholdersTable.ui',Widget)
            SecurDict = {}
            for security in self.CompanyShareholdersInfo:
                try:
                        Key = security[6].lower()
                        TempList = SecurDict[Key]
                        TempList.append(security)
                        SecurDict[Key] = TempList
                except Exception as e:
                        print(e)
                        TempDict = [security]
                        SecurDict[Key] = TempDict
            for security in SecurDict.keys():
                if security.lower()!='equity' and security.lower() not in tablist:
                    Table = self.createShareholderTable()
                    Widget.TabWidget.addTab(Table,security)
                    Widget.TabWidget.setTabText(len(tablist),security.upper())
                    tablist.append(security.lower())
                currentTable = Widget.TabWidget.widget(tablist.index(security.lower())).findChild(QtWidgets.QTableWidget)
                currentTable.setRowCount(len(SecurDict[security]))
                for x in range(len(SecurDict[security])):
                    for y in range(len(SecurDict[security][x])-2):
                        item = QtWidgets.QTableWidgetItem()
                        currentTable.setItem(x, y, item)
                        item.setText(str(SecurDict[security][x][y+1]))
                currentTable.resizeRowsToContents() 
            self.DisplayArea.layout().addWidget(Widget,*(0,0))
        else:
            try:
                os.startfile(self.CompanyShareholdersInfo[0][7])
            except:
                print("File Deleted?")

    def Holding(self):
        Widget = QtWidgets.QWidget()
        pyside_dynamic.loadUi('../Resources/ui/HSATable.ui',Widget)
        Widget.Table.setRowCount(len(self.CompanyHoldingCompaniesInfo))
        for x in range(len(self.CompanyHoldingCompaniesInfo)):
                for y in range(len(self.CompanyHoldingCompaniesInfo[x])):
                    if not y+1==len(self.CompanyHoldingCompaniesInfo[x]):
                        item = QtWidgets.QTableWidgetItem()
                        Widget.Table.setItem(x, y, item)
                        item.setText(str(self.CompanyHoldingCompaniesInfo[x][y+1]))
                        Widget.Table.resizeRowsToContents() 
        self.DisplayArea.layout().addWidget(Widget,*(0,0))

    def Subsidiary(self):
        Widget = QtWidgets.QWidget()
        pyside_dynamic.loadUi('../Resources/ui/HSATable.ui',Widget)
        Widget.Table.setRowCount(len(self.CompanySubsidiaryCompaniesInfo))
        for x in range(len(self.CompanySubsidiaryCompaniesInfo)):
                for y in range(len(self.CompanySubsidiaryCompaniesInfo[x])):
                    if not y+1==len(self.CompanySubsidiaryCompaniesInfo[x]):
                        item = QtWidgets.QTableWidgetItem()
                        Widget.Table.setItem(x, y, item)
                        item.setText(str(self.CompanySubsidiaryCompaniesInfo[x][y+1]))
                        Widget.Table.resizeRowsToContents() 
        self.DisplayArea.layout().addWidget(Widget,*(0,0))

    def Associate(self):
        Widget = QtWidgets.QWidget()
        pyside_dynamic.loadUi('../Resources/ui/HSATable.ui',Widget)
        Widget.Table.setRowCount(len(self.CompanyAssociateCompaniesInfo))
        for x in range(len(self.CompanyAssociateCompaniesInfo)):
                for y in range(len(self.CompanyAssociateCompaniesInfo[x])):
                    if not y+1==len(self.CompanyAssociateCompaniesInfo[x]):
                        item = QtWidgets.QTableWidgetItem()
                        Widget.Table.setItem(x, y, item)
                        item.setText(str(self.CompanyAssociateCompaniesInfo[x][y+1]))
                        Widget.Table.resizeRowsToContents() 
        self.DisplayArea.layout().addWidget(Widget,*(0,0))

    def Documents(self):
        self.DocumentWidget = QtWidgets.QWidget()
        self.doculayout = QtWidgets.QVBoxLayout()
        self.DocumentWidget.setLayout(self.doculayout)
        for x in range(len(self.CompanyDocuments)):
            document = self.CompanyDocuments[x]
            self.docuBar(document[1],str(x))
        self.doculayout.addItem(QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding))
        self.DisplayArea.layout().addWidget(self.DocumentWidget,*(0,0))

    def Contacts(self):
        Widget = QtWidgets.QWidget()
        pyside_dynamic.loadUi('../Resources/ui/CompanyBasicInfo.ui',Widget)
        self.DisplayArea.layout().addWidget(Widget,*(0,0))

    def Charges(self):
        self.chargesWidget = QtWidgets.QWidget()
        pyside_dynamic.loadUi('../Resources/ui/ChargesTable.ui',self.chargesWidget)
        self.captcha()
        

    def Filings(self):
        ScrollArea = QtWidgets.QScrollArea()
        filingvbox = QtWidgets.QVBoxLayout()
        self.ToolBoxWidget = QtWidgets.QToolBox()
        YOI = datetime.datetime.strptime(self.CompanyBasicInfo[9],'%d/%m/%Y').year
        YOI = YOI if YOI>2006 else 2006
        CurrentYear = datetime.datetime.now().year
        YearDiff =  CurrentYear- YOI
        for delta in range(YearDiff+1):
            year = str(CurrentYear-delta)
            label = QtWidgets.QLabel()
            self.ToolBoxWidget.addItem(label, year)
        ScrollArea.setWidget(self.ToolBoxWidget)
        self.ToolBoxWidget.currentChanged.connect(self.test)
        ScrollArea.setWidgetResizable(True)
        self.DisplayArea.layout().addWidget(ScrollArea,*(0,0))

    def test(self,x):
        Widget = self.ToolBoxWidget.widget(x)
        Widget.setText('Hello')
        
    def Activities(self):
        Widget = QtWidgets.QWidget()
        pyside_dynamic.loadUi('../Resources/ui/CompanyBasicInfo.ui',Widget)
        self.DisplayArea.layout().addWidget(Widget,*(0,0))

    def viewExtendedFn(self):
        sender =(self.sender())
        self.SignaWidget.hideExtend.clicked.connect(self.hideExtendWindow)
        self.DirectorsList = self.CompanyDirectorsInfo[int(sender.objectName())][1:]
        labelText = ['DIN', 'Name', 'Address', 'Designation'
                     ,'Date of Appointment','DSC registered', 'DSC expiry Date',
                     'First Name', 'Middle Name', 'Last Name','Gender', "Father's First Name",
                     "Father's Middle Name", "Father's Last Name", 'Present Address',
                     'Permanent Address', 'Mobile Number', 'Email ID',
                     'Nationality', 'Place of Birth', 'Occupation', 'Date of Birth',
                     'Age' , 'Educational Qualification', 'Aadhar Number', 'PAN', 'Passport',
                     'Other ID','Alias']
        self.SignaWidget.ExtendedInfo.setHidden(False)
        self.SignaWidget.AssociatedCompany_2.setRowCount(0)
        self.SignaWidget.getAssociatedData.clicked.connect(self.getDirectorsCompaniesData)
        layout = self.SignaWidget.extendedWindowPersonal.layout()
        clearLayout(layout)
        for x in range(len(self.DirectorsList)):
            info = QtWidgets.QLabel()
            info.setText(self.DirectorsList[x])
            label = QtWidgets.QLabel()
            label.setText(labelText[x])
            layout.insertRow(layout.rowCount(),label, info)

    def getDirectorsCompaniesData(self):
        if self.DirectorsList[0].isnumeric():
            DirCompanies = getDirDetails.getDirdetails(self.DirectorsList[0])
            self.SignaWidget.AssociatedCompany_2.setRowCount(len(DirCompanies['data']))
            for x in range(len(DirCompanies['data'])):
                CompInfo = list(DirCompanies['data'][x+1].values())
                for y in range(len(DirCompanies['data'][x+1])):
                    item = QtWidgets.QTableWidgetItem()
                    self.SignaWidget.AssociatedCompany_2.setItem(x, y, item)
                    item.setText(str(CompInfo[y]))
            self.SignaWidget.AssociatedCompany_2.resizeRowsToContents()
            self.SignaWidget.AssociatedCompany_2.resizeColumnsToContents()
            
            
        
        

    def DirectorBanner(self, Count, Name, DIN, Designation):
        DirectorBanner = QtWidgets.QFrame()
        DirectorBanner.setMaximumSize(QtCore.QSize(16777215, 80))
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        font.setPointSize(10)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        DirectorBanner.setFont(font)
        DirectorBanner.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border-radius:30;\n""border: 1px solid rgb(212, 212, 212);\n""border-width: 2px;")
        hLayout = QtWidgets.QHBoxLayout(DirectorBanner)
        hLayout.setContentsMargins(0, 0, 0, 0)
        DirectorName = QtWidgets.QLabel(DirectorBanner)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(DirectorName.sizePolicy().hasHeightForWidth())
        DirectorName.setSizePolicy(sizePolicy)
        DirectorName.setWordWrap(True)
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        font.setPointSize(10)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        DirectorName.setFont(font)
        DirectorName.setAlignment(QtCore.Qt.AlignCenter)
        DirectorName.setText(Name)
        DirectorName.setObjectName('DirectorName')
        DirectorName.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
        hLayout.addWidget(DirectorName)
        DirectorDIN = QtWidgets.QLabel()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(DirectorDIN.sizePolicy().hasHeightForWidth())
        DirectorDIN.setSizePolicy(sizePolicy)
        DirectorDIN.setMaximumSize(QtCore.QSize(150, 16777215))
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        font.setPointSize(10)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        DirectorDIN.setFont(font)
        DirectorDIN.setObjectName('DirectorDIN')
        DirectorDIN.setAlignment(QtCore.Qt.AlignCenter)
        DirectorDIN.setText(DIN)
        DirectorDIN.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
        hLayout.addWidget(DirectorDIN)
        DirectorDesi = QtWidgets.QLabel()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(DirectorDesi.sizePolicy().hasHeightForWidth())
        DirectorDesi.setSizePolicy(sizePolicy)
        DirectorDesi.setWordWrap(True)
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        font.setPointSize(10)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        DirectorDesi.setFont(font)
        DirectorDesi.setAlignment(QtCore.Qt.AlignCenter)
        DirectorDesi.setText(Designation)
        if Designation.lower()=='wholetime director':
            DirectorDesi.setStyleSheet("background color: rgb(171,210,250)")
        elif Designation.lower()=='managing director':
            DirectorDesi.setStyleSheet("background color: rgb(118,146,255); color: rgb(255,255,255)")
        elif Designation.lower()=='company secretary':
            DirectorDesi.setStyleSheet("background color: rgb(9,21,64); color: rgb(255,255,255)")
        DirectorDesi.setObjectName('DirectorDesi')
        DirectorDesi.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
        hLayout.addWidget(DirectorDesi)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Minimum)
        hLayout.addItem(spacerItem)
        MoreInfo = QtWidgets.QPushButton(DirectorBanner)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MoreInfo.sizePolicy().hasHeightForWidth())
        MoreInfo.setSizePolicy(sizePolicy)
        MoreInfo.setMaximumSize(QtCore.QSize(120, 16777215))
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        font.setPointSize(10)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        MoreInfo.setFont(font)
        MoreInfo.setStyleSheet("background-color: rgb(85, 255, 255);")
        MoreInfo.setText('More Info')
        MoreInfo.setObjectName(str(Count))
        MoreInfo.clicked.connect(self.viewExtendedFn)
        hLayout.addWidget(MoreInfo)
        return DirectorBanner

    def createShareholderTable(self):
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QGridLayout(widget)
        table = QtWidgets.QTableWidget()
        font = QtGui.QFont()
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        table.setFont(font)
        table.setAlternatingRowColors(True)
        table.setColumnCount(5)
        table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        item.setText("Name")
        table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("Father\'s Name")
        table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("Address")
        table.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("Nationality")
        table.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("No of Shares")
        table.setHorizontalHeaderItem(4, item)
        layout.addWidget(table, 0, 0, 1, 1)
        table.horizontalHeader().setDefaultSectionSize(150)
        return widget

    def docuBar(self,DocumentTitle, index):
        clientBanner = QtWidgets.QFrame()
        clientBanner.setMaximumSize(QtCore.QSize(16777215, 50))
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        font.setPointSize(10)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        clientBanner.setFont(font)
        clientBanner.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border-radius:30;\n""border: 2px solid rgb(212, 212, 212);\n""border-width: 2px;")
        hLayout = QtWidgets.QHBoxLayout(clientBanner)
        hLayout.setContentsMargins(0, 0, 0, 0)
        DocumentName = QtWidgets.QLabel(clientBanner)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(DocumentName.sizePolicy().hasHeightForWidth())
        DocumentName.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        font.setPointSize(10)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        DocumentName.setFont(font)
        DocumentName.setAlignment(QtCore.Qt.AlignCenter)
        DocumentName.setText(DocumentTitle)
        DocumentName.setObjectName('DocumentName')
        DocumentName.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
        hLayout.addWidget(DocumentName)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Minimum)
        hLayout.addItem(spacerItem)
        ViewButton = QtWidgets.QPushButton(clientBanner)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ViewButton.sizePolicy().hasHeightForWidth())
        ViewButton.setSizePolicy(sizePolicy)
        ViewButton.setMaximumSize(QtCore.QSize(120, 16777215))
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        font.setPointSize(10)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        ViewButton.setFont(font)
        ViewButton.setStyleSheet("background-color: rgb(85, 255, 255);")
        ViewButton.setText("View")
        ViewButton.setObjectName(index)
        ViewButton.clicked.connect(self.openDocument)
        hLayout.addWidget(ViewButton)
        self.doculayout.addWidget(clientBanner)

    def openDocument(self):
        sender =(self.sender())
        document = sender.objectName()
        print(document)
        os.startfile(self.CompanyDocuments[int(document)][2])

    def captcha(self):
        try:
            self.captchaWindow = QtWidgets.QWidget()
            pyside_dynamic.loadUi('../Resources/ui/captcha.ui',self.captchaWindow)
            #self.captchaWindow.move(300,300)
            self.captchaView = self.captchaWindow.findChild(QtWidgets.QLabel, 'captchaview')
            self.getCaptcha()
            self.CaptchaInput = self.captchaWindow.findChild(QtWidgets.QLineEdit, 'captchainput')
            self.SubmitButton = self.captchaWindow.findChild(QtWidgets.QPushButton, 'submit')
            self.SubmitButton.clicked.connect(self.getChargedetails)
            self.refreshButton = self.captchaWindow.findChild(QtWidgets.QPushButton, 'refresh')
            self.refreshButton.clicked.connect(self.getCaptcha)
            self.captchaWindow.show()
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
       
        

    def getChargedetails(self):
        self.chargeinfo = getCharges.getCharges(session, self.CIN,captcha = self.CaptchaInput.text())
        if self.chargeinfo['Status']=='Failed':
            self.getCaptcha()
        else:
            self.captchaWindow.close()
            try:
                if len(self.chargeinfo['data'])>0:
                    self.DisplayArea.layout().addWidget(self.chargesWidget,*(0,0))
                    self.chargedetails = self.chargeinfo['data']
                    self.chargesWidget.Table.setRowCount(len(self.chargedetails))
                    for x in range(len(self.chargedetails)):
                        DirectInfo = self.chargedetails[x][1:]
                        for y in range(len(DirectInfo)):
                            item = QtWidgets.QTableWidgetItem()
                            self.chargesWidget.Table.setItem(x, y, item)
                            item.setText(str(DirectInfo[y]))
                    for col in range(self.chargesWidget.Table.columnCount()):
                        self.chargesWidget.Table.horizontalHeader().setSectionResizeMode(col, QtWidgets.QHeaderView.ResizeToContents)
                else:
                    QtWidgets.QMessageBox.critical(self, "No Charges Registered", "No charge is registered for the company")
            except NameError as e:
                print(e)
                pass
        
    
def clearLayout(layout):
    while layout.count():
        child = layout.takeAt(0)
        if child.widget() is not None:
            child.widget().deleteLater()
        elif child.layout() is not None:
            clearLayout(child.layout())
