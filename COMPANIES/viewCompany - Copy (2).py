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
from COMPANIES import Notice, Minutes
import pickle
from collections import Counter
import webbrowser


session = requests_html.HTMLSession()

class Ui(QtWidgets.QWidget):
    def __init__(self,DirectorDIN):
        super(Ui, self).__init__()
        pyside_dynamic.loadUi('../Resources/ui/viewCompany.ui',self)
        with open('Config','rb') as f:
            self.Config = pickle.loads(f.read())
            f.close()
        self.CIN = DirectorDIN
        self.dbfilepath = os.path.join(self.Config['Database'],'C3_DataBase.db')
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
        self.Sidebar.layout().addWidget(self.createButton('Meeting Manager', self.meetingManager))
        self.Sidebar.layout().addWidget(self.createButton('Register Manager', self.registerManager))
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
        

    def registerManager(self):
        pass
    
    def meetingManager(self):
        ScrollArea = QtWidgets.QScrollArea()
        ScrollDisplay = QtWidgets.QWidget()
        filingvbox = QtWidgets.QVBoxLayout()
        ScrollDisplay.setLayout(filingvbox)
        ScrollArea.setWidget(ScrollDisplay)
        self.frame_2 = QtWidgets.QFrame()
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
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.addMeetingBtn = QtWidgets.QPushButton(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.addMeetingBtn.sizePolicy().hasHeightForWidth())
        self.addMeetingBtn.setSizePolicy(sizePolicy)
        self.addMeetingBtn.setMinimumSize(QtCore.QSize(120, 0))
        self.addMeetingBtn.setMaximumSize(QtCore.QSize(120, 16777215))
        self.addMeetingBtn.setSizeIncrement(QtCore.QSize(0, 0))
        self.addMeetingBtn.setText("Add Meeting")
        font = QtGui.QFont()
        font.setFamily("Georgia")
        font.setPointSize(10)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.addMeetingBtn.setFont(font)
        self.addMeetingBtn.setStyleSheet("background-color:rgb(0, 170, 0);\n"
"color: rgb(255, 255, 255);\n"
"border-radius:10")
        self.addMeetingBtn.setObjectName("addMeeting")
        self.horizontalLayout_2.addWidget(self.addMeetingBtn)
        self.addNoticeBtn = QtWidgets.QPushButton(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.addNoticeBtn.sizePolicy().hasHeightForWidth())
        self.addNoticeBtn.setSizePolicy(sizePolicy)
        self.addNoticeBtn.setMinimumSize(QtCore.QSize(120, 0))
        self.addNoticeBtn.setMaximumSize(QtCore.QSize(120, 16777215))
        self.addNoticeBtn.setText("Add Notice")
        self.addNoticeBtn.clicked.connect(self.addNotice)
        font = QtGui.QFont()
        font.setFamily("Georgia")
        font.setPointSize(10)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.addNoticeBtn.setFont(font)
        self.addNoticeBtn.setStyleSheet("background-color:rgb(0, 170, 0);\n"
"color: rgb(255, 255, 255);\n"
"border-radius:10")
        self.addNoticeBtn.setObjectName("addNotice")
        self.horizontalLayout_2.addWidget(self.addNoticeBtn)
        self.addMinuteBtn = QtWidgets.QPushButton(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.addMinuteBtn.sizePolicy().hasHeightForWidth())
        self.addMinuteBtn.setSizePolicy(sizePolicy)
        self.addMinuteBtn.setMinimumSize(QtCore.QSize(120, 0))
        self.addMinuteBtn.setMaximumSize(QtCore.QSize(120, 16777215))
        self.addMinuteBtn.setText("Add Minute")
        self.addMinuteBtn.clicked.connect(self.addMinute)
        font = QtGui.QFont()
        font.setFamily("Georgia")
        font.setPointSize(10)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.addMinuteBtn.setFont(font)
        self.addMinuteBtn.setStyleSheet("background-color:rgb(0, 170, 0);\n"
"color: rgb(255, 255, 255);\n"
"border-radius:10")
        self.addMinuteBtn.setObjectName("addMinute")
        self.horizontalLayout_2.addWidget(self.addMinuteBtn)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        
        self.ToolBoxWidget = QtWidgets.QToolBox()
        self.ToolBoxWidget.setStyleSheet("QToolBox::Tab{font-size: 16px;font-family: 'Georgia';font-style: bold;border-width:2px;border-radius: 15px;background:rgb(36, 52, 75);color:rgb(255, 255, 255);}QToolBox::Tab:selected{background:rgb(60, 81, 109);}QToolBox{ icon-size: 32px; }")
        self.minutesPath = os.path.join(self.Config['Database'],'minutes.db')
        self.conn = sqlite3.connect(self.minutesPath)
        self.cur = self.conn.cursor()
        self.minutesBook = self.cur.execute(f'SELECT * from minutes WHERE company_cin = "{self.CIN}"').fetchall()
        if len(self.minutesBook)==0:
            year = str(datetime.datetime.now().year)
            meetWidget = QtWidgets.QWidget()
            pyside_dynamic.loadUi('../Resources/ui/MeetingsManager.ui',meetWidget)
            meetWidget.meetingTable.setColumnWidth(0, 120)
            meetWidget.meetingTable.setColumnWidth(1, 120)
            meetWidget.meetingTable.setColumnWidth(2, 200)
            meetWidget.meetingTable.setColumnWidth(3, 200)
            meetWidget.meetingTable.setColumnWidth(4, 200)
            meetWidget.meetingTable.setColumnWidth(5, 120)
            meetWidget.meetingTable.setColumnWidth(6, 120)
            self.ToolBoxWidget.addItem(meetWidget, year)
        else:
            yearList = []
            for minute in self.minutesBook:
                yearList.append(minute[3])
            yearCount = dict(Counter(yearList))
            sortedYearList = sorted(yearCount.keys(),reverse=True)
            self.segYeardata = {}
            for minute in self.minutesBook:
                if not minute[3] in self.segYeardata.keys():
                    self.segYeardata[minute[3]] = [minute]
                else:
                    self.segYeardata[minute[3]].append(minute)
            for year in sortedYearList:
                meetWidget = QtWidgets.QWidget()
                pyside_dynamic.loadUi('../Resources/ui/MeetingsManager.ui',meetWidget)
                meetWidget.meetingTable.setRowCount(yearCount[year])
                meetWidget.meetingTable.setColumnWidth(0, 120)
                meetWidget.meetingTable.setColumnWidth(1, 120)
                meetWidget.meetingTable.setColumnWidth(2, 200)
                meetWidget.meetingTable.setColumnWidth(3, 200)
                meetWidget.meetingTable.setColumnWidth(4, 200)
                meetWidget.meetingTable.setColumnWidth(5, 120)
                meetWidget.meetingTable.setColumnWidth(6, 120)
                self.ToolBoxWidget.addItem(meetWidget, year)
            for year in self.segYeardata.keys():
                tabIndex = sortedYearList.index(year)
                tabWidget = self.ToolBoxWidget.widget(tabIndex)
                for x, minute in enumerate(self.segYeardata[year]):
                    for y in range(len(minute[:5])):
                        item = QtWidgets.QTableWidgetItem()
                        tabWidget.meetingTable.setItem(x, y, item)
                        item.setText(str(minute[y+1]))
                    self.addTableButtons(tabWidget.meetingTable,x,minute[6],minute[7])
                tabWidget.meetingTable.sortItems(0, QtCore.Qt.AscendingOrder)
        filingvbox.addWidget(self.frame_2)
        filingvbox.addWidget(self.ToolBoxWidget)
        ScrollArea.setWidgetResizable(True)
        self.DisplayArea.layout().addWidget(ScrollArea,*(0,0))

    def addMeetingRow(self):
        sender =(self.sender())
        parent = sender.parent().parent()
        meetingTable = parent.findChild(QtWidgets.QTableWidget, 'meetingTable')
        rowPosition = meetingTable.rowCount()
        meetingTable.insertRow(rowPosition)
        self.addTableButtons(meetingTable)

    def openDoc(self):
        buttonClicked = self.sender()
        senderBtn = buttonClicked.objectName()
        docindex = self.ToolBoxWidget.currentWidget().meetingTable.indexAt(buttonClicked.pos()).row()
        year = self.ToolBoxWidget.itemText(self.ToolBoxWidget.currentIndex())
        print(senderBtn)
        if 'notice' in senderBtn.lower():
            docid = 6
        else:
            docid = 7
        docName = self.segYeardata[year][docindex][docid]
        os.startfile(docName+'.docx')
        
        
        
    def addTableButtons(self,table,row, notice = '', minute=''):
        NoFrame = QtWidgets.QFrame(self)
        NoLayout = QtWidgets.QHBoxLayout(NoFrame) 
        addNoticeButton = QtWidgets.QToolButton()
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(QtGui.QImage("../Resources/Icon/plus.svg")), QtGui.QIcon.Normal)
        addNoticeButton.setIcon(icon)
        addNoticeButton.setObjectName("addNoticeButton")
        addNoticeButton.setToolTip("Add Notice")
        if notice=='':
            addNoticeButton.clicked.connect(self.addNotice)
        else:
            addNoticeButton.setEnabled(False)
        NoLayout.addWidget(addNoticeButton)
        editNoticeButton = QtWidgets.QToolButton()
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(QtGui.QImage("../Resources/Icon/edit.svg")), QtGui.QIcon.Normal)
        editNoticeButton.setIcon(icon)
        editNoticeButton.setObjectName("editNoticeButton")
        editNoticeButton.setToolTip("Edit Notice")
        if notice=='':
            editNoticeButton.setEnabled(False)
        else:
            editNoticeButton.clicked.connect(self.openDoc)
        NoLayout.addWidget(editNoticeButton)
        reviewNoticeButton = QtWidgets.QToolButton()
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(QtGui.QImage("../Resources/Icon/review.svg")), QtGui.QIcon.Normal)
        reviewNoticeButton.setIcon(icon)
        reviewNoticeButton.setObjectName("reviewNoticeButton")
        reviewNoticeButton.setToolTip("Mark Notice for Review")
        #reviewNoticeButton.setStyleSheet("background-color: rgb(121,85,72);")
        reviewNoticeButton.setEnabled(False)
        NoLayout.addWidget(reviewNoticeButton)
        NoFrame.setLayout(NoLayout)
        NoLayout.setContentsMargins(0, 0, 0, 0)
        table.setCellWidget(row, 5, NoFrame)

        MiFrame = QtWidgets.QFrame(self)
        MiLayout = QtWidgets.QHBoxLayout(MiFrame) 
        addMinutesButton = QtWidgets.QToolButton()
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(QtGui.QImage("../Resources/Icon/plus.svg")), QtGui.QIcon.Normal)
        addMinutesButton.setIcon(icon)
        addMinutesButton.setObjectName("addMinutesButton")
        addMinutesButton.setToolTip("Add Minutes")
        #addMinutesButton.clicked.connect(self.addNotice)
        #addMinutesButton.setStyleSheet("background-color: rgb(0,150,136);")
        MiLayout.addWidget(addMinutesButton)
        editMinutesButton = QtWidgets.QToolButton()
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(QtGui.QImage("../Resources/Icon/edit.svg")), QtGui.QIcon.Normal)
        editMinutesButton.setIcon(icon)
        editMinutesButton.setObjectName("editMinutesButton")
        editMinutesButton.setToolTip("Edit Minutes")
        #editMinutesButton.setStyleSheet("background-color: rgb(255,152,0);")
        editMinutesButton.setEnabled(False)
        MiLayout.addWidget(editMinutesButton)
        reviewMinutesButton = QtWidgets.QToolButton()
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(QtGui.QImage("../Resources/Icon/review.svg")), QtGui.QIcon.Normal)
        reviewMinutesButton.setIcon(icon)
        reviewMinutesButton.setObjectName("reviewMinutesButton")
        reviewMinutesButton.setToolTip("Mark Minutes for Review")
        #reviewMinutesButton.setStyleSheet("background-color: rgb(121,85,72);")
        reviewMinutesButton.setEnabled(False)
        MiLayout.addWidget(reviewMinutesButton)
        MiFrame.setLayout(MiLayout)
        MiLayout.setContentsMargins(0, 0, 0, 0)
        table.setCellWidget(row, 6, MiFrame)
        
            
    def addNotice(self):
        sender = self.sender()
        parent = getParent(sender,'HomePage')
        layout = parent.findChild(QtWidgets.QWidget, 'MainWindow').layout()
        clearLayout(layout)
        CurrentWidget = Notice.Ui(self.CompanyBasicInfo[1])
        layout.addWidget(CurrentWidget, *(0,0))


    def addMinute(self):
        sender = self.sender()
        parent = getParent(sender,'HomePage')
        layout = parent.findChild(QtWidgets.QWidget, 'MainWindow').layout()
        clearLayout(layout)
        CurrentWidget = Minutes.Ui(self.CompanyBasicInfo[1])
        layout.addWidget(CurrentWidget, *(0,0))
        
        
    def createButton(self,Text,Fn):
        button = QtWidgets.QPushButton()
        button.setStyleSheet("QPushButton{background-color: rgb(1, 22, 39);border-radius:10; color: rgb(255,255,255)} QPushButton:hover{background:rgb(240, 240, 240);color: rgb(1, 22, 39)} QPushButton:pressed:!hover{background:rgb(240, 240, 240)}")
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
        self.SignaWidget.DirectorsInfo.setRowCount(len(self.CompanyDirectorsInfo))
        for ROW,Director in enumerate(self.CompanyDirectorsInfo):
            DirInfo = [Director[2].title(),Director[1],Director[4]]
            for COLUMN in range(len(DirInfo)):
                item = QtWidgets.QTableWidgetItem()
                self.SignaWidget.DirectorsInfo.setItem(ROW, COLUMN, item)
                item.setText(str(DirInfo[COLUMN]))
                item.setFlags(QtCore.Qt.ItemIsEnabled)
            MoreInfo = QtWidgets.QPushButton()
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
            MoreInfo.setObjectName(str(ROW))
            MoreInfo.clicked.connect(self.viewExtendedFn)
            self.SignaWidget.DirectorsInfo.setCellWidget(ROW, 3, MoreInfo)
        self.SignaWidget.DirectorsInfo.setColumnWidth(0, 600)
        self.SignaWidget.DirectorsInfo.setColumnWidth(1, 150)
        self.SignaWidget.DirectorsInfo.setColumnWidth(2, 250)
        self.SignaWidget.DirectorsInfo.setColumnWidth(3, 100)
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
        pyside_dynamic.loadUi('../Resources/ui/documentViewer.ui',self.DocumentWidget)
        self.DocumentWidget.documentTable.setRowCount(len(self.CompanyDocuments))
        for ROW in range(len(self.CompanyDocuments)):
            item = QtWidgets.QTableWidgetItem()
            self.DocumentWidget.documentTable.setItem(ROW, 0, item)
            item.setText(self.CompanyDocuments[ROW][1])
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            ViewButton = QtWidgets.QPushButton()
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
            ViewButton.setObjectName(str(ROW))
            ViewButton.clicked.connect(self.openDocument)
            self.DocumentWidget.documentTable.setCellWidget(ROW, 1, ViewButton)
        self.DocumentWidget.documentTable.setColumnWidth(0, 1000)
        self.DocumentWidget.documentTable.setColumnWidth(1, 100)
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
        ScrollArea.setWidgetResizable(True)
        self.DisplayArea.layout().addWidget(ScrollArea,*(0,0))
        
    def Activities(self):
        ScrollArea = QtWidgets.QScrollArea()
        ScrollDisplay = QtWidgets.QWidget()
        filingvbox = QtWidgets.QVBoxLayout()
        ScrollDisplay.setLayout(filingvbox)
        ScrollArea.setWidget(ScrollDisplay)
        self.ToolBoxWidget = QtWidgets.QToolBox()
        self.ToolBoxWidget.setStyleSheet("QToolBox::Tab{font-size: 16px;font-family: 'Georgia';font-style: bold;border-width:2px;border-radius: 15px;background:rgb(36, 52, 75);color:rgb(255, 255, 255);}QToolBox::Tab:selected{background:rgb(60, 81, 109);}QToolBox{ icon-size: 32px; }")
        activities = os.path.join(self.Config['Database'],'activities.db')
        conn = sqlite3.connect(activities)
        cur = conn.cursor()
        activitiesData = cur.execute(f'SELECT * from activities WHERE company_cin = "{self.CIN}"').fetchall()
        if len(activitiesData)==0:
            year = str(datetime.datetime.now().year)
        else:
            yearList = []
            for activity in activitiesData:
                yearList.append(activity[6])
            yearCount = dict(Counter(yearList))
            sortedYearList = sorted(yearCount.keys(),reverse=True)
            self.segYeardata = {}
            for activity in activitiesData:
                if not activity[5] in self.segYeardata.keys():
                    self.segYeardata[activity[6]] = [activity]
                else:
                    self.segYeardata[activity[6]].append(activity)
            for year in sortedYearList:
                meetWidget = QtWidgets.QWidget()
                pyside_dynamic.loadUi('../Resources/ui/ActivitiesManager.ui',meetWidget)
                meetWidget.meetingTable.setRowCount(yearCount[year])
                meetWidget.meetingTable.setColumnWidth(0, 120)
                meetWidget.meetingTable.setColumnWidth(1, 120)
                meetWidget.meetingTable.setColumnWidth(2, 120)
                meetWidget.meetingTable.setColumnWidth(3, 120)
                meetWidget.meetingTable.setColumnWidth(4, 350)
                meetWidget.meetingTable.setColumnWidth(5, 200)
                #meetWidget.meetingTable.itemDoubleClicked.connect(self.OpenLink)
                self.ToolBoxWidget.addItem(meetWidget, year)
            for year in self.segYeardata.keys():
                tabIndex = sortedYearList.index(year)
                tabWidget = self.ToolBoxWidget.widget(tabIndex)
                for x, activity in enumerate(self.segYeardata[year]):
                    filterList = [x for x in [x if activity.index(x) not in (0,6,8) else None for x in activity] if x]
                    for y in range(len(filterList)):
                        if y != 6:
                            item = QtWidgets.QTableWidgetItem()
                            tabWidget.meetingTable.setItem(x, y, item)
                            item.setText(str(filterList[y]))
                            item.setFlags(QtCore.Qt.ItemIsEnabled)
                        else:
                            if filterList[y] !='':
                                ViewButton = QtWidgets.QPushButton()
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
                                ViewButton.setText("Open Document")
                                ViewButton.setObjectName(str(filterList[y]))
                                ViewButton.clicked.connect(self.OpenLink)
                                tabWidget.meetingTable.setCellWidget(x, y, ViewButton)
                tabWidget.meetingTable.sortItems(0, QtCore.Qt.AscendingOrder)
        filingvbox.addWidget(self.ToolBoxWidget)
        ScrollArea.setWidgetResizable(True)
        self.DisplayArea.layout().addWidget(ScrollArea,*(0,0))

    def OpenLink(self,item):
##        parentWidget = item.tableWidget()
##        if item.column() == 5:
        sender =(self.sender())
        document = sender.objectName()
        webbrowser.open(document+'.docx')
            
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
        sender =(self.sender())
        Home = sender.parent().parent().parent().parent()
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
       
        

    def getChargedetails(self):
        self.ChargeThread = upateThread(parent=self)
        self.ChargeThread.start()
        

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

class upateThread(QtCore.QThread):  
    progress = QtCore.Signal(str) 
    def __init__(self,parent=None):  
        super(upateThread,self).__init__(parent)  
        self.exiting = False
        self.parent = parent
  
    def run(self):  
        self.chargeinfo = getCharges.getCharges(session, self.parent.CIN,captcha = self.parent.CaptchaInput.text())
        if self.chargeinfo['Status']=='Failed':
            self.parent.getCaptcha()
        else:
            self.parent.captchaWindow.close()
            self.parent.Toast.setHidden(not self.parent.Toast.isHidden())
            try:
                if len(self.chargeinfo['data'])>0:
                    self.parent.DisplayArea.layout().addWidget(self.parent.chargesWidget,*(0,0))
                    self.chargedetails = self.chargeinfo['data']
                    self.parent.chargesWidget.Table.setRowCount(len(self.chargedetails))
                    for x in range(len(self.chargedetails)):
                        DirectInfo = self.chargedetails[x][1:]
                        for y in range(len(DirectInfo)):
                            item = QtWidgets.QTableWidgetItem()
                            self.parent.chargesWidget.Table.setItem(x, y, item)
                            item.setText(str(DirectInfo[y]))
                    for col in range(self.parent.chargesWidget.Table.columnCount()):
                        self.parent.chargesWidget.Table.horizontalHeader().setSectionResizeMode(col, QtWidgets.QHeaderView.ResizeToContents)
                else:
                    QtWidgets.QMessageBox.critical(self, "No Charges Registered", "No charge is registered for the company")
            except NameError as e:
                print(e)
                pass 
