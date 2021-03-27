from PySide2 import QtWidgets, QtUiTools,QtCore, QtGui
import sys
import HomePage
import os
from functions import Database_Manager as db
from functions import pyside_dynamic
from COMPANIES import viewCompany
#from functions.Gdrive import Gdrive
import webbrowser
import pickle
import sqlite3
import datetime

class Ui(QtWidgets.QWidget):
    def __init__(self, CIN, Committee = None):
        super(Ui, self).__init__()
        pyside_dynamic.loadUi('Resources/ui/AddCommittee.ui',self)
        with open('Config','rb') as f:
            self.Config = pickle.loads(f.read())
            f.close()
        self.CIN = CIN
        self.Committee = Committee
        self.committeFilePath = os.path.join(self.Config['Database'],'committees.db')
        self.policy = ''
        self.membersTable.setColumnWidth(0, 60)
        self.membersTable.setColumnWidth(1, 300)
        self.membersTable.setColumnWidth(2, 200)
        self.addMember.clicked.connect(self.addOneRow)
        self.membersTable.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.membersTable.customContextMenuRequested.connect(self.contextMenu)
        self.saveCommittee.clicked.connect(self.Save)
        self.backButton.clicked.connect(self.backtoCommittee)
        self.creationDate.setDateTime(QtCore.QDateTime.currentDateTime())
        if Committee:
            self.fillCommittee(Committee)


    def fillCommittee(self,Committee):
        self.conn = sqlite3.connect(self.committeFilePath)
        self.cur = self.conn.cursor()
        self.CommInfo = self.cur.execute(f'SELECT * from committee WHERE company_cin = "{self.CIN}" AND committee_name = "{Committee}"').fetchall()[0]
        self.CommMemInfo = self.cur.execute(f'SELECT * from CommitteeMembers WHERE company_cin = "{self.CIN}" AND committee_name = "{Committee}"').fetchall()
        if self.CommInfo:
            self.committeeName.setText(self.CommInfo[1])
            self.creationDate.setDateTime(datetime.datetime.strptime(self.CommInfo[4],'%d-%m-%Y'))
            self.description.setText(self.CommInfo[2])
            self.applicableSection.setText(self.CommInfo[3])
        if self.CommMemInfo:
            self.membersTable.setRowCount(len(self.CommMemInfo))
            for ROW in range(len(self.CommMemInfo)):
                Data = self.CommMemInfo[ROW][2:]
                for COL in range(self.membersTable.columnCount()):
                    item = QtWidgets.QTableWidgetItem()
                    self.membersTable.setItem(ROW, COL, item)
                    item.setText(str(Data[COL]))
            
            
        
        
    def backtoCommittee(self):
        sender = self.sender()
        parent = getParent(sender,'HomePage')
        titleCard = parent.findChild(QtWidgets.QLabel,"WidgetTitleText")
        titleCard.setStyleSheet("background-color:  rgb(24, 44, 97); color: rgb(255,255,255)")
        titleCard.setText("View Company")
        layout = parent.findChild(QtWidgets.QWidget, 'MainWindow').layout()
        clearLayout(layout)
        CurrentWidget = viewCompany.Ui(self.CIN)
        layout.addWidget(CurrentWidget, *(0,0))

    def addOneRow(self):
        self.membersTable.insertRow(self.membersTable.rowCount())
        comboBox = QtWidgets.QComboBox()
        comboBox.addItems(['Mr.','Ms.','Dr.','Shri.','Smt.'])
        self.membersTable.setCellWidget(self.membersTable.rowCount()-1, 0, comboBox)
        
        
    def contextMenu(self, pos):
        x,y = pos.x(), pos.y()
        it = self.membersTable.indexAt(pos)
        selectedrow = it.row()
        if it is None: return
        menu = QtWidgets.QMenu()
        delete = menu.addAction("Delete Member")
        action = menu.exec_(self.membersTable.viewport().mapToGlobal(pos))
        if action == delete:
            self.membersTable.removeRow(selectedrow)

    def getMembers(self):
        comboBox = QtWidgets.QComboBox()
        comboBox.addItems(['Mr.','Ms.','Dr.','Shri.','Smt.'])
        self.membersTable.setCellWidget(x, 0, comboBox)

    def Save(self):
        conn = sqlite3.connect(self.committeFilePath)
        cur = conn.cursor()
        try:
            cur.execute(f'DELETE FROM committee WHERE company_cin = {repr(self.CIN)} AND committee_name = "{self.Committee}"')
            cur.execute(f'DELETE FROM CommitteeMembers WHERE company_cin = {repr(self.CIN)} AND committee_name = "{self.Committee}" ')
            cur.close()
            conn.commit()
            conn.close()  
        except sqlite3.OperationalError:
            pass
        CommitteName = self.committeeName.text()
        CreationDate = self.creationDate.date().toPython().strftime('%d-%m-%Y')
        Description = self.description.text()
        Section = self.applicableSection.text()
        DbData = [self.CIN,CommitteName,Description,Section,CreationDate,self.policy]
        DBMemData = []
        for ROW in range(self.membersTable.rowCount()):
            tempList = [self.CIN,CommitteName]
            for COL in range(self.membersTable.columnCount()):
                try:
                    tempList.append(self.membersTable.cellWidget(ROW,COL).currentText())
                except:
                    tempList.append(self.membersTable.item(ROW,COL).text())
            DBMemData.append(tuple(tempList))
        
        db.Committeedb(DbData)
        db.CommitteeMembers(DBMemData)           
        QtWidgets.QMessageBox.information(self,'Success','Committee has been created')
        self.backtoCommittee()

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
