from PySide2 import QtWidgets, QtUiTools,QtCore, QtGui
import sys
import os
sys.path.append(os.path.abspath(os.path.join('..')))
import HomePage
import pickle
from functions import Database_Manager as db
from functions import pyside_dynamic
from functions.generateDocuments import Minutes
from pathlib import Path
import datetime
import sqlite3
from functools import partial
import re


class Ui(QtWidgets.QWidget):
    def __init__(self,CoName, date):
        super(Ui, self).__init__()
        pyside_dynamic.loadUi('Resources/ui/Minutes.ui',self)
        self.currentselection = CoName
        with open('Config','rb') as f:
            self.Config = pickle.loads(f.read())
            f.close()
        self.AuthTracker = {}
        self.dbfilepath = os.path.join(self.Config['Database'],'C3_DataBase.db')
        self.resolutionspath = os.path.join(self.Config['Database'],'Resolutions.db')
        self.conn = sqlite3.connect(self.dbfilepath)
        self.cur = self.conn.cursor()
        self.AgendaDict = {}
        self.SignNO = 4
        self.LOA = []
        self.Absent = []
        self.Present = []
        self.AttendeesList = []
        self.DateFormats=['%d.%m.%Y','%d/%m/%Y','%B %e, %Y','%A, %B %e, %Y']
        self.AuthorizedContainer = []
        self.GetSignatoriesList()
        CompanyListdb = self.cur.execute('SELECT "company_name" from Masterdata').fetchall()
        self.AgendaNoteList = {}
        self.SavedInfo = {}
        self.CoName = CoName
        self.AgendaTable = self.findChild(QtWidgets.QTableWidget, 'AgendaTable')
        self.AgendaTable.resizeRowsToContents()
        self.AgendaTable.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.AgendaTable.customContextMenuRequested.connect(self.handleHeaderMenu_client)
        self.DateSelection = self.findChild(QtWidgets.QDateEdit, 'DateSelection')
        mDate = QtCore.QDateTime.currentDateTime()
        if date!=None:
            mDate = datetime.datetime.strptime(date, '%d-%m-%Y')
        self.DateSelection.setDateTime(mDate)
        self.exDate.setDateTime(mDate)
        self.TimeSelect = self.findChild(QtWidgets.QTimeEdit, 'TimeSelect')
        self.TimeSelect.setTime(QtCore.QTime.currentTime())
        self.TimeSelect.timeChanged.connect(self.setStartTime)
        self.StartTime.setTime(self.TimeSelect.time())
        self.StartTime.timeChanged.connect(self.setEndTime)
        self.EndTime.setTime(self.StartTime.time().addSecs(60*30))
        self.EndTime.timeChanged.connect(self.checkTime)
        self.VenueSelect = self.findChild(QtWidgets.QLineEdit, 'VenueSelect')
        self.GenerateNotice = self.findChild(QtWidgets.QPushButton, 'GenerateNotice')
        self.Attendees.clicked.connect(self.AuthorizationSelection)
        self.GenerateMinutes.clicked.connect(self.generateDoc)
        self.conn = sqlite3.connect(self.resolutionspath)
        self.cur = self.conn.cursor()
        self.AgendaItems = self.cur.execute('SELECT TITLE from Resolutions').fetchall()
        self.AgendaList=['']
        for item in self.AgendaItems:
            self.AgendaList.append(item[0])
        NosList = list(map(str,list(range(1,100))))
        self.fy.setText(self.findfinyear(self.DateSelection.date().toPython()))
        self.NosofAgenda.addItems(NosList)
        self.NosofAgenda.currentIndexChanged.connect(self.expandAgendas)
        self.TmzSelect.activated.connect(self.checkTime)
        self.expandAgendas()
        self.VariableStore=[]
        self.Committee.clicked.connect(self.enableCommittee)
        self.BoardMeeting.clicked.connect(self.enableCommittee)
        self.EGM.clicked.connect(self.enableCommittee)
        self.AGM.clicked.connect(self.enableCommittee)
        self.committeFilePath = os.path.join(self.Config['Database'],'committees.db')
        conn = sqlite3.connect(self.committeFilePath)
        cur = conn.cursor()
        Committees = cur.execute(f'SELECT committee_name from committee WHERE company_cin = "{self.CINNum}"').fetchall()
        cur.close()
        conn.commit()
        conn.close()  
        if Committees:
            CommitteeList = []
            for committee in Committees:
               CommitteeList.append(committee[0])
            self.commiteeName.addItems(CommitteeList)
        self.commiteeName.setEnabled(False)

    #Check Mandatory Fields
        self.isAttendanceSelected = False

    def setStartTime(self):
        self.StartTime.setTime(self.TimeSelect.time())

    def setEndTime(self):
        self.EndTime.setTime(self.StartTime.time().addSecs(60*30))
        self.checkTime()

    def checkTime(self):
        if self.TimeSelect.time()<=self.StartTime.time() and self.StartTime.time()<self.EndTime.time():
            item = QtWidgets.QTableWidgetItem()
            self.AgendaTable.setItem(self.AgendaTable.rowCount()-1, 1, item)
            if self.AGM.isChecked() or  self.EGM.isChecked():
                item.setText(f"There being no other business to transact the meeting concluded with a vote of thanks to the chair at {datetime.datetime.strftime(datetime.datetime.strptime(self.EndTime.time().toString(),'%H:%M:%S'),'%I:%M %p')} ({self.TmzSelect.currentText()}).")
            else:    
                item.setText(f"Upon the confirmation of all the directors present at the meeting that there was no other business to transact, the meeting concluded with a vote of thanks to the chair at {datetime.datetime.strftime(datetime.datetime.strptime(self.EndTime.time().toString(),'%H:%M:%S'),'%I:%M %p')} ({self.TmzSelect.currentText()})")
            self.AgendaTable.resizeRowsToContents()
        else:
            QtWidgets.QMessageBox.warning(self,'Alert!!','Time shall not be less than Meeting Time or Start Time!!')
            
        
    def Selectionfill(self):
        item = QtWidgets.QTableWidgetItem()
        self.AgendaTable.setItem(self.AgendaTable.currentRow(), 1, item)
        Agenda = self.AgendaTable.cellWidget(self.AgendaTable.currentRow(),0).currentText()
        if Agenda != '':
            self.conn = sqlite3.connect(self.resolutionspath)
            self.cur = self.conn.cursor()
            self.Narration = self.cur.execute(f'SELECT NARRATION from Resolutions WHERE TITLE = {repr(Agenda)}').fetchall()[0][0]
            self.Resolution = self.cur.execute(f'SELECT RESOLUTION from Resolutions WHERE TITLE = {repr(Agenda)}').fetchall()[0][0]
            self.Field = self.cur.execute(f'SELECT FIELDS from Resolutions WHERE TITLE = {repr(Agenda)}').fetchall()[0][0]
            self.AgendaDict[self.AgendaTable.currentRow()]=(Agenda,self.Narration,self.Resolution,self.Field)
            self.AgendaTable.resizeRowsToContents()
            VariablesList = []
            VariablesList= VariablesList+re.findall(r"\{(\w+)\}",self.Narration)
            VariablesList= VariablesList+re.findall(r"\{(\w+)\}",self.Resolution)
            VariablesList = list(set(VariablesList))
            self.VariableStore={}
            self.VariableStore[self.AgendaTable.currentRow()]={}
            for variable in VariablesList:
                    self.VariableStore[self.AgendaTable.currentRow()][variable]=''
            self.SavedInfo.pop(self.AgendaTable.currentRow()+1, None)
            self.SavedInfo[self.AgendaTable.currentRow()+1] = [Agenda,self.Narration.replace('\\n','\n'),self.Resolution.replace('\\n','\n')]
        else:
            self.AgendaDict.pop(self.AgendaTable.currentRow())
        
        

    def GetSignatoriesList(self):
        self.NosofAgenda.setEnabled(True)
        self.conn = sqlite3.connect(self.dbfilepath)
        self.cur = self.conn.cursor()
        self.CINNum = self.cur.execute(f'SELECT company_cin from Masterdata WHERE company_name = "{self.currentselection}"').fetchall()[0][0]
        self.SignatoriesData = self.cur.execute(f'SELECT * from Signatories WHERE "company_cin" = "{self.CINNum}"').fetchall()
        self.SignNO = len(self.SignatoriesData)
        self.DirectorList=['']
        for item in self.SignatoriesData:
            self.DirectorList.append(item[0])
        #self.expandAgendas()

    def AuthorizationSelection(self):
        self.AuthorizationsWindow = QtWidgets.QWidget()
        pyside_dynamic.loadUi('Resources/ui/Attendees.ui', self.AuthorizationsWindow)
        self.AuthorizationsWindow.MembersSection.setHidden(True)
        if (self.EGM.isChecked() or self.AGM.isChecked()):
            self.AuthorizationsWindow.MembersSection.setHidden(False)
        self.AuthorizationsWindow.Done.clicked.connect(self.groupauthorized)
        self.AuthorizationsWindow.AddInvitees.clicked.connect(self.addrow)
        layout = QtWidgets.QVBoxLayout()
        Font = QtGui.QFont("Open Sans", 11)
        button_group  = QtWidgets.QButtonGroup()
        if self.Committee.isChecked():
            Committee = self.commiteeName.currentText()
            conn = sqlite3.connect(self.committeFilePath)
            cur = conn.cursor()
            self.CommMemInfo = cur.execute(f'SELECT * from CommitteeMembers WHERE company_cin = "{self.CINNum}" AND committee_name = "{Committee}"').fetchall()
            print(self.CommMemInfo)
            cur.close()
            conn.commit()
            conn.close()
            self.AuthorizationsWindow.BTGroup = QtWidgets.QButtonGroup()
            self.AuthorizationsWindow.DirectorsTable.setRowCount(len(self.CommMemInfo))
            loopCounter = 0
            for member in self.CommMemInfo:
                item = QtWidgets.QTableWidgetItem()
                self.AuthorizationsWindow.DirectorsTable.setItem(loopCounter, 0, item)
                item.setText(member[2]+member[3].title())
                item = QtWidgets.QTableWidgetItem()
                self.AuthorizationsWindow.DirectorsTable.setItem(loopCounter, 1, item)
                item.setText(member[4])
                loopCounter +=1
            for x in range(len(self.CommMemInfo)):
                checkbox = QtWidgets.QRadioButton()
                button_group.addButton(checkbox)
                self.AuthorizationsWindow.DirectorsTable.setCellWidget(x, 2, checkbox)
            for x in range(len(self.CommMemInfo)):
                checkbox = QtWidgets.QCheckBox()
                self.AuthorizationsWindow.DirectorsTable.setCellWidget(x, 3, checkbox)
                checkbox = QtWidgets.QCheckBox()
                self.AuthorizationsWindow.DirectorsTable.setCellWidget(x, 4, checkbox)
            self.AuthorizationsWindow.DirectorsTable.cellWidget(0,2).setChecked(True)

        else:
            self.DesignationPriority = {"Managing Director": 0, "Wholetime Director": 1, "Director": 2, "Additional Director": 3,
                                   "Alternate Director": 4, "Nominee Director": 4,"Company Secretary": 5, "CEO(KMP)" : 6 , 'CFO(KMP)' : 7}
            self.SignatoriesData.sort(key=lambda val: self.DesignationPriority[val[4]])
            self.AuthorizationsWindow.BTGroup = QtWidgets.QButtonGroup()
            self.AuthorizationsWindow.DirectorsTable.setRowCount(len(self.SignatoriesData))
            loopCounter = 0
            for director in self.SignatoriesData:
                item = QtWidgets.QTableWidgetItem()
                self.AuthorizationsWindow.DirectorsTable.setItem(loopCounter, 0, item)
                title = 'Ms.' if director[11].lower()=='feml' else 'Mr.'
                if director[11]=='':
                    title = ''
                item.setText(title+director[2].title())
                item = QtWidgets.QTableWidgetItem()
                self.AuthorizationsWindow.DirectorsTable.setItem(loopCounter, 1, item)
                item.setText(director[4])
                loopCounter +=1
            for x in range(len(self.SignatoriesData)):
                checkbox = QtWidgets.QRadioButton()
                button_group.addButton(checkbox)
                self.AuthorizationsWindow.DirectorsTable.setCellWidget(x, 2, checkbox)
            for x in range(len(self.SignatoriesData)):
                checkbox = QtWidgets.QCheckBox()
                self.AuthorizationsWindow.DirectorsTable.setCellWidget(x, 3, checkbox)
                checkbox = QtWidgets.QCheckBox()
                self.AuthorizationsWindow.DirectorsTable.setCellWidget(x, 4, checkbox)
            self.AuthorizationsWindow.DirectorsTable.cellWidget(0,2).setChecked(True)
            if self.AGM.isChecked() or self.EGM.isChecked():
                self.resolutionspath = os.path.join(self.Config['Database'],'registers.db')
                self.conn = sqlite3.connect(self.resolutionspath)
                self.cur = self.conn.cursor()
                self.Shareholders = self.cur.execute(f'SELECT name, status from MGT1PERSONAL WHERE "company_cin" = "{self.CINNum}" AND "class" ="EQUITY"').fetchall()
                loopCounter = 0
                self.AuthorizationsWindow.MembersTable.setRowCount(len(self.Shareholders))
                for shareholder in self.Shareholders:
                    item = QtWidgets.QTableWidgetItem()
                    self.AuthorizationsWindow.MembersTable.setItem(loopCounter, 0, item)
                    item.setText(shareholder[0].title())
                for x in range(len(self.SignatoriesData)):
                    checkbox = QtWidgets.QRadioButton()
                    button_group.addButton(checkbox)
                    self.AuthorizationsWindow.MembersTable.setCellWidget(x, 1, checkbox)
                for x in range(len(self.SignatoriesData)):
                    checkbox = QtWidgets.QCheckBox()
                    self.AuthorizationsWindow.MembersTable.setCellWidget(x, 2, checkbox)
                #self.AuthorizationsWindow.DirectorsTable.cellWidget(0,2).setChecked(True)
        self.AuthorizationsWindow.DirectorsTable.resizeRowsToContents()
        self.AuthorizationsWindow.DirectorsTable.resizeColumnsToContents()
        button_group.setExclusive(True) 
        self.AuthorizationsWindow.show()


    def addrow(self):
        rowPosition = self.AuthorizationsWindow.InviteesTable.rowCount()
        self.AuthorizationsWindow.InviteesTable.insertRow(rowPosition)
        
    def AddAuthorized(self,button):
        if button.text() not in self.AuthorizedContainer:
            self.AuthorizedContainer.append(button.text())
        elif button.text() in self.AuthorizedContainer:
            self.AuthorizedContainer.remove(button.text())
        else:
            None

    def selectAuthorization(self,label,sender,index,Row):
        self.AuthorizationsWindow = QtWidgets.QWidget()
        key = label.lower().replace(' ','_')
        keyText = self.VariableStore[Row][key]     
        pyside_dynamic.loadUi('Resources/ui/AddAuthorizations.ui', self.AuthorizationsWindow)
        self.AuthorizationsWindow.Done = self.AuthorizationsWindow.findChild(QtWidgets.QPushButton, 'Done')
        self.AuthorizationsWindow.AddOfficer = self.AuthorizationsWindow.findChild(QtWidgets.QPushButton, 'AddOfficer')
        self.AuthorizationsWindow.BacktoRes = self.AuthorizationsWindow.findChild(QtWidgets.QPushButton, 'BacktoRes')
        self.AuthorizationsWindow.selectionWindow = self.AuthorizationsWindow.findChild(QtWidgets.QWidget, 'SelectionWindow')
        layout = QtWidgets.QVBoxLayout()
        Font = QtGui.QFont("Open Sans", 10)
        if self.BoardMeeting.isChecked():
            self.DesignationPriority = {"Managing Director": 0, "Wholetime Director": 1, "Director": 2, "Additional Director": 3,
                                   "Alternate Director": 4, "Nominee Director": 4,"Company Secretary": 5, "CEO(KMP)" : 6 , 'CFO(KMP)' : 7}
            self.SignatoriesData.sort(key=lambda val: self.DesignationPriority[val[4]])
            self.AuthorizationsWindow.BTGroup = QtWidgets.QButtonGroup()
            for director in self.SignatoriesData:
                title = 'Ms.' if director[11].lower()=='feml' else 'Mr.'
                if director[11]=='':
                    title = ''
                item = QtWidgets.QCheckBox(title+director[2]+', '+director[4])
                item.setFont(Font)
                layout.addWidget(item)
                self.AuthorizationsWindow.BTGroup.addButton(item)
            self.AuthorizationsWindow.BTGroup.setExclusive(False)
        elif self.Committee.isChecked():
            Committee = self.commiteeName.currentText()
            conn = sqlite3.connect(self.committeFilePath)
            cur = conn.cursor()
            self.CommMemInfo = cur.execute(f'SELECT * from CommitteeMembers WHERE company_cin = "{self.CINNum}" AND committee_name = "{Committee}"').fetchall()
            cur.close()
            conn.commit()
            conn.close()  
            self.AuthorizationsWindow.BTGroup = QtWidgets.QButtonGroup()
            for member in self.CommMemInfo:
                item = QtWidgets.QCheckBox(member[1]+member[2]+', '+member[3])
                item.setFont(Font)
                layout.addWidget(item)
                self.AuthorizationsWindow.BTGroup.addButton(item)
            self.AuthorizationsWindow.BTGroup.setExclusive(False)
        if Row in self.AuthTracker.keys():
            if label in self.AuthTracker[Row].keys():
                for idx in self.AuthTracker[Row][label]:
                    self.AuthorizationsWindow.BTGroup.button(idx).setChecked(True)
        self.AuthorizationsWindow.selectAll.stateChanged.connect(partial(self.disableButtons,self.AuthorizationsWindow.BTGroup))
        if 'severally' in keyText:
            self.AuthorizationsWindow.severally.setChecked(True)
        if 'collectively' in keyText:
            self.AuthorizationsWindow.collectively.setChecked(True)
        self.AuthorizationsWindow.Done.clicked.connect(partial(self.updateResolutions,index,Row,self.AuthorizationsWindow.selectAll,self.AuthorizationsWindow.severally,self.AuthorizationsWindow.collectively))
        self.AuthorizationsWindow.selectionWindow.setLayout(layout)
        self.AuthorizationsWindow.show()

    def disableButtons(self,BTGroup,_):
        needtoDisable = False if self.AuthorizationsWindow.selectAll.isChecked() else True
        for button in BTGroup.buttons():
            button.setEnabled(needtoDisable)

    def updateResolutions(self,index,Row,allAuth,SeveBox,CollBox):
        label = self.VariableWidget.variableTable.item(index,0).text()
        self.AuthorizedContainer = []
        self.AuthTracker[Row] = {}
        self.AuthTracker[Row][label] = []
        for button in self.AuthorizationsWindow.BTGroup.buttons():
            if button.isChecked():
                self.AuthorizedContainer.append(button.text())
                self.AuthTracker[Row][label].append(self.AuthorizationsWindow.BTGroup.id(button))
        key = label.lower().replace(' ','_')
        variable = '{'+key+'}'
        NarText = self.VariableWidget.NarrationPreview.toPlainText()
        ResText = self.VariableWidget.ResolutionPreview.toPlainText()
        if allAuth.isChecked():
            authorizationText = "the Directors of the Company be and are hereby authorized "
            SeveText = ''
            if SeveBox.isChecked() and not CollBox.isChecked():
                if self.VariableStore[Row][key]=='':
                    pass
                else:
                    SeveText = ' severally'
            if not SeveBox.isChecked() and CollBox.isChecked():
                if self.VariableStore[Row][key]=='':
                    pass
                else:
                    SeveText = ' collectively'
            if SeveBox.isChecked() and CollBox.isChecked():
                if self.VariableStore[Row][key]=='':
                    pass
                else:
                    SeveText = ' severally/collectively'
            authorizationText = authorizationText+SeveText
            if self.VariableStore[Row][key]=='':
                NewNarText = NarText.replace(variable,authorizationText)
                NewResText = ResText.replace(variable,authorizationText)
            else:
                NewNarText = NarText.replace(self.VariableStore[Row][key],authorizationText)
                NewResText = ResText.replace(self.VariableStore[Row][key],authorizationText)

        else:
            Authorizations = {}
            Authorizations[label] = self.AuthorizedContainer
            if len(Authorizations[label])==1:
                authorizationText = Authorizations[label][0].title()+" of the Company, be and is hereby authorized"
            elif len(Authorizations[label])>1:
                authorizationText = ''
                AuthList = {}
                for director in Authorizations[label]:
                    designation = director.split(',')[1]
                    if 'director' in designation.lower():
                        if not 'managing' in designation.lower():
                            designation = 'Director'
                    if designation in AuthList.keys():
                        AuthList[designation].append(director.split(',')[0].title())
                    else:
                        AuthList[designation] = [director.split(',')[0].title()]
                for count,xkey in enumerate(AuthList.keys()):
                    if len(AuthList[xkey])>1:
                        TempStr = ', '.join(AuthList[xkey][:-1])+' and '+AuthList[xkey][-1]+f', {xkey}s of the Company, '
                    else:
                        TempStr = AuthList[xkey][0]+f', {xkey} of the Company, '
                    if count==len(AuthList.keys())-2:
                        TempStr=TempStr+' and '
                    authorizationText=authorizationText+TempStr
                SeveText = ''
                if SeveBox.isChecked() and not CollBox.isChecked():
                    SeveText = ' severally'
                elif not SeveBox.isChecked() and CollBox.isChecked():
                    SeveText = ' severally'
                elif SeveBox.isChecked() and CollBox.isChecked():
                    SeveText = ' severally/collectively'
                authorizationText = authorizationText+f'be and are hereby authorized{SeveText}'
            if self.VariableStore[Row][key]=='':
                NewNarText = NarText.replace(variable,authorizationText)
                NewResText = ResText.replace(variable,authorizationText)
            else:
                NewNarText = NarText.replace(self.VariableStore[Row][key],authorizationText)
                NewResText = ResText.replace(self.VariableStore[Row][key],authorizationText)
        self.VariableWidget.NarrationPreview.setText(NewNarText)
        self.VariableWidget.ResolutionPreview.setText(NewResText)
        self.VariableStore[Row][key]=authorizationText
        self.AuthorizationsWindow.close()
        self.AuthorizedContainer=[]
        
    def enableCommittee(self):
        sender =(self.sender())
        BtButton = sender.objectName()
        print(BtButton)
        if BtButton=='Committee':
            meetingName = 'Committee'
        elif BtButton == 'AGM' or BtButton == 'EGM':
            meetingName = 'General Meeting'
        else:
            meetingName = 'Board Meeting'
        if BtButton=='Committee':
            if self.commiteeName.count():
                self.commiteeName.setEnabled(True)
            else:
                QtWidgets.QMessageBox.warning(self,'Alert!!','Company does not have Committees')  
        else:
            self.commiteeName.setEnabled(False)
        self.updateAgenda(meetingName)


    def updateAgenda(self, meetingName):
        self.AgendaItems = self.cur.execute(f'SELECT TITLE from Resolutions WHERE CATEGORY = "{meetingName}"').fetchall()
        self.AgendaList=['']
        for item in self.AgendaItems:
            self.AgendaList.append(item[0])
        self.expandAgendas()
        
        
    def updateAuthorization(self):
        sender = self.sender()
        sonWidget = sender.parent()
        parentWidget = sonWidget.parent().parent()
        label = parentWidget.findChild(QtWidgets.QLabel).text()
        key = label.lower().replace(' ','_')
        AuthWidget = parentWidget.findChild(QtWidgets.QWidget,'AuthWidget')
        AuthButton = AuthWidget.findChild(QtWidgets.QPushButton)
        allAuth = AuthWidget.findChild(QtWidgets.QCheckBox,'All')
        SevWidget = parentWidget.findChild(QtWidgets.QWidget,'SeveWidget')
        SeveBox = SevWidget.findChild(QtWidgets.QCheckBox,'Severally')
        CollBox = SevWidget.findChild(QtWidgets.QCheckBox,'Collectively')
        variable = '{'+key+'}'
        NarText = self.NarrationPreview.toPlainText()
        ResText = self.ResolutionPreview.toPlainText()
        NewNarText =''
        NewResText = ''
        
        if allAuth.isChecked():
            AuthButton.setEnabled(False)
            authorizationText = "the Directors of the Company be and are hereby authorized "
            SeveText = ''
            if SeveBox.isChecked() and not CollBox.isChecked():
                if self.VariableStore[Row][key]=='':
                    pass
                else:
                    SeveText = ' severally'
            if not SeveBox.isChecked() and CollBox.isChecked():
                if self.VariableStore[Row][key]=='':
                    pass
                else:
                    SeveText = ' collectively'
            if SeveBox.isChecked() and CollBox.isChecked():
                if self.VariableStore[Row][key]=='':
                    pass
                else:
                    SeveText = ' severally/collectively'
            authorizationText = authorizationText+SeveText
            if self.VariableStore[Row][key]=='':
                NewNarText = NarText.replace(variable,authorizationText)
                NewResText = ResText.replace(variable,authorizationText)
            else:
                NewNarText = NarText.replace(self.VariableStore[Row][key],authorizationText)
                NewResText = ResText.replace(self.VariableStore[Row][key],authorizationText)
            self.NarrationPreview.setText(NewNarText)
            self.ResolutionPreview.setText(NewResText)
            self.VariableStore[Row][key]=authorizationText

        else:
            Authorizations = {}
            Authorizations[label] = self.AuthorizedContainer
            if len(Authorizations[label])==1:
                authorizationText = Authorizations[label][0].title()+" of the Company, be and is hereby authorized"
            elif len(Authorizations[label])>1:
                authorizationText = ''
                AuthList = {}
                for director in Authorizations[label]:
                    designation = director.split(',')[1]
                    if 'director' in designation.lower():
                        if not 'managing' in designation.lower():
                            designation = 'Director'
                    if designation in AuthList.keys():
                        AuthList[designation].append(director.split(',')[0].title())
                    else:
                        AuthList[designation] = [director.split(',')[0].title()]
                for count,key in enumerate(AuthList.keys()):
                    if len(AuthList[key])>1:
                        TempStr = ', '.join(AuthList[key][:-1])+' and '+AuthList[key][-1]+f', {key}s of the Company, '
                    else:
                        TempStr = AuthList[key][0]+f', {key} of the Company, '
                    if count==len(AuthList.keys())-2:
                        TempStr=TempStr+' and '
                    authorizationText=authorizationText+TempStr
                SeveText = ''
                if SeveBox.isChecked() and not CollBox.isChecked():
                    SeveText = ' severally'
                elif not SeveBox.isChecked() and CollBox.isChecked():
                    SeveText = ' severally'
                elif SeveBox.isChecked() and CollBox.isChecked():
                    SeveText = ' severally/collectively'
                authorizationText = authorizationText+f'be and are hereby authorized{SeveText}'
            if self.VariableStore[key]=='':
                NewNarText = NarText.replace(variable,authorizationText)
                NewResText = ResText.replace(variable,authorizationText)
            else:
                NewNarText = NarText.replace(self.VariableStore[key],authorizationText)
                NewResText = ResText.replace(self.VariableStore[key],authorizationText)
            self.NarrationPreview.setText(NewNarText)
            self.ResolutionPreview.setText(NewResText)
            self.VariableStore[Row][key]=authorizationText
        
            
    def groupauthorized(self):
        self.LOA = []
        self.Absent = []
        self.Present = []
        self.AttendeesList = []
        for x in range(self.AuthorizationsWindow.DirectorsTable.rowCount()):
            m=[]
            m.append(self.AuthorizationsWindow.DirectorsTable.item(x,0).text())
            m.append(self.AuthorizationsWindow.DirectorsTable.item(x,1).text())
            if self.AuthorizationsWindow.DirectorsTable.cellWidget(x,2).isChecked():
                self.Chairman = self.AuthorizationsWindow.DirectorsTable.item(x,0).text()
                ChairmanAtten = [[self.Chairman, 'Chairman']]
            elif self.AuthorizationsWindow.DirectorsTable.cellWidget(x,3).isChecked():
                self.LOA.append(m)
            elif self.AuthorizationsWindow.DirectorsTable.cellWidget(x,4).isChecked():
                self.Absent.append(m)
            else:
                self.Present.append(m)
        if self.AGM.isChecked() or self.EGM.isChecked():
            for x in range(self.AuthorizationsWindow.MembersTable.rowCount()):
                if not self.AuthorizationsWindow.MembersTable.cellWidget(x,2).isChecked():
                    m = []
                    m.append(self.AuthorizationsWindow.MembersTable.item(x,0).text())
                    m.append('Member')
                    self.Present.append(m)
                
        InviteesList=[]
        for x in range(self.AuthorizationsWindow.InviteesTable.rowCount()):
            m=[]
            for y in range(self.AuthorizationsWindow.InviteesTable.columnCount()):
                try:
                    m.append(self.AuthorizationsWindow.InviteesTable.item(x,y).text())
                except:
                    m.append('')
            InviteesList.append(tuple(m))
        self.AttendeesList = ChairmanAtten+ self.Present + InviteesList
        self.updateChairman()
        self.AuthorizationsWindow.close()
        self.isAttendanceSelected = True

    def updateChairman(self):
        item = QtWidgets.QTableWidgetItem()
        self.AgendaTable.setItem(0, 1, item)
        item.setText(f"{self.Chairman.title()} was elected as Chairman of the meeting and accordingly {'he' if self.Chairman[0:2].lower()=='mr' else ('she' if self.Chairman[0:2].lower()=='ms' else '')} took the chair and conducted the proceedings.")
        absente_string = ''
        for counter,absentee in enumerate(self.LOA):
            if counter == 0:
                absente_string = absente_string+absentee[0]
            elif counter!=len(self.LOA)-1:
                absente_string = absente_string+', '+absentee[0]
            else:
                absente_string = absente_string+' and '+absentee[0]
        if len(self.LOA)>0:
            LAO_Text = f'Leave of absence was granted to {absente_string} who expressed {("his" if absentee[0][0:2].lower()=="mr" else "her") if len(self.LOA)==1 else "their"} inability to attend the meeting.'
            item = QtWidgets.QTableWidgetItem()
            self.AgendaTable.setItem(2, 1, item)
            item.setText(LAO_Text)
            
            
            
    def expandAgendas(self):
        self.AgendaTable.setRowCount(0)
        AgendaStart = 4 if not(self.AGM.isChecked() or  self.EGM.isChecked()) else 3
        print(AgendaStart)
        self.AgendaTable.setRowCount(AgendaStart+int(self.NosofAgenda.currentText())+1)
        for x in range(AgendaStart):
##            NoteButton = QtWidgets.QPushButton()
##            NoteButton.clicked.connect(self.PreviewResolution)
##            NoteButton.setText("Edit")
##            NoteButton.setStyleSheet("background-color:rgb(0, 170, 255);color: rgb(255, 255, 255);border-radius:10;")
            item = QtWidgets.QTableWidgetItem()
            self.AgendaTable.setItem(x, 0, item)
            if x==0:
               if self.AGM.isChecked() or  self.EGM.isChecked():
                   item.setText("Chairman")
               else:
                   item.setText("Appointment of Chairman for the Meeting.")
               item = QtWidgets.QTableWidgetItem()
               self.AgendaTable.setItem(x, 1, item)
               item.setText("Please select a Chairman for the meeting") 
            elif x==1:
               if self.AGM.isChecked() or  self.EGM.isChecked():
                   item.setText("Quorum")
               else:
                   item.setText("Quorum of the Meeting")
               item = QtWidgets.QTableWidgetItem()
               self.AgendaTable.setItem(x, 1, item)
               if self.AGM.isChecked() or  self.EGM.isChecked():
                   item.setText("The Chairman welcomed the members to the meeting and called the meeting to order, requisite quorum being present, the Chairman declared the meeting open for discussion")
               else:
                   item.setText("Chairman declared that requisite quorum was present and called the meeting to order.")
            elif x==2:
                if self.AGM.isChecked() or  self.EGM.isChecked():
                    item.setText("Notice")
                else:
                    item.setText("Leave of absence")
                item = QtWidgets.QTableWidgetItem()
                self.AgendaTable.setItem(x, 1, item)
                if self.AGM.isChecked() or  self.EGM.isChecked():
                    item.setText("The Notice convening the said meeting was read out to the members by the Chairman.")
                else:
                    if self.SignNO>2:
                        item.setText("Since all the Directors were present, the subject did not arise.")
                    else:
                        item.setText("Since both the Directors were present, the subject did not arise.")
            if x==3:        
                item.setText("Confirmation of Minutes of the previous Meeting.")
                item = QtWidgets.QTableWidgetItem()
                self.AgendaTable.setItem(x, 1, item)
                item.setText("The minutes of the previous Board meeting, which were circulated amongst the Directors, approved and signed by the Chairman are hereby noted.")
        for x in range(AgendaStart,AgendaStart+int(self.NosofAgenda.currentText())+1):
            VariableButton = QtWidgets.QPushButton()
            VariableButton.clicked.connect(self.EditVariable)
            VariableButton.setText("Enter Variables")
            VariableButton.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
            VariableButton.setStyleSheet("background-color:rgb(170, 0, 255);color: rgb(255, 255, 255);border-radius:10;")
            if x<AgendaStart+int(self.NosofAgenda.currentText()):
                Box = QtWidgets.QWidget()
                Layout = QtWidgets.QHBoxLayout(Box)
                Layout.addWidget(VariableButton)
                Layout.setContentsMargins(0,0,0,0)
                Box.setLayout(Layout)
                comboBox = QtWidgets.QComboBox()
                comboBox.addItems(self.AgendaList)
                comboBox.setEditable(True)
                comboBox.currentIndexChanged.connect(self.Selectionfill)
                self.AgendaTable.setCellWidget(x, 0, comboBox)
                self.AgendaTable.setCellWidget(x, 1, Box)
            elif x==AgendaStart+int(self.NosofAgenda.currentText()):
                item = QtWidgets.QTableWidgetItem()
                self.AgendaTable.setItem(x, 0, item)
                item.setText("Vote of Thanks")
                item = QtWidgets.QTableWidgetItem()
                self.AgendaTable.setItem(x, 1, item)
                if self.AGM.isChecked() or  self.EGM.isChecked():
                    item.setText(f"There being no other business to transact the meeting concluded with a vote of thanks to the chair at {datetime.datetime.strftime(datetime.datetime.strptime(self.EndTime.time().toString(),'%H:%M:%S'),'%I:%M %p')} ({self.TmzSelect.currentText()}).")
                else:
                    item.setText(f"Upon the confirmation of all the directors present at the meeting that there was no other business to transact, the meeting concluded with a vote of thanks to the chair at \
{datetime.datetime.strftime(datetime.datetime.strptime(self.EndTime.time().toString(),'%H:%M:%S'),'%I:%M %p')} ({self.TmzSelect.currentText()})")
        self.AgendaTable.resizeRowsToContents()
               

    def EditVariable(self):
        sender = self.sender()
        index = self.AgendaTable.indexAt(sender.parent().pos())
        Row = index.row()
        print(Row)
        self.VariableWidget = QtWidgets.QWidget()
        pyside_dynamic.loadUi('Resources/ui/editvariable.ui', self.VariableWidget)
        rowcount = 0
        self.VariableWidget.variableTable.setRowCount(len(eval(self.AgendaDict[Row][3])))
        for fieldItem in eval(self.AgendaDict[Row][3]):
            item = QtWidgets.QTableWidgetItem()
            self.VariableWidget.variableTable.setItem(rowcount, 0, item)
            item.setText(fieldItem[0])
            if 'date' in fieldItem[1].lower():
                varWidget = QtWidgets.QWidget()
                layout = QtWidgets.QHBoxLayout()
                DateField = QtWidgets.QDateEdit()
                DateField.setDisplayFormat('dd.MM.yyyy')
                DateField.setDateTime(QtCore.QDateTime.currentDateTime())
                DateField.dateChanged.connect(partial(self.dateUpdate,rowcount,Row,varWidget))
                formatList = QtWidgets.QComboBox()
                formatList.addItems(self.DateFormats)
                formatList.activated.connect(partial(self.dateUpdate,rowcount,Row,varWidget))
                layout.addWidget(DateField)
                layout.addWidget(formatList)
                layout.setContentsMargins(0,0,0,0)
                varWidget.setLayout(layout)
            elif 'time' in fieldItem[1].lower():
                varWidget = QtWidgets.QWidget()
                layout = QtWidgets.QHBoxLayout()
                TimeField = QtWidgets.QTimeEdit()
                TimeField.setDisplayFormat('h:mm AP')
                TimeField.setTime(QtCore.QTime.currentTime())
                TimeField.timeChanged.connect(partial(self.TimeUpdate,rowcount,Row,varWidget))
                formatList = QtWidgets.QLineEdit()
                formatList.setText('IST')
                formatList.textChanged.connect(partial(self.TimeUpdate,rowcount,Row,varWidget))
                layout.addWidget(TimeField)
                layout.addWidget(formatList)
                layout.setContentsMargins(0,0,0,0)
                varWidget.setLayout(layout)
            elif 'din' in fieldItem[1].lower():
                varWidget = QtWidgets.QLineEdit()
                varWidget.textChanged.connect(partial(self.LiveFill,rowcount,Row))
                varWidget.setValidator(QtGui.QIntValidator())
                varWidget.setMaxLength(8)
            elif 'cin' in fieldItem[1].lower():
                varWidget = QtWidgets.QLineEdit()
                varWidget.textChanged.connect(partial(self.LiveFill,rowcount,Row))
                varWidget.setMaxLength(21)
            elif 'authorization' == fieldItem[1].lower():
                varWidget = QtWidgets.QPushButton()
                varWidget.setText("Select Authorizations")
                varWidget.clicked.connect(partial(self.selectAuthorization,fieldItem[0],varWidget,rowcount,Row))
            else:
                varWidget = QtWidgets.QLineEdit()
                varWidget.textChanged.connect(partial(self.LiveFill,rowcount,Row))
            self.VariableWidget.variableTable.setCellWidget(rowcount, 1, varWidget)
            rowcount+=1
        if not Row+1 in self.SavedInfo.keys():
            NarrationText=(self.AgendaDict[Row][1].replace('\\n','\n'))
            ResolutionText=(self.AgendaDict[Row][2].replace('\\n','\n'))
            Title = self.AgendaDict[Row][0]
        else:
            NarrationText = self.SavedInfo[Row+1][1]
            ResolutionText= self.SavedInfo[Row+1][2]
            Title = self.SavedInfo[Row+1][0]
        self.VariableWidget.NarrationPreview.setText(NarrationText)
        self.VariableWidget.ResolutionPreview.setText(ResolutionText)
        self.VariableWidget.Title.setText(Title)
        self.VariableWidget.Save.clicked.connect(partial(self.saveVariables,Row))
        for varRow in range(self.VariableWidget.variableTable.rowCount()):
            label = self.VariableWidget.variableTable.item(varRow,0).text()
            key = label.lower().replace(' ','_')
            if key in self.VariableStore[Row].keys():
                if isinstance(self.VariableWidget.variableTable.cellWidget(varRow,1), QtWidgets.QLineEdit):
                    self.VariableWidget.variableTable.cellWidget(varRow,1).setText(self.VariableStore[Row][key].replace('}','').replace('{',''))
        #self.VariableWidget.setWindowModality(QtCore.Qt.ApplicationModal)
        self.VariableWidget.show()


    def saveVariables(self, Row):
        Title = self.VariableWidget.Title.text()
        Narration = self.VariableWidget.NarrationPreview.toPlainText()
        Resolutions = self.VariableWidget.ResolutionPreview.toPlainText()
        self.SavedInfo[Row+1] = [Title, Narration, Resolutions]
        print(self.SavedInfo)
        self.VariableWidget.close()
        
    def getAuthorizations(self):
        self.AuthSelect = QtWidgets.QWidget()
        Alllayout = QtWidgets.QVBoxLayout()
        AuthWidget = QtWidgets.QWidget()
        AuthWidget.setObjectName('AuthWidget')
        layout = QtWidgets.QHBoxLayout()
        Authorization = QtWidgets.QPushButton()
        Authorization.setText('Select')
        Authorization.clicked.connect(self.AuthorizationSelection)
        layout.addWidget(Authorization)
        AllSelect = QtWidgets.QCheckBox()
        AllSelect.stateChanged.connect(self.updateAuthorization)
        AllSelect.setText('All')
        AllSelect.setObjectName('All')
        layout.addWidget(AllSelect)
        AuthWidget.setLayout(layout)
        SeveWidget = QtWidgets.QWidget()
        SeveWidget.setObjectName('SeveWidget')
        sevlayout = QtWidgets.QHBoxLayout()
        sevCheckBox = QtWidgets.QCheckBox()
        sevCheckBox.stateChanged.connect(self.updateAuthorization)
        sevCheckBox.setText("Severally")
        sevCheckBox.setObjectName('Severally')
        sevlayout.addWidget(sevCheckBox)
        colCheckBox = QtWidgets.QCheckBox()
        colCheckBox.stateChanged.connect(self.updateAuthorization)
        colCheckBox.setText('Collectively')
        colCheckBox.setObjectName('Collectively')
        sevlayout.addWidget(colCheckBox)
        SeveWidget.setLayout(sevlayout)
        layout.addWidget(AllSelect)
        Alllayout.addWidget(AuthWidget)
        Alllayout.addWidget(SeveWidget)
        self.AuthSelect.setLayout(Alllayout)
        self.AuthSelect.show()
    
    def PreviewResolution(self):
        Row = self.AgendaTable.currentRow()
        #CurrentSelection = self.Resolution.currentText()
        self.InputWindow = QtWidgets.QWidget()
        pyside_dynamic.loadUi('Resources/ui/Preview.ui', self.InputWindow)
        NarrationText=(self.AgendaDict[Row][0].replace('\\n','\n'))
        ResolutionText=(self.AgendaDict[Row][1].replace('\\n','\n'))
        self.InputWindow.NarrationPreview.setText(self.NarrationText)
        self.InputWindow.ResolutionPreview.setText(self.ResolutionText)
        self.InputWindow.Title.setText(self.AgendaDict[Row][1])
        self.InputWindow.NarrationPreview.setText(self.AgendaDict[Row][1])
        self.InputWindow.ResolutionPreview.setText(self.AgendaDict[Row][2])
        self.InputWindow.show()


    def handleHeaderMenu_client(self, pos):
        x,y = pos.x(), pos.y()
        it = self.AgendaTable.indexAt(pos)
        row = it.row()
        if it is None: return
        menu = QtWidgets.QMenu()
        edit = menu.addAction("Delete")
        action = menu.exec_(self.AgendaTable.viewport().mapToGlobal(pos))
        if action == edit:
            self.AgendaTable.removeRow(row)
            
    def findfinyear(self,date):
        try:
            if date.month<=3:
                return str(int(date.year)-1)+'-'+str(int(date.year))[-2:]
            else:
                return str(int(date.year))+'-'+str(int(date.year)+1)[-2:]
        except:
            if date.month()<=3:
                return str(int(date.year())-1)+'-'+str(int(date.year()))
            else:
                return str(int(date.year()))+'-'+str(int(date.year())+1)

    def LiveFill(self,index,Row,item):
        sendText = '{'+item+'}'
        label = self.VariableWidget.variableTable.item(index,0).text()
        key = label.lower().replace(' ','_')
        variable = '{'+key+'}'
        NarText = self.VariableWidget.NarrationPreview.toPlainText()
        ResText = self.VariableWidget.ResolutionPreview.toPlainText()
        if self.VariableStore[Row][key]=='':
            NewNarText = NarText.replace(variable,sendText)
            NewResText = ResText.replace(variable,sendText)
        else:
            NewNarText = NarText.replace(self.VariableStore[Row][key],sendText)
            NewResText = ResText.replace(self.VariableStore[Row][key],sendText)
        self.VariableWidget.NarrationPreview.setText(NewNarText)
        self.VariableWidget.ResolutionPreview.setText(NewResText)
        self.VariableStore[Row][key]=sendText
        
    def dateUpdate(self,index,Row,childwidget,item):
        dateFormatWidget = childwidget.findChild(QtWidgets.QComboBox)
        dateWidget = childwidget.findChild(QtWidgets.QDateEdit)
        pyDate = dateWidget.date().toPython()
        formattedDate = '{'+pyDate.strftime(dateFormatWidget.currentText())+'}'
        label = self.VariableWidget.variableTable.item(index,0).text()
        key = label.lower().replace(' ','_')
        variable = '{'+key+'}'
        NarText = self.VariableWidget.NarrationPreview.toPlainText()
        ResText = self.VariableWidget.ResolutionPreview.toPlainText()
        if self.VariableStore[Row][key]=='':
            NewNarText = NarText.replace(variable,formattedDate)
            NewResText = ResText.replace(variable,formattedDate)
        else:
            NewNarText = NarText.replace(self.VariableStore[Row][key],formattedDate)
            NewResText = ResText.replace(self.VariableStore[Row][key],formattedDate)
        self.VariableWidget.NarrationPreview.setText(NewNarText)
        self.VariableWidget.ResolutionPreview.setText(NewResText)
        self.VariableStore[Row][key]=formattedDate

    def TimeUpdate(self,index,Row,childwidget,item):
        dateFormatWidget = childwidget.findChild(QtWidgets.QLineEdit)
        dateWidget = childwidget.findChild(QtWidgets.QTimeEdit)
        pyDate = dateWidget.time().toPython()
        TimeR = pyDate.strftime('%I:%M %p')
        if dateFormatWidget.text()!='':
            TimeR = TimeR+" ("+dateFormatWidget.text()+")"
        formattedDate = '{'+TimeR+'}'
        label = self.VariableWidget.variableTable.item(index,0).text()
        key = label.lower().replace(' ','_')
        variable = '{'+key+'}'
        NarText = self.VariableWidget.NarrationPreview.toPlainText()
        ResText = self.VariableWidget.ResolutionPreview.toPlainText()
        if self.VariableStore[Row][key]=='':
            NewNarText = NarText.replace(variable,formattedDate)
            NewResText = ResText.replace(variable,formattedDate)
        else:
            NewNarText = NarText.replace(self.VariableStore[Row][key],formattedDate)
            NewResText = ResText.replace(self.VariableStore[Row][key],formattedDate)
        self.VariableWidget.NarrationPreview.setText(NewNarText)
        self.VariableWidget.ResolutionPreview.setText(NewResText)
        self.VariableStore[Row][key]=formattedDate
        
    def generateDoc(self):
        if not self.isAttendanceSelected:
            QtWidgets.QMessageBox.warning(self,'Alert!!','Please select attendees for the meeting.')
        else:
            #Letterhead Items
            self.conn = sqlite3.connect(self.dbfilepath)
            self.cur = self.conn.cursor()
            RegOffice = self.cur.execute(f'SELECT company_registered_address from Masterdata WHERE company_name = "{self.currentselection}"').fetchall()[0][0]
            self.conn = sqlite3.connect(self.dbfilepath)
            self.cur = self.conn.cursor()
            agenda_list_for_doc = []
            for ROW in range(self.AgendaTable.rowCount()):
                if isinstance(self.AgendaTable.cellWidget(ROW,0), QtWidgets.QComboBox):
                    pass
                else:
                    infoCol = self.AgendaTable.item(ROW,1)
                    if infoCol is not None and self.AgendaTable.item(ROW,1).text()!='':
                        infoTitle = self.AgendaTable.item(ROW,0).text()
                        infoText = self.AgendaTable.item(ROW,1).text()
                        self.SavedInfo[ROW+1] = [infoTitle,infoText,'']
            self.SavedInfo = dict(sorted(self.SavedInfo.items(), key=lambda item: item[0]))
            for key in self.SavedInfo.keys():
                temp_agenda_holder = {}
                Agenda = self.SavedInfo[key]
                NarText = Agenda[1]
                ResText = Agenda[2]
                if key-1 in self.VariableStore.keys():
                    for index in self.VariableStore[key-1].keys():
                        if self.VariableStore[key-1][index]=='':
                            variable = '{'+index+'}'
                            NarText = NarText.replace(variable,'_______')
                            ResText = ResText.replace(variable,'_______')
                temp_agenda_holder['TITLE'] = str(key)+'. '+Agenda[0]
                if Agenda[1]!='':
                    temp_agenda_holder['NARRATION'] = NarText.replace('{','').replace('}','').replace('\n\n','\n').replace('\n \n','\n').split('\n')
                else:
                    temp_agenda_holder['NARRATION'] = ''
                if Agenda[2]!='':
                    temp_agenda_holder['RESOLUTION'] = ResText.replace('{','').replace('}','').replace('\n\n','\n').replace('\n \n','\n').split('\n')
                else:
                    temp_agenda_holder['RESOLUTION'] = ''
                agenda_list_for_doc.append(temp_agenda_holder)
            if self.BoardMeeting.isChecked():
                MeetingType='Meeting of the Board of Directors'
                MeetingName = 'Board Meeting'
                MeetingNo = self.MeetingNo.value()
                #MeetShrt = 'BM_Extract_'+self.Title.text().replace(' ','_').replace('.','_')+'_'
            elif self.Committee.isChecked():
                MeetingType=f'Meeting of {self.commiteeName.currentText()}'
                MeetingName = 'Committee Meeting'
                MeetingNo = self.MeetingNo.value()
                #MeetShrt = 'Committee_Extract_'+self.Title.text().replace(' ','_').replace('.','_')+'_'
            elif self.AGM.isChecked():
                MeetingType='Annual General Meeting'
                MeetingName = 'Annual General Meeting'
                MeetingNo = self.MeetingNo.value()
                #MeetShrt = 'AGM_Extract_'+self.Title.text().replace(' ','_').replace('.','_')+'_'
            elif self.EGM.isChecked():
                MeetingType='Extra-Ordinary General Meeting'
                MeetingName = 'Extra Ordinary General Meeting'
                MeetingNo = ''
                #MeetShrt = 'EGM_Extract_'+self.Title.text().replace(' ','_').replace('.','_')+'_'

            print(agenda_list_for_doc)
            Minute = Minutes.createDoc()
            Minute.formatMinutes(self.MeetingNo.value(),self.fy.text())
            RegOffSwitch = RegOffice if self.VenueSelect.text().lower()=='registered office' else self.VenueSelect.text()
            Minute.Boardmeetingdetails(self.CoName, self.MeetingNo.value(),MeetingType,MeetingName,self.fy.text(),self.TmzSelect.currentText(), self.DateSelection.date().toPython(),self.TimeSelect.time().toPython(),RegOffSwitch)
            Minute.BMattendance(self.AttendeesList, MeetingName)
            Minute.Agendas(self.TimeSelect.time().toPython().strftime('%I.%M %p'),agenda_list_for_doc,self.exPlace.text(),self.exDate.date().toPython().strftime('%d.%m.%Y') )
            Minute.saveDoc('TestMinutes')
            self.Feedback('Success','The Document created sucessfully',"View Document")
    
    def Feedback(self,action,Message,link=None):
        self.FeedBackWin = QtWidgets.QWidget()
        pyside_dynamic.loadUi('Resources/ui/feedback.ui',self.FeedBackWin)
        self.FeedBackWin.Message.setText(Message)
        if link:
            self.FeedBackWin.link.setText(link)
            self.FeedBackWin.link.clicked.connect(self.openDoc)
        if action=='Success':
            self.FeedBackWin.Icon.setPixmap(QtGui.QPixmap(QtGui.QImage("Resources/Icon/tick.png")))
        if action=='Failed':
            self.FeedBackWin.Icon.setPixmap(QtGui.QPixmap(QtGui.QImage("Resources/Icon/close.png")))
        if action=='Warning':
            self.FeedBackWin.Icon.setPixmap(QtGui.QPixmap(QtGui.QImage("Resources/Icon/warning.png")))
        self.FeedBackWin.show()

    def openDoc(self):
        self.FeedBackWin.close()
        os.startfile('"TestMinutes.docx"')
        
        
