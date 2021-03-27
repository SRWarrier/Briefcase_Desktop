from PySide2 import QtWidgets, QtUiTools,QtCore, QtGui
import sys
import HomePage
import os
from functions import Database_Manager as db
from functions import pyside_dynamic
#from functions.Gdrive import Gdrive
import requests_html
import sqlite3


session = requests_html.HTMLSession()

class Ui(QtWidgets.QWidget):
    def __init__(self):
        super(Ui, self).__init__()
        pyside_dynamic.loadUi('Resources/ui/EditcontactPerson.ui',self)
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
        self.contactDisplay = self.findChild(QtWidgets.QTableWidget, 'Display')
        self.contactDisplay.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.contactDisplay.customContextMenuRequested.connect(self.handleHeaderMenu_client)
        self.SaveButton = self.findChild(QtWidgets.QPushButton, 'Save')
        self.SaveButton.clicked.connect(self.SavContacts)
        self.AddButton = self.findChild(QtWidgets.QPushButton, 'AddPerson')
        self.AddButton.clicked.connect(self.addrow)
        self.show()


    def fillTable(self):
        self.currentselection = self.Nameentry.currentText()
        self.CINNum = self.cur.execute(f'SELECT company_cin from Masterdata WHERE company_name = "{self.currentselection}"').fetchall()[0][0]
        ContactList = self.cur.execute(f'SELECT * from Contacts WHERE company_cin = {repr(self.CINNum)}').fetchall()
        if len(ContactList)==0:
            self.contactDisplay.setRowCount(0)
            self.contactDisplay.insertRow(0)
            
        else:
            self.contactDisplay.setRowCount(len(ContactList))
            for x in range(len(ContactList)):
                for y in range(len(ContactList[x])):
                    if not y+1==len(ContactList[x]):
                        item = QtWidgets.QTableWidgetItem()
                        self.contactDisplay.setItem(x, y, item)
                        item.setText(str(ContactList[x][y+1]))
                        self.contactDisplay.resizeRowsToContents()
                    
    def SavContacts(self):
        ContactsList=[]
        for x in range(self.contactDisplay.rowCount()):
                m=[]
                m.append(self.CINNum)
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

    def addrow(self):
        rowPosition = self.contactDisplay.rowCount()
        self.contactDisplay.insertRow(rowPosition)

    def handleHeaderMenu_client(self, pos):
        x,y = pos.x(), pos.y()
        it = self.contactDisplay.indexAt(pos)
        row = it.row()
        data = self.contactDisplay.model().index(row, 0).data()
        if it is None: return
        menu = QtWidgets.QMenu()
        edit = menu.addAction("Delete Contact")
        action = menu.exec_(self.contactDisplay.viewport().mapToGlobal(pos))
        if action == edit:
            self.contactDisplay.removeRow(row)
            
    def done(self):
        self.close()
        
