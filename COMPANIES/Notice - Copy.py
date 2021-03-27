from PySide2 import QtWidgets, QtUiTools,QtCore, QtGui
import sys
import os
sys.path.append(os.path.abspath(os.path.join('..')))
import HomePage
 
from functions import Database_Manager as db
from functions import ExportToDoc, pyside_dynamic
from pathlib import Path
import datetime
import sqlite3
import pickle


class Ui(QtWidgets.QWidget):
    def __init__(self):
        super(Ui, self).__init__()
        pyside_dynamic.loadUi('../Resources/ui/Notice.ui',self)
        with open('Config','rb') as f:
            Config = pickle.loads(f.read())
            f.close()
        self.dbfilepath = os.path.join(Config['Database'],'C3_DataBase.db')
        self.resolutionspath = os.path.join(Config['Database'],'Resolutions.db')
        self.conn = sqlite3.connect(self.dbfilepath)
        self.cur = self.conn.cursor()
        self.SignNO = 4
        self.CompanySelection = self.findChild(QtWidgets.QComboBox, 'CompanySelection')
        CompanyListdb = self.cur.execute('SELECT "company_name" from Masterdata').fetchall()
        self.conn = sqlite3.connect(self.resolutionspath)
        self.cur = self.conn.cursor()
        self.AgendaItems = self.cur.execute('SELECT TITLE from Resolutions').fetchall()
        self.AgendaList=['']
        for item in self.AgendaItems:
            self.AgendaList.append(item[0])
        self.NosofAgenda = self.findChild(QtWidgets.QComboBox, 'AgendaNos')
        self.NosofAgenda.setEnabled(False)
        NosList = list(map(str,list(range(1,100))))
        self.NosofAgenda.currentIndexChanged.connect(self.expandAgendas)
        self.NosofAgenda.addItems(NosList)
        CompanyList=['']
        for item in CompanyListdb:
            CompanyList.append(item[0])
        self.CompanySelection.addItems(CompanyList)
        self.CompanySelection.activated.connect(self.GetSignatoriesList)
        self.AgendaNoteList = {}
        self.AgendaTable = self.findChild(QtWidgets.QTableWidget, 'AgendaTable')
        self.AgendaTable.resizeRowsToContents()
        self.AgendaTable.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.AgendaTable.customContextMenuRequested.connect(self.handleHeaderMenu_client)
##        self.AgendaTable.setRowCount(1)
##        comboBox = QtWidgets.QComboBox()
##        comboBox.addItems(self.AgendaList)
##        comboBox.setEditable(True)
##        comboBox.currentIndexChanged.connect(self.Selectionfill)
##        self.AgendaTable.setCellWidget(0, 0, comboBox)
        self.DateSelection = self.findChild(QtWidgets.QDateEdit, 'DateSelection')
        self.DateSelection.setDateTime(QtCore.QDateTime.currentDateTime())
        self.TimeSelect = self.findChild(QtWidgets.QTimeEdit, 'TimeSelect')
        self.TimeSelect.setTime(QtCore.QTime.currentTime())
        self.VenueSelect = self.findChild(QtWidgets.QLineEdit, 'VenueSelect')
        self.GenerateNotice = self.findChild(QtWidgets.QPushButton, 'GenerateNotice')
        self.GenerateNotice.clicked.connect(self.generateNoticeDoc)
        self.show()


    def Selectionfill(self):
        item = QtWidgets.QTableWidgetItem()
        self.AgendaTable.setItem(self.AgendaTable.currentRow(), 1, item)
        Agenda = self.AgendaTable.cellWidget(self.AgendaTable.currentRow(),0).currentText()
        self.conn = sqlite3.connect(self.resolutionspath)
        self.cur = self.conn.cursor()
        AgendaNote = self.cur.execute(f'SELECT SUMMARY from Resolutions WHERE TITLE = {repr(Agenda)}').fetchall()[0][0]
        item.setText(AgendaNote)
        self.AgendaTable.resizeRowsToContents()

    def GetSignatoriesList(self):
        self.NosofAgenda.setEnabled(True)
        self.currentselection = self.CompanySelection.currentText()
        self.conn = sqlite3.connect(self.dbfilepath)
        self.cur = self.conn.cursor()
        self.CINNum = self.cur.execute(f'SELECT company_cin from Masterdata WHERE company_name = "{self.currentselection}"').fetchall()[0][0]
        self.DirectorNames = self.cur.execute(f'SELECT director_name from Signatories WHERE company_cin = {repr(self.CINNum)}').fetchall()
        self.DirectorList=['']
        for item in self.DirectorNames:
            self.DirectorList.append(item[0])
        self.Signedby.clear()
        self.Signedby.addItems(self.DirectorList)
        self.SignNO = len(self.DirectorList)
        self.expandAgendas()
        
    def expandAgendas(self):
        self.AgendaTable.setRowCount(0)
        self.AgendaTable.setRowCount(4+int(self.NosofAgenda.currentText())+2)
        for x in range(4):
            item = QtWidgets.QTableWidgetItem()
            self.AgendaTable.setItem(x, 0, item)
            if x==0:
               item.setText("Chairman")
               item = QtWidgets.QTableWidgetItem()
               self.AgendaTable.setItem(x, 2, item)
               item.setText("APPROVAL") 
            elif x==1:
               item.setText("Quorum of the Meeting")
               item = QtWidgets.QTableWidgetItem()
               self.AgendaTable.setItem(x, 1, item)
               if self.SignNO<3:
                   item.setText("Both of the Directors are requested to attend the Meeting")
               else: 
                   item.setText("In accordance with Section 174, the quorum for the meeting shall be one third of its total strength or two directors, whichever is higher")
               item = QtWidgets.QTableWidgetItem()
               self.AgendaTable.setItem(x, 2, item)
               item.setText("NOTING") 
            elif x==2:
                item.setText("Leave of absence")
                item = QtWidgets.QTableWidgetItem()
                self.AgendaTable.setItem(x, 1, item)
                item.setText("To grant leave of absence to non attending directors.")
                item = QtWidgets.QTableWidgetItem()
                self.AgendaTable.setItem(x, 2, item)
                item.setText("NOTING")
            else:
                item.setText("Confirmation of Minutes of the previous Meeting.")
                item = QtWidgets.QTableWidgetItem()
                self.AgendaTable.setItem(x, 1, item)
                item.setText("The Minutes of the previous Meeting is to be circulated to the Directors for confirmation and noting.")
                item = QtWidgets.QTableWidgetItem()
                self.AgendaTable.setItem(x, 2, item)
                item.setText("NOTING")
        self.AgendaTable.resizeRowsToContents()
            
        for x in range(4,4+int(self.NosofAgenda.currentText())+2):
            if x<4+int(self.NosofAgenda.currentText()):
                comboBox = QtWidgets.QComboBox()
                comboBox.addItems(self.AgendaList)
                comboBox.setEditable(True)
                comboBox.currentIndexChanged.connect(self.Selectionfill)
                self.AgendaTable.setCellWidget(x, 0, comboBox)
                comboBox = QtWidgets.QComboBox()
                comboBox.addItems(['NOTING','APPROVAL','AUTHORIZATION'])
                comboBox.setEditable(True)
                self.AgendaTable.setCellWidget(x, 2, comboBox)
            elif x==4+int(self.NosofAgenda.currentText()):
                item = QtWidgets.QTableWidgetItem()
                self.AgendaTable.setItem(x, 0, item)
                item.setText("Any other business with the approval of the Board")
            elif x==4+int(self.NosofAgenda.currentText())+1:
                item = QtWidgets.QTableWidgetItem()
                self.AgendaTable.setItem(x, 0, item)
                item.setText("Vote of Thanks")
               
        
   
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
        if date.month()<=3:
            return str(int(date.year())-1)+'-'+str(int(date.year()))
        else:
            return str(int(date.year()))+'-'+str(int(date.year())+1)
        
    def generateNoticeDoc(self):
        #Letterhead Items
        self.conn = sqlite3.connect(self.dbfilepath)
        self.cur = self.conn.cursor()
        Lthead = self.cur.execute(f'SELECT company_registered_address,company_email_id from Masterdata WHERE company_name = "{self.currentselection}"').fetchall()[0]
        Notice=ExportToDoc.createDoc()
        Notice.letterhead(self.currentselection,Lthead[0],self.CINNum, Lthead[1],'')
        Notice.Noticetitle()
        Notice.NoticeTo(self.DirectorList)
        SignatoriesList=[]
        for x in range(self.AgendaTable.rowCount()):
            m=[]
            for y in range(self.AgendaTable.columnCount()):
                try:
                    m.append(self.AgendaTable.item(x,y).text())
                except:
                    try:
                        m.append(self.AgendaTable.cellWidget(x,y).currentText())
                    except:
                        m.append('')
            SignatoriesList.append(tuple(m))
        if self.BoardMeeting.isChecked():
            MeetingType='Meeting of the Board of Directors'
            MeetingNo = self.MeetingNo.value()
        elif self.AGM.isChecked():
            MeetingType='Annual General Meeting'
            MeetingNo = self.MeetingNo.value()
        elif self.EGM.isChecked():
            MeetingType='Extra-Ordinary General Meeting'
            MeetingNo = ''
        elif self.FBM.isChecked():
            MeetingType='First Board Meeting'
            MeetingNo = ''
        Notice.NoticeBody(MeetingNo,MeetingType,self.currentselection,Lthead[0],self.DateSelection.date().toPython(),self.TimeSelect.time().toPython(),
                          True,Agenda=SignatoriesList)    
        Path(os.path.join('..','Clients',self.currentselection,self.findfinyear(self.DateSelection.date()),datetime.datetime.strftime(datetime.datetime.strptime(self.DateSelection.date().toString(),'%a %b %d %Y').date(),'%d.%m.%Y'))).mkdir(parents=True, exist_ok=True)
        SignedByAuth = self.Signedby.currentText()
        self.conn = sqlite3.connect(self.dbfilepath)
        self.cur = self.conn.cursor()
        SignedByInfo = self.cur.execute(f'SELECT director_din, Designation,director_address from Signatories WHERE company_cin = "{self.CINNum}" AND director_name = "{SignedByAuth}"').fetchall()[0]
        Notice.NoticeSignatures(self.currentselection, SignedByAuth, SignedByInfo[1], SignedByInfo[0], SignedByInfo[2])
        Notice.saveDoc(os.path.join('..','Clients',self.currentselection,self.findfinyear(self.DateSelection.date()),datetime.datetime.strftime(self.DateSelection.date().toPython(),'%d.%m.%Y'),'BM_Notice_'+datetime.datetime.strftime(datetime.datetime.strptime(self.DateSelection.date().toString(),'%a %b %d %Y').date(),'%d_%m_%Y')))       
        self.Feedback('Success','Document Generated Successfully',"View Document")
    
    def Feedback(self,action,Message,link=None):
        self.FeedBackWin = QtWidgets.QWidget()
        pyside_dynamic.loadUi('../Resources/ui/feedback.ui',self.FeedBackWin)
        self.FeedBackWin.Message.setText(Message)
        if link:
            self.FeedBackWin.link.setText(link)
            self.FeedBackWin.link.clicked.connect(self.openDoc)
        if action=='Success':
            self.FeedBackWin.Icon.setPixmap(QtGui.QPixmap(QtGui.QImage("../Resources/Icon/tick.png")))
        if action=='Failed':
            self.FeedBackWin.Icon.setPixmap(QtGui.QPixmap(QtGui.QImage("../Resources/Icon/close.png")))
        if action=='Warning':
            self.FeedBackWin.Icon.setPixmap(QtGui.QPixmap(QtGui.QImage("../Resources/Icon/warning.png")))
        self.FeedBackWin.show()

    def openDoc(self):
        os.startfile('"'+os.path.abspath(os.path.join(Config['Home'],self.currentselection,self.findfinyear(self.DateSelection.date()),datetime.datetime.strftime(self.DateSelection.date().toPython(),'%d.%m.%Y'),'BM_Notice_'+datetime.datetime.strftime(datetime.datetime.strptime(self.DateSelection.date().toString(),'%a %b %d %Y').date(),'%d_%m_%Y')+'.docx'))+'"')

