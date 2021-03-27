from PySide2 import QtWidgets, QtUiTools,QtCore, QtGui
import sys
import os
sys.path.append(os.path.abspath(os.path.join('..')))
import HomePage
import pickle
from functions import Database_Manager as db
from functions import pyside_dynamic
from functions.generateDocuments import MeetingExtracts
from pathlib import Path
import sqlite3
import re
import json
import datetime
import webbrowser
from functools import partial

class Ui(QtWidgets.QWidget):
    def __init__(self):
        super(Ui, self).__init__()
        pyside_dynamic.loadUi('Resources/ui/QuickResolution.ui',self)
        with open('Config','rb') as f:
            self.Config = pickle.loads(f.read())
            f.close()
        self.dbfilepath = os.path.join(self.Config['Database'],'C3_DataBase.db')
        self.resolutionspath = os.path.join(self.Config['Database'],'Resolutions.db')
        self.adjustSize()
        self.DateFormats=['%d.%m.%Y','%d/%m/%Y','%B %e, %Y','%A, %B %e, %Y']
        self.AuthorizedContainer = []
        self.AuthTracker = {}
        self.conn = sqlite3.connect(self.resolutionspath)
        self.cur = self.conn.cursor()
        self.Resolution = self.findChild(QtWidgets.QComboBox, 'ResolutionType')
        self.Authorizations = {}
        try:
            ResolutionListdb = self.cur.execute('SELECT "DESCRIPTION" from Resolutions').fetchall()
        except:
            ErrorMessage =  QtWidgets.QMessageBox()
            ErrorMessage.setIcon(QtWidgets.QMessageBox.Warning)
            ErrorMessage.setText("No Resolutions Found in Database")
            ErrorMessage.setInformativeText("Please refer this to admin and add resolutions")
            ErrorMessage.setWindowTitle("Resolutions Not Found")
            ErrorMessage.setStandardButtons(QtWidgets.QMessageBox.Ok)
            ErrorMessage.buttonClicked.connect(self.GotoDashBoard)
            ErrorMessage.show()
            
        ResolutionList=['']
        for item in ResolutionListdb:
            ResolutionList.append(item[0])
        self.Resolution.addItems(ResolutionList)
        self.Resolution.activated.connect(self.getResolution)
        self.InputFieldsShow = self.findChild(QtWidgets.QWidget, 'FieldView')
        self.InputLayout = QtWidgets.QFormLayout()
        self.CompanySelection = self.findChild(QtWidgets.QComboBox, 'CompanySelection')
        self.conn = sqlite3.connect(self.dbfilepath)
        self.cur = self.conn.cursor()
        CompanyListdb = self.cur.execute('SELECT "company_name" from Masterdata').fetchall()
        CompanyList=['']
        for item in CompanyListdb:
            CompanyList.append(item[0])
        self.CompanySelection.addItems(CompanyList)
        self.CompanySelection.activated.connect(self.getCompanyData)
        self.DateSelection = self.findChild(QtWidgets.QDateEdit, 'DateSelection')
        self.DateSelection.setDateTime(QtCore.QDateTime.currentDateTime())
        self.TimeSelect = self.findChild(QtWidgets.QTimeEdit, 'TimeSelect')
        self.TimeSelect.setTime(QtCore.QTime.currentTime())
        self.VenueSelect = self.findChild(QtWidgets.QLineEdit, 'VenueSelect')
        self.NarrationPreview = self.findChild(QtWidgets.QTextEdit, 'NarrationPreview')
        self.ResolutionPreview = self.findChild(QtWidgets.QTextEdit, 'ResolutionPreview')
        self.GenerateDoc = self.findChild(QtWidgets.QPushButton, 'GenerateDoc')  
        self.GenerateDoc.clicked.connect(self.ExportDocx)
        self.Committee.clicked.connect(self.enableCommittee)
        self.BoardMeeting.clicked.connect(self.enableCommittee)
        self.EGM.clicked.connect(self.enableCommittee)
        self.AGM.clicked.connect(self.enableCommittee)

        

    def getCompanyData(self):
        self.currentCompany = self.CompanySelection.currentText()
        self.conn = sqlite3.connect(self.dbfilepath)
        self.cur = self.conn.cursor()
        self.CompanyData = self.cur.execute(f'SELECT * from Masterdata WHERE "company_name" = "{self.currentCompany}"').fetchall()[0]
        self.CompanyCIN = self.CompanyData[0]
        self.SignatoriesData = self.cur.execute(f'SELECT * from Signatories WHERE "company_cin" = "{self.CompanyCIN}"').fetchall()
        self.DirectorList=['']
        for item in self.SignatoriesData:
            self.DirectorList.append(item[2])
        self.Signedby.clear()
        self.Signedby.addItems(self.DirectorList)
        

    def GotoDashBoard(self):
        pass
    
    def getResolution(self):
        CompanySelection = self.CompanySelection.currentText()
        if CompanySelection=='':
            QtWidgets.QMessageBox.warning(self,'Alert!!','Please select Company')
            self.Resolution.setCurrentIndex(0)
        else:
            CurrentSelection = self.Resolution.currentText()
            #ResolutionsFile
            self.conn = sqlite3.connect(self.resolutionspath)
            self.cur = self.conn.cursor()
            self.ResolutionData = self.cur.execute(f'SELECT * from Resolutions WHERE DESCRIPTION = "{CurrentSelection}"').fetchall()[0]

            #DbFile
            self.ResolutionTitle = self.ResolutionData[2]
            self.Fields = eval(self.ResolutionData[7])
            self.variableTable.setRowCount(len(self.Fields))
            for rowcount,field in enumerate(self.Fields):
                item = QtWidgets.QTableWidgetItem()
                self.variableTable.setItem(rowcount, 0, item)
                item.setText(field[0])
                if 'date' in field[1].lower():
                    print('date Wifdget')
                    varWidget = QtWidgets.QWidget()
                    layout = QtWidgets.QHBoxLayout()
                    DateField = QtWidgets.QDateEdit()
                    DateField.setDisplayFormat('dd.MM.yyyy')
                    DateField.setDateTime(QtCore.QDateTime.currentDateTime())
                    DateField.dateChanged.connect(partial(self.dateUpdate,rowcount,varWidget))
                    formatList = QtWidgets.QComboBox()
                    formatList.addItems(self.DateFormats)
                    formatList.activated.connect(partial(self.dateUpdate,rowcount,varWidget))
                    layout.addWidget(DateField)
                    layout.addWidget(formatList)
                    layout.setContentsMargins(0,0,0,0)
                    varWidget.setLayout(layout)
                elif 'time' in field[1].lower():
                    varWidget = QtWidgets.QWidget()
                    layout = QtWidgets.QHBoxLayout()
                    TimeField = QtWidgets.QTimeEdit()
                    TimeField.setDisplayFormat('h:mm AP')
                    TimeField.setTime(QtCore.QTime.currentTime())
                    TimeField.timeChanged.connect(partial(self.TimeUpdate,rowcount,varWidget))
                    formatList = QtWidgets.QLineEdit()
                    formatList.setText('IST')
                    formatList.textChanged.connect(partial(self.TimeUpdate,rowcount,varWidget))
                    layout.addWidget(TimeField)
                    layout.addWidget(formatList)
                    layout.setContentsMargins(0,0,0,0)
                    varWidget.setLayout(layout)
                elif 'din' in field[1].lower():
                    varWidget = QtWidgets.QLineEdit()
                    varWidget.textChanged.connect(partial(self.LiveFill,rowcount))
                    varWidget.setValidator(QtGui.QIntValidator())
                    varWidget.setMaxLength(8)
                elif 'cin' in field[1].lower():
                    varWidget = QtWidgets.QLineEdit()
                    varWidget.textChanged.connect(partial(self.LiveFill,rowcount))
                    varWidget.setMaxLength(21)
                elif 'authorization' == field[1].lower():
                    varWidget = QtWidgets.QPushButton()
                    varWidget.setText("Select Authorizations")
                    self.AuthTracker[field[0]] = []
                    varWidget.clicked.connect(partial(self.selectAuthorization,field[0],varWidget,rowcount))
                else:
                    varWidget = QtWidgets.QLineEdit()
                    varWidget.textChanged.connect(partial(self.LiveFill,rowcount))
                self.variableTable.setCellWidget(rowcount, 1, varWidget)   
            self.NarrationText=(self.ResolutionData[5].replace('\\n','\n'))
            self.ResolutionText=(self.ResolutionData[6].replace('\\n','\n'))
            self.Title.setText(CurrentSelection.upper())
            self.NarrationPreview.setText(self.NarrationText)
            self.ResolutionPreview.setText(self.ResolutionText)
            self.VariableStore = {}
            VariablesList = []
            VariablesList= VariablesList+re.findall(r"\{(\w+)\}",self.NarrationText)
            VariablesList= VariablesList+re.findall(r"\{(\w+)\}",self.ResolutionText)
            VariablesList = list(set(VariablesList))
            for variable in VariablesList:
                self.VariableStore[variable]=''

            #Check Previous resolutions
            activities = os.path.join(self.Config['Database'],'activities.db')
            conn = sqlite3.connect(activities)
            cur = conn.cursor()
            xDate = datetime.datetime.strftime(datetime.datetime.strptime(self.DateSelection.date().toString(),'%a %b %d %Y').date(),'%d.%m.%Y')
            activitiesList = cur.execute(f'SELECT * from activities WHERE "company_cin" = "{self.CompanyCIN}" AND "date" = "{xDate}" AND "description" = "{self.ResolutionData[2].title()}"').fetchall()
            if activitiesList:
                self.activitiesView = QtWidgets.QWidget()
                pyside_dynamic.loadUi('Resources/ui/meetingsList.ui',self.activitiesView)
                self.activitiesView.differentBtn.clicked.connect(self.closeActivity)
                self.activitiesView.meetingTable.setRowCount(len(activitiesList))
                self.activitiesView.meetingTable.itemDoubleClicked.connect(self.OpenLink)
                self.activitiesView.setWindowModality(QtCore.Qt.ApplicationModal)
                for x, activity in enumerate(activitiesList):
                    filterList = [x for x in [x if activity.index(x) in (1,4,6,8) else None for x in activity] if x]
                    for y in range(len(filterList)):
                        item = QtWidgets.QTableWidgetItem()
                        self.activitiesView.meetingTable.setItem(x, y, item)
                        item.setText(str(filterList[y]))
                        item.setFlags(QtCore.Qt.ItemIsEnabled)
                self.activitiesView.show()

    def closeActivity(self):
        self.activitiesView.close()

    def OpenLink(self,item):
        parentWidget = item.tableWidget()
        if item.column() == 3:
            self.activitiesView.close()
            webbrowser.open((parentWidget.item(item.row(),3).text()+'.docx'))

    def disableButtons(self,BTGroup,_):
        needtoDisable = False if self.AuthorizationsWindow.selectAll.isChecked() else True
        for button in BTGroup.buttons():
            button.setEnabled(needtoDisable)
            
    def selectAuthorization(self,label,sender,index):
        self.AuthorizationsWindow = QtWidgets.QWidget()
        key = label.lower().replace(' ','_')
        keyText = self.VariableStore[key]
        pyside_dynamic.loadUi('Resources/ui/AddAuthorizations.ui', self.AuthorizationsWindow)
        self.AuthorizationsWindow.Done = self.AuthorizationsWindow.findChild(QtWidgets.QPushButton, 'Done')
        self.AuthorizationsWindow.AddOfficer = self.AuthorizationsWindow.findChild(QtWidgets.QPushButton, 'AddOfficer')
        self.AuthorizationsWindow.BacktoRes = self.AuthorizationsWindow.findChild(QtWidgets.QPushButton, 'BacktoRes')
        self.AuthorizationsWindow.selectionWindow = self.AuthorizationsWindow.findChild(QtWidgets.QWidget, 'SelectionWindow')
        layout = QtWidgets.QVBoxLayout()
        Font = QtGui.QFont("Open Sans", 10)
        self.DesignationPriority = {"Managing Director": 0, "Wholetime Director": 1, "Director": 2, "Additional Director": 3,
                               "Alternate Director": 4, "Nominee Director": 4,"Company Secretary": 5, "CEO(KMP)" : 6 , 'CFO(KMP)' : 7}
        self.SignatoriesData.sort(key=lambda val: self.DesignationPriority[val[4]])
        self.AuthorizationsWindow.BTGroup = QtWidgets.QButtonGroup()
        for director in self.SignatoriesData:
            title = 'Ms.' if director[11].lower()=='feml' else 'Mr.'
            if director[11]=='':
                title = ''
            item = QtWidgets.QCheckBox(title+director[2].title()+', '+director[4])
            item.setFont(Font)
            layout.addWidget(item)
            self.AuthorizationsWindow.BTGroup.addButton(item)
        self.AuthorizationsWindow.BTGroup.setExclusive(False)
        if label in self.AuthTracker.keys():
            for idx in self.AuthTracker[label]:
                self.AuthorizationsWindow.BTGroup.button(idx).setChecked(True)
        self.AuthorizationsWindow.selectAll.stateChanged.connect(partial(self.disableButtons,self.AuthorizationsWindow.BTGroup))
        if 'severally' in keyText:
            self.AuthorizationsWindow.severally.setChecked(True)
        if 'collectively' in keyText:
            self.AuthorizationsWindow.collectively.setChecked(True)
        self.AuthorizationsWindow.Done.clicked.connect(partial(self.updateResolutions,index,self.AuthorizationsWindow.selectAll,self.AuthorizationsWindow.severally,self.AuthorizationsWindow.collectively))
        self.AuthorizationsWindow.selectionWindow.setLayout(layout)
        self.AuthorizationsWindow.show()

    def updateResolutions(self,index,allAuth,SeveBox,CollBox):
        label = self.variableTable.item(index,0).text()
        self.AuthorizedContainer = []
        self.AuthTracker[label] = []
        for button in self.AuthorizationsWindow.BTGroup.buttons():
            if button.isChecked():
                self.AuthorizedContainer.append(button.text())
                self.AuthTracker[label].append(self.AuthorizationsWindow.BTGroup.id(button))
        key = label.lower().replace(' ','_')
        variable = '{'+key+'}'
        NarText = self.NarrationPreview.toPlainText()
        ResText = self.ResolutionPreview.toPlainText()
        if allAuth.isChecked():
            authorizationText = "the Directors of the Company be and are hereby authorized "
            SeveText = ''
            if SeveBox.isChecked() and not CollBox.isChecked():
                if self.VariableStore[key]=='':
                    pass
                else:
                    SeveText = ' severally'
            if not SeveBox.isChecked() and CollBox.isChecked():
                if self.VariableStore[key]=='':
                    pass
                else:
                    SeveText = ' collectively'
            if SeveBox.isChecked() and CollBox.isChecked():
                if self.VariableStore[key]=='':
                    pass
                else:
                    SeveText = ' severally/collectively'
            authorizationText = authorizationText+SeveText
            if self.VariableStore[key]=='':
                NewNarText = NarText.replace(variable,authorizationText)
                NewResText = ResText.replace(variable,authorizationText)
            else:
                NewNarText = NarText.replace(self.VariableStore[key],authorizationText)
                NewResText = ResText.replace(self.VariableStore[key],authorizationText)
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
            if self.VariableStore[key]=='':
                NewNarText = NarText.replace(variable,authorizationText)
                NewResText = ResText.replace(variable,authorizationText)
            else:
                NewNarText = NarText.replace(self.VariableStore[key],authorizationText)
                NewResText = ResText.replace(self.VariableStore[key],authorizationText)
        self.NarrationPreview.setText(NewNarText)
        self.ResolutionPreview.setText(NewResText)
        self.VariableStore[key]=authorizationText
        self.AuthorizationsWindow.close()
        self.AuthorizedContainer=[]      


    def enableCommittee(self):
        sender =(self.sender())
        BtButton = sender.objectName()
        if BtButton=='Committee':
            self.commiteeName.setEnabled(True)
        else:
            self.commiteeName.setEnabled(False)
            self.commiteeName.setText('')


    def setBlank(self):
        for key in self.VariableStore.keys():
            if self.VariableStore[key]=='':
                variable = '{'+key+'}'
                NarText = self.NarrationPreview.toPlainText()
                ResText = self.ResolutionPreview.toPlainText()
                NewNarText = NarText.replace(variable,'_______')
                NewResText = ResText.replace(variable,'_______')
                self.NarrationPreview.setText(NewNarText)
                self.ResolutionPreview.setText(NewResText)
            

    def ExportDocx(self):
        self.setBlank()
        self.conn = sqlite3.connect(self.dbfilepath)
        self.cur = self.conn.cursor()
        CompanyInfo = self.cur.execute(f'SELECT * from Masterdata WHERE "company_name" = "{self.CompanySelection.currentText()}"').fetchall()
        meta= self.cur.execute("PRAGMA table_info(Masterdata)").fetchall()
        tableDict = {}
        print(CompanyInfo)
        print(meta)
        loop_count = 0
        for item in meta:
            tableDict[item[1]] = CompanyInfo[0][loop_count]
            loop_count+=1
        if self.BoardMeeting.isChecked():
            MeetingType='Meeting of the Board of Directors'
            MeetingName = 'Board Meeting'
            MeetingNo = self.MeetingNo.value()
            MeetShrt = 'BM_Extract_'+self.Title.text().replace(' ','_').replace('.','_')+'_'
        elif self.Committee.isChecked():
            MeetingType=f'Meeting of the members of {self.commiteeName.text()}'
            MeetingName = 'Committee Meeting'
            MeetingNo = self.MeetingNo.value()
            MeetShrt = 'Committee_Extract_'+self.Title.text().replace(' ','_').replace('.','_')+'_'
        elif self.AGM.isChecked():
            MeetingType='Annual General Meeting'
            MeetingName = 'Annual General Meeting'
            MeetingNo = self.MeetingNo.value()
            MeetShrt = 'AGM_Extract_'+self.Title.text().replace(' ','_').replace('.','_')+'_'
        elif self.EGM.isChecked():
            MeetingType='Extra-Ordinary General Meeting'
            MeetingName = 'Extra Ordinary General Meeting'
            MeetingNo = ''
            MeetShrt = 'EGM_Extract_'+self.Title.text().replace(' ','_').replace('.','_')+'_'
        FinYear = None
        MeetNo = None
        if not self.ignoreFY.isChecked():
            FinYear = self.fy_2.text()
        if not self.ignoreMeetingNo.isChecked():
            MeetNo = self.MeetingNo.value()
        if self.blankFy.isChecked():
            FinYear = '_'*7
        if self.blankMN.isChecked():
            MeetNo = '_'*3
        Document = MeetingExtracts.createDoc()
        Document.letterhead(tableDict['company_name'],tableDict['company_registered_address'],tableDict['company_cin'],tableDict['company_email_id'],tableDict['company_phone'],NoLetterHead=self.isLetterhead.isChecked())
        Document.ExtractHeader(MeetingType,tableDict['company_name'],tableDict['company_registered_address'],self.DateSelection.date().toPython(),self.TimeSelect.time().toPython(),FinYear,MeetNo)
        NarTextFinal = self.NarrationPreview.toPlainText().replace('{','').replace('}','').split('\n')
        ResTextFinal = self.ResolutionPreview.toPlainText().replace('{','').replace('}','').split('\n')
        Document.ExtractText(self.Title.text(),NarTextFinal,ResTextFinal)
        SignedByAuth = self.Signedby.currentText()
        SignedByInfo = self.cur.execute(f'SELECT director_din, Designation,director_address from Signatories WHERE company_cin = "{self.CompanyCIN}" AND director_name = "{SignedByAuth}"').fetchall()[0]
        Document.Signatures(self.CompanySelection.currentText(), SignedByAuth, SignedByInfo[1], SignedByInfo[0], SignedByInfo[2])
        Path(os.path.join(self.Config['Home'],self.CompanySelection.currentText(),self.findfinyear(self.DateSelection.date()),MeetingName,datetime.datetime.strftime(datetime.datetime.strptime(self.DateSelection.date().toString(),'%a %b %d %Y').date(),'%d.%m.%Y'))).mkdir(parents=True, exist_ok=True)
        self.filepath = os.path.join(self.Config['Home'],self.CompanySelection.currentText(),self.findfinyear(self.DateSelection.date()),MeetingName,datetime.datetime.strftime(self.DateSelection.date().toPython(),'%d.%m.%Y'),MeetShrt+datetime.datetime.strftime(datetime.datetime.strptime(self.DateSelection.date().toString(),'%a %b %d %Y').date(),'%d_%m_%Y'))
        Document.saveDoc(self.filepath)
        with open('_temp/_currentuser','rb') as currentUser:
            self.Userdata = pickle.loads(currentUser.read())
            currentUser.close()
        CurrentUserName = self.Userdata['CurrentUser']
        data = json.dumps([self.Title.text(),NarTextFinal,ResTextFinal])
        dbData = [tableDict['company_cin'],datetime.datetime.now().strftime('%d.%m.%Y'),datetime.datetime.strftime(datetime.datetime.strptime(self.DateSelection.date().toString(),'%a %b %d %Y').date(),'%d.%m.%Y'),\
                  'Meeting',MeetingName,self.ResolutionData[2].title(),self.findfinyear(self.DateSelection.date()),CurrentUserName,data,self.filepath]    
        db.Activities(dbData)
        extractData = [tableDict['company_cin'],datetime.datetime.strftime(datetime.datetime.strptime(self.DateSelection.date().toString(),'%a %b %d %Y').date(),'%d.%m.%Y'),MeetingName,\
                self.findfinyear(self.DateSelection.date()),CurrentUserName,self.filepath]    
        db.Extracts(extractData)
        self.Feedback('Success','Document Generated Successfully',"View Document")
    
        
    def ErrorWindow(host,Message):
        self.ErrorMessage = QtWidgets.QMessageBox(host)
        self.ErrorMessage.setIcon(QtWidgets.QMessageBox.Information)
        self.ErrorMessage.setText(Message)
        self.ErrorMessage.setWindowTitle('Alert!!')
        self.Ido = QtWidgets.QPushButton()
        self.Ido.setText('Yes I do')
        self.Ido.clicked.connect(self.accept)
        self.ErrorMessage.addButton(self.Ido, QtWidgets.QMessageBox.YesRole)
        self.ErrorMessage.addButton(self.idont, QtWidgets.QMessageBox.NoRole)
        self.ErrorMessage.show()

    def genVariableField(self,label,Widget,Prefill=None):
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(Widget)
        widget.setLayout(layout)
        return widget
        
    def LiveFill(self,index,item):
        print(item, index)
        sendText = '{'+item+'}'
        label = self.variableTable.item(index,0).text()
        key = label.lower().replace(' ','_')
        variable = '{'+key+'}'
        NarText = self.NarrationPreview.toPlainText()
        ResText = self.ResolutionPreview.toPlainText()
        if self.VariableStore[key]=='':
            NewNarText = NarText.replace(variable,sendText)
            NewResText = ResText.replace(variable,sendText)
        else:
            NewNarText = NarText.replace(self.VariableStore[key],sendText)
            NewResText = ResText.replace(self.VariableStore[key],sendText)
        self.NarrationPreview.setText(NewNarText)
        self.ResolutionPreview.setText(NewResText)
        self.VariableStore[key]=sendText
        
    def dateUpdate(self,index,childwidget,item):
        dateFormatWidget = childwidget.findChild(QtWidgets.QComboBox)
        dateWidget = childwidget.findChild(QtWidgets.QDateEdit)
        pyDate = dateWidget.date().toPython()
        formattedDate = '{'+pyDate.strftime(dateFormatWidget.currentText())+'}'
        label = self.variableTable.item(index,0).text()
        key = label.lower().replace(' ','_')
        variable = '{'+key+'}'
        NarText = self.NarrationPreview.toPlainText()
        ResText = self.ResolutionPreview.toPlainText()
        if self.VariableStore[key]=='':
            NewNarText = NarText.replace(variable,formattedDate)
            NewResText = ResText.replace(variable,formattedDate)
        else:
            NewNarText = NarText.replace(self.VariableStore[key],formattedDate)
            NewResText = ResText.replace(self.VariableStore[key],formattedDate)
        self.NarrationPreview.setText(NewNarText)
        self.ResolutionPreview.setText(NewResText)
        self.VariableStore[key]=formattedDate

    def TimeUpdate(self,index,childwidget,item):
        dateFormatWidget = childwidget.findChild(QtWidgets.QLineEdit)
        dateWidget = childwidget.findChild(QtWidgets.QTimeEdit)
        pyDate = dateWidget.time().toPython()
        TimeR = pyDate.strftime('%I:%M %p')
        if dateFormatWidget.text()!='':
            TimeR = TimeR+" ("+dateFormatWidget.text()+")"
        formattedDate = '{'+TimeR+'}'
        label = self.variableTable.item(index,0).text()
        key = label.lower().replace(' ','_')
        variable = '{'+key+'}'
        NarText = self.NarrationPreview.toPlainText()
        ResText = self.ResolutionPreview.toPlainText()
        if self.VariableStore[key]=='':
            NewNarText = NarText.replace(variable,formattedDate)
            NewResText = ResText.replace(variable,formattedDate)
        else:
            NewNarText = NarText.replace(self.VariableStore[key],formattedDate)
            NewResText = ResText.replace(self.VariableStore[key],formattedDate)
        self.NarrationPreview.setText(NewNarText)
        self.ResolutionPreview.setText(NewResText)
        self.VariableStore[key]=formattedDate

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
        os.startfile('"'+self.filepath+'.docx'+'"')

def clearLayout(layout):
    while layout.count():
        child = layout.takeAt(0)
        if child.widget() is not None:
            child.widget().deleteLater()
        elif child.layout() is not None:
            clearLayout(child.layout())
        
