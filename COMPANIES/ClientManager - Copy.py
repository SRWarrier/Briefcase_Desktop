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
        Home = sender.parent().parent().parent().parent().parent().parent().parent()
        titleCard = Home.findChild(QtWidgets.QLabel,"WidgetTitleText")
        titleCard.setStyleSheet("background-color:  rgb(255,193,7); color: rgb(255,255,255)")
        titleCard.setText("Edit Company")
        currentCIN = sender.parent().findChild(QtWidgets.QLabel,'CompanyCIN').text()
        Displaylayout = sender.parent().parent().parent().parent().parent().parent().layout()
        clearLayout(Displaylayout)
        CurrentWidget = EditCompany.Ui(currentCIN)
        Displaylayout.addWidget(CurrentWidget, *(0,0))
    

    def addCompanyFn(self):
        sender =(self.sender())
        Home = sender.parent().parent().parent().parent()
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
        Home = sender.parent().parent().parent().parent().parent().parent().parent()
        titleCard = Home.findChild(QtWidgets.QLabel,"WidgetTitleText")
        titleCard.setStyleSheet("background-color:  rgb(24, 44, 97); color: rgb(255,255,255)")
        titleCard.setText("View Company")
        currentCIN = sender.parent().findChild(QtWidgets.QLabel,'CompanyCIN').text()
        Displaylayout = sender.parent().parent().parent().parent().parent().parent().layout()
        clearLayout(Displaylayout)
        CurrentWidget = viewCompany.Ui(currentCIN)
        Displaylayout.addWidget(CurrentWidget, *(0,0))

    def deleteCompanyFn(self):
        sender =(self.sender())
        self.deleteCIN = sender.parent().findChild(QtWidgets.QLabel,'CompanyCIN').text()
        CompanyName = sender.parent().findChild(QtWidgets.QLabel,'CompanyName').text()
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
        CompanyName = QtWidgets.QLabel(clientBanner)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(CompanyName.sizePolicy().hasHeightForWidth())
        CompanyName.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        font.setPointSize(10)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        CompanyName.setFont(font)
        CompanyName.setAlignment(QtCore.Qt.AlignCenter)
        CompanyName.setText(companyName)
        CompanyName.setObjectName('CompanyName')
        CompanyName.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
        hLayout.addWidget(CompanyName)
        CompanyCIN = QtWidgets.QLabel(clientBanner)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(CompanyCIN.sizePolicy().hasHeightForWidth())
        CompanyCIN.setSizePolicy(sizePolicy)
        CompanyCIN.setMaximumSize(QtCore.QSize(180, 16777215))
        font = QtGui.QFont()
        font.setFamily("Open Sans")
        font.setPointSize(10)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        CompanyCIN.setFont(font)
        CompanyCIN.setObjectName('CompanyCIN')
        CompanyCIN.setAlignment(QtCore.Qt.AlignCenter)
        CompanyCIN.setText(companyCIN)
        CompanyCIN.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
        hLayout.addWidget(CompanyCIN)
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
        ViewButton.clicked.connect(self.viewCompanyFn)
        hLayout.addWidget(ViewButton)
        if self.canDelete:
            #EDIT
            EditButton = QtWidgets.QPushButton(clientBanner)
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(EditButton.sizePolicy().hasHeightForWidth())
            EditButton.setSizePolicy(sizePolicy)
            EditButton.setMaximumSize(QtCore.QSize(120, 16777215))
            font = QtGui.QFont()
            font.setFamily("Open Sans")
            font.setPointSize(10)
            font.setStyleStrategy(QtGui.QFont.PreferAntialias)
            EditButton.setFont(font)
            EditButton.setStyleSheet("background-color: rgb(255, 255, 127);")
            EditButton.setText("Edit")
            EditButton.clicked.connect(self.editCompanyFn)
            hLayout.addWidget(EditButton)
            #DELETE
            DeleteButton = QtWidgets.QPushButton(clientBanner)
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(DeleteButton.sizePolicy().hasHeightForWidth())
            DeleteButton.setSizePolicy(sizePolicy)
            DeleteButton.setMaximumSize(QtCore.QSize(120, 16777215))
            font = QtGui.QFont()
            font.setFamily("Open Sans")
            font.setPointSize(10)
            font.setStyleStrategy(QtGui.QFont.PreferAntialias)
            DeleteButton.setFont(font)
            DeleteButton.setStyleSheet("background-color: rgb(255, 0, 0);")
            DeleteButton.setText("Delete")
            hLayout.addWidget(DeleteButton)
            DeleteButton.clicked.connect(self.deleteCompanyFn)
        self.clientBoard.addWidget(clientBanner)
        
        

def clearLayout(layout):
    while layout.count():
        child = layout.takeAt(0)
        if child.widget() is not None:
            child.widget().deleteLater()
        elif child.layout() is not None:
            clearLayout(child.layout())
