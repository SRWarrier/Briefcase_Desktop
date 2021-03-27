from PySide2 import QtWidgets, QtUiTools,QtCore, QtGui
import sys
import os
from functions import pyside_dynamic
from functions.Gdrive import Gdrive
import sqlite3
from COMPANIES import AddCompany, deleteCompany, viewCompany, EditCompany
import pickle
import pandas as pd


class Ui(QtWidgets.QWidget):
    def __init__(self):
        super(Ui, self).__init__()
        pyside_dynamic.loadUi('Resources/ui/ClientManager.ui',self)
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
            clienttablepd = self.readSQL('SELECT company_cin,company_name,company_roc,company_date_of_incorporation,company_last_update from Masterdata',None)
            self.clienttablepd = clienttablepd.sort_values(by=["company_name"],ascending = True).reset_index(drop=True)
            CompanyList=[]
            for item in CompanyListdb:
                CompanyList.append((item[0],item[1]))
##            for company in CompanyList:
                #self.clientbar(company[0],company[1])
            CompanyList.sort(key=lambda x: x[0])
        except:
            clienttablepd = pd.DataFrame(columns = ['CIN','Company Name','Registrar','Date of Incorporation', 'Last Update'])
            pass
        #ClickMapping
        self.addCompany.clicked.connect(self.addCompanyFn)
        self.clienttablepd.columns = ['CIN','Company Name','Registrar','Date of Incorporation', 'Last Update']
        self.pandasmodel = DataFrameModel(self.clienttablepd)
        trows = len(self.clienttablepd)
        tcols = len(self.clienttablepd.T)
        self.filter_proxy_model = QtCore.QSortFilterProxyModel()
        self.filter_proxy_model.setSourceModel(self.pandasmodel)
        self.filter_proxy_model.setFilterCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.filter_proxy_model.setFilterKeyColumn(1)
        self.Companydisplay.setModel(self.filter_proxy_model)
        self.Companydisplay.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.Companydisplay.customContextMenuRequested.connect(self.handleHeaderMenu_client)
        self.Companydisplay.setColumnWidth(0,180)
        self.Companydisplay.setColumnWidth(1,550)
        self.Companydisplay.setColumnWidth(2,300)
        self.Companydisplay.setColumnWidth(3,150)
        self.Companydisplay.setColumnWidth(4,180)
        self.Companydisplay.verticalHeader().hide()
        self.Companydisplay.setStyleSheet("height: 10px;")
        selection = self.Companydisplay.selectionModel()
        selection.selectionChanged.connect(self.handleSelectionChanged)
        #SearchBar
        self.Searchbar = self.findChild(QtWidgets.QLineEdit, 'Searchbar')
        self.Searchbar.textChanged.connect(self.filter_proxy_model.setFilterRegExp)


    def handleSelectionChanged(self, selected, deselected):
        indexes = selected.indexes()
        if not len(indexes)>1:
            if indexes[0].column()==1:
                row = indexes[0].row()
                CIN = indexes[0].model().index(row, 0).data()
                sender =(self.sender())
                Home = getParent(sender,'HomePage')
                self.viewCompanyFn(CIN,Home)
            

    def handleHeaderMenu_client(self, pos):
        x,y = pos.x(), pos.y()
        it = self.Companydisplay.indexAt(pos)
        self.selectedrow = it.row()
        self.companyName = self.Companydisplay.model().index(self.selectedrow, 1).data()
        self.CIN = self.Companydisplay.model().index(self.selectedrow, 0).data()
        if it is None: return
        menu = QtWidgets.QMenu()
        edit = menu.addAction("Edit Company")
        delete = menu.addAction("Delete Company")
        action = menu.exec_(self.Companydisplay.viewport().mapToGlobal(pos))
        if action == delete:
            msgBox = QtWidgets.QMessageBox(self)
            msgBox.setIcon(QtWidgets.QMessageBox.Warning)
            msgBox.setText(f"Do you really want to delete {self.companyName}?")
            msgBox.setWindowTitle("Delete?")
            msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
            msgBox.buttonClicked.connect(self.decision)
            msgBox.show()
        elif action == edit:
            Home = getParent(self,'HomePage')
            self.editCompanyFn(self.CIN,Home)
            
            
    def readSQL(self,Query, Index):
        conn = sqlite3.connect(self.dbfilepath)
        cur = conn.cursor()
        table = pd.read_sql_query(Query,conn,index_col=Index)
        cur.close()
        conn.close()
        return table  

    def editCompanyFn(self,currentCIN,Home):
        sender =(self.sender())
        titleCard = Home.findChild(QtWidgets.QLabel,"WidgetTitleText")
        titleCard.setStyleSheet("background-color:  rgb(255,193,7); color: rgb(255,255,255)")
        titleCard.setText("Edit Company")
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

    def viewCompanyFn(self,currentCIN,Home):
        titleCard = Home.findChild(QtWidgets.QLabel,"WidgetTitleText")
        titleCard.setStyleSheet("background-color:  rgb(24, 44, 97); color: rgb(255,255,255)")
        titleCard.setText("View Company")
        Displaylayout = Home.findChild(QtWidgets.QWidget,"MainWindow").layout()
        clearLayout(Displaylayout)
        CurrentWidget = viewCompany.Ui(currentCIN)
        Displaylayout.addWidget(CurrentWidget, *(0,0))

    def deleteCompanyFn(self,currentCIN,Home,CompanyName):
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
            self.deleteCIN = self.CIN 
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
        else:
            pass

        
        
    def clientbar(self,companyName, companyCIN):
        clientBanner = QtWidgets.QWidget()
        pyside_dynamic.loadUi('Resources/ui/clientbar.ui',clientBanner)
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

class DataFrameModel(QtCore.QAbstractTableModel):
    DtypeRole = QtCore.Qt.UserRole + 1000
    ValueRole = QtCore.Qt.UserRole + 1001

    def __init__(self, df=pd.DataFrame(), parent=None):
        super(DataFrameModel, self).__init__(parent)
        self._dataframe = df

    def setDataFrame(self, dataframe):
        self.beginResetModel()
        self._dataframe = dataframe.copy()
        self.endResetModel()

    def dataFrame(self):
        return self._dataframe

    dataFrame = QtCore.Property(pd.DataFrame, fget=dataFrame, fset=setDataFrame)

    @QtCore.Slot(int, QtCore.Qt.Orientation, result=str)

    def headerData(self, section: int, orientation: QtCore.Qt.Orientation, role: int = QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return self._dataframe.columns[section]
            else:
                return str(self._dataframe.index[section])
        return None

    def rowCount(self, parent=QtCore.QModelIndex()):
        if parent.isValid():
            return 0
        return len(self._dataframe.index)

    def columnCount(self, parent=QtCore.QModelIndex()):
        if parent.isValid():
            return 0
        return self._dataframe.columns.size

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if not index.isValid() or not (0 <= index.row() < self.rowCount() \
            and 0 <= index.column() < self.columnCount()):
            return None
        row = self._dataframe.index[index.row()]
        col = self._dataframe.columns[index.column()]
        dt = self._dataframe[col].dtype

        val = self._dataframe.iloc[row][col]
        if role == QtCore.Qt.DisplayRole:
            return str(val)
        elif role == DataFrameModel.ValueRole:
            return val
        if role == DataFrameModel.DtypeRole:
            return dt
        return None

    def roleNames(self):
        roles = {
            QtCore.Qt.DisplayRole: b'display',
            DataFrameModel.DtypeRole: b'dtype',
            DataFrameModel.ValueRole: b'value'
        }
        return roles
        
