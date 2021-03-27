from PySide2 import QtWidgets, QtUiTools,QtCore, QtGui
import sys
import os
from functions import pyside_dynamic
from functions.Gdrive import Gdrive
import sqlite3
from COMPANIES import AddCompany, deleteCompany, viewCompany, EditCompany
import pickle


class Ui(QtWidgets.QWidget):
    def __init__(self):
        super(Ui, self).__init__()
        pyside_dynamic.loadUi('../Resources/ui/ClientManager.ui',self)
        with open('Config','rb') as f:
            Config = pickle.loads(f.read())
            f.close()
        self.dbfilepath = os.path.join(Config['Database'],'C3_DataBase.db')
        self.conn = sqlite3.connect(self.dbfilepath)
        self.cur = self.conn.cursor()
        #UserTracking
        with open('_temp/_currentuser','rb') as currentUser:
            self.Userdata = pickle.loads(currentUser.read())
            currentUser.close()
        self.canDelete = True 
        if self.Userdata['Role']!='Administrator':
            self.canDelete = False
            self.addCompany.setParent(None)
        try:
            CompanyListdb = self.cur.execute('SELECT "company_name", "company_cin" from Masterdata').fetchall()
            CompanyList=[]
            for item in CompanyListdb:
                CompanyList.append((item[0],item[1]))
            for company in CompanyList:
                self.clientbar(company[0],company[1])
            CompanyList.sort(key=lambda x: x[0])
        except:
            pass
        #ClickMapping
        self.addCompany.clicked.connect(self.addCompanyFn)
        self.SearchButton.clicked.connect(self.Search)
        

        

    def editCompanyFn(self):
        sender =(self.sender())
        Home = getParent(sender,'HomePage')
        titleCard = Home.findChild(QtWidgets.QLabel,"WidgetTitleText")
        titleCard.setStyleSheet("background-color:  rgb(255,193,7); color: rgb(255,255,255)")
        titleCard.setText("Edit Company")
        currentCIN = sender.parent().parent().findChild(QtWidgets.QLabel,'CIN').text()
        Displaylayout = Home.findChild(QtWidgets.QWidget,"MainWindow").layout()
        clearLayout(Displaylayout)
        CurrentWidget = EditCompany.Ui(currentCIN)
        Displaylayout.addWidget(CurrentWidget, *(0,0))
    

    def addCompanyFn(self):
        sender =(self.sender())
        Home = getParent(sender,'HomePage')
        Displaylayout = Home.findChild(QtWidgets.QWidget,"MainWindow").layout()
        titleCard = Home.findChild(QtWidgets.QLabel,"WidgetTitleText")
        titleCard.setStyleSheet("background-color: rgb(0,230,45); color: rgb(255,255,255)")
        titleCard.setText("Add Company")
        clearLayout(Displaylayout)
        CurrentWidget = AddCompany.Ui()
        Displaylayout.addWidget(CurrentWidget, *(0,0))

    def Search(self):
        pass

    def viewCompanyFn(self):
        sender =(self.sender())
        Home = getParent(sender,'HomePage')
        print(Home)
        titleCard = Home.findChild(QtWidgets.QLabel,"WidgetTitleText")
        titleCard.setStyleSheet("background-color:  rgb(24, 44, 97); color: rgb(255,255,255)")
        titleCard.setText("View Company")
        currentCIN = sender.parent().findChild(QtWidgets.QLabel,'CIN').text()
        Displaylayout = Home.findChild(QtWidgets.QWidget,"MainWindow").layout()
        clearLayout(Displaylayout)
        CurrentWidget = viewCompany.Ui(currentCIN)
        Displaylayout.addWidget(CurrentWidget, *(0,0))

    def deleteCompanyFn(self):
        sender =(self.sender())
        self.deleteCIN = sender.parent().findChild(QtWidgets.QLabel,'CIN').text()
        CompanyName = sender.parent().parent().findChild(QtWidgets.QLabel,'companyName').text()
        self.ParentCard = sender.parent()
        msgBox = QtWidgets.QMessageBox(self)
        msgBox.setStyleSheet("background-color:  rgb(253, 253, 253);")
        msgBox.setIcon(QtWidgets.QMessageBox.Warning)
        msgBox.setText(f"Do you really want to delete {CompanyName}?")
        msgBox.setWindowTitle("Delete?")
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
        msgBox.buttonClicked.connect(self.decision)
        msgBox.show()
        
    def decision(self,button):
        if button.text()=='OK':
            conn = sqlite3.connect(self.dbfilepath)
            cur = conn.cursor()
            cur.execute(f'DELETE FROM Masterdata WHERE company_cin = {repr(self.deleteCIN)}')
            cur.execute(f'DELETE FROM Signatories WHERE company_cin = {repr(self.deleteCIN)}')
            cur.execute(f'DELETE FROM HoldingCompanies WHERE company_cin = {repr(self.deleteCIN)}')
            cur.execute(f'DELETE FROM SubsidiaryCompanies WHERE company_cin = {repr(self.deleteCIN)}')
            cur.execute(f'DELETE FROM AssociateCompanies WHERE company_cin = {repr(self.deleteCIN)}')
            cur.execute(f'DELETE FROM documents WHERE company_cin = {repr(self.deleteCIN)}')
            cur.execute(f'DELETE FROM Shareholders WHERE company_cin = {repr(self.deleteCIN)}')
            cur.execute(f'DELETE FROM Contacts WHERE company_cin = {repr(self.deleteCIN)}')
            cur.close()
            conn.commit()
            conn.close()
            self.ParentCard.setParent(None)
        else:
            pass

        
        
    def clientbar(self,companyName, companyCIN):
        clientBanner = QtWidgets.QWidget()
        pyside_dynamic.loadUi('../Resources/ui/clientbar.ui',clientBanner)
        clientBanner.companyName.setText(companyName.upper())
        clientBanner.companyName.clicked.connect(self.viewCompanyFn)
        clientBanner.CIN.setText(companyCIN)
        clientBanner.buttons.setEnabled(False)
        if self.canDelete:
            clientBanner.buttons.setEnabled(True)
            clientBanner.editButton.clicked.connect(self.editCompanyFn)
            clientBanner.deleteButton.clicked.connect(self.deleteCompanyFn)
        self.clientBoard.addWidget(clientBanner)
    
        

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
