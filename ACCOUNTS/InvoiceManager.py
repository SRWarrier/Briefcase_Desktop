from PySide2 import QtWidgets, QtUiTools,QtCore, QtGui
import sys
import os
from functions import pyside_dynamic
#from functions.Gdrive import Gdrive
from functions import Database_Manager as db
import sqlite3
from ACCOUNTS import AddInvoice
import pickle
import pandas as pd


class Ui(QtWidgets.QWidget):
    def __init__(self):
        super(Ui, self).__init__()
        pyside_dynamic.loadUi('Resources/ui/InvoiceManager.ui',self)
        with open('Config','rb') as f:
            Config = pickle.loads(f.read())
            f.close()
        self.dbfilepath = os.path.join(Config['Database'],'C3_DataBase.db')
        self.conn = sqlite3.connect(self.dbfilepath)
        self.cur = self.conn.cursor()
        #UserTracking
        try:
            CompanyListdb = self.cur.execute('SELECT "BILLNO","CLIENT","AMOUNT","TYPE" from Bills').fetchall()
            Invoicedisplay = self.readSQL('SELECT "BILLNO","CLIENT","AMOUNT","TYPE" from Bills',None)
            self.Invoicedisplay = Invoicedisplay.sort_values(by=["ClientName"],ascending = True).reset_index(drop=True)
            CompanyList=[]
            for item in CompanyListdb:
                CompanyList.append((item[0],item[1]))
##            for company in CompanyList:
                #self.clientbar(company[0],company[1])
            CompanyList.sort(key=lambda x: x[0])
        except:
            Invoicedisplay = pd.DataFrame(columns = ["BILLNO","CLIENT","AMOUNT","TYPE"])
            pass
        #ClickMapping
        self.addInvoice.clicked.connect(self.addInvoiceFn)
        self.Invoicedisplay.columns = ["BILLNO","CLIENT","AMOUNT","TYPE"]
        self.pandasmodel = DataFrameModel(self.Invoicedisplay)
        try:
            trows = len(self.Invoicedisplay)
            tcols = len(self.Invoicedisplay.T)
        except:
            trows = 0
            tcols = 4
        self.meetingProxy = QtCore.QSortFilterProxyModel()
        self.meetingProxy.setSourceModel(self.pandasmodel)
        self.meetingProxy.setFilterCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.meetingProxy.setFilterKeyColumn(2)
        self.Invoicedisplay.setModel(self.meetingProxy)
        self.Invoicedisplay.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.Invoicedisplay.customContextMenuRequested.connect(self.handleHeaderMenu_client)
        self.Invoicedisplay.setColumnWidth(0,300)
        self.Invoicedisplay.setColumnWidth(0,300)
        self.Invoicedisplay.setColumnWidth(1,300)
        self.Invoicedisplay.setColumnWidth(2,200)
        self.Invoicedisplay.verticalHeader().hide()
        self.Invoicedisplay.setStyleSheet("height: 10px;")
        selection = self.Invoicedisplay.selectionModel()
        #selection.selectionChanged.connect(self.handleSelectionChanged)
        #SearchBar
        self.Searchbar = self.findChild(QtWidgets.QLineEdit, 'Searchbar')
        self.Searchbar.textChanged.connect(self.search)

    def search(self):
        self.filter_proxy_model = QtCore.QSortFilterProxyModel()
        self.filter_proxy_model.setSourceModel(self.pandasmodel)
        self.filter_proxy_model.setFilterCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.filter_proxy_model.setFilterKeyColumn(0)
        self.filter_proxy_model.setFilterRegExp(self.Searchbar.text())
        self.Invoicedisplay.setModel(self.filter_proxy_model)
        
            

    def handleHeaderMenu_client(self, pos):
        x,y = pos.x(), pos.y()
        it = self.Invoicedisplay.indexAt(pos)
        self.selectedrow = it.row()
        self.InvoiceNumber = self.Invoicedisplay.model().index(self.selectedrow, 0).data()
        ClientName = self.Invoicedisplay.model().index(self.selectedrow, 1).data()
        self.CIN = self.Invoicedisplay.model().index(self.selectedrow, 0).data()
        if it is None: return
        menu = QtWidgets.QMenu()
        edit = menu.addAction("Edit Invoice")
        delete = menu.addAction("Delete Invoice")
        action = menu.exec_(self.Invoicedisplay.viewport().mapToGlobal(pos))
        if action == delete:
            msgBox = QtWidgets.QMessageBox(self)
            msgBox.setIcon(QtWidgets.QMessageBox.Warning)
            msgBox.setText(f"Do you really want to delete {self.InvoiceNumber}?")
            msgBox.setWindowTitle("Delete?")
            msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
            msgBox.buttonClicked.connect(self.decision)
            msgBox.show()
        elif action == edit:
           pass
            
            
    def readSQL(self,Query, Index):
        conn = sqlite3.connect(self.dbfilepath)
        cur = conn.cursor()
        table = pd.read_sql_query(Query,conn,index_col=Index)
        cur.close()
        conn.close()
        return table  

    

    def addInvoiceFn(self):
        sender =(self.sender())
        Home = getParent(sender,'HomePage')
        Displaylayout = Home.findChild(QtWidgets.QWidget,"MainWindow").layout()
        titleCard = Home.findChild(QtWidgets.QLabel,"WidgetTitleText")
        titleCard.setStyleSheet("background-color: rgb(0,230,45); color: rgb(255,255,255)")
        titleCard.setText("Add Invoice")
        clearLayout(Displaylayout)
        CurrentWidget = AddInvoice.Ui()
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

    def deleteCompanyFn(self,currentCIN,Home,InvoiceNumber):
        msgBox = QtWidgets.QMessageBox(self)
        msgBox.setStyleSheet("background-color:  rgb(253, 253, 253);")
        msgBox.setIcon(QtWidgets.QMessageBox.Warning)
        msgBox.setText(f"Do you really want to delete {InvoiceNumber}?")
        msgBox.setWindowTitle("Delete?")
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
        msgBox.buttonClicked.connect(self.decision)
        msgBox.show()
        
    def decision(self,button):
        if button.text()=='OK':
            conn = sqlite3.connect(self.dbfilepath)
            cur = conn.cursor()
            cur.execute(f'DELETE FROM Resolutions WHERE ID = {repr(self.CIN)}')
            conn.commit()
            conn.close()
            self.Invoicedisplay.reset()
            print(self.Invoicedisplay)
            index = self.Invoicedisplay.loc[self.Invoicedisplay['ID']==int(self.CIN)].index[0]
            self.Invoicedisplay = self.Invoicedisplay.drop(index)
            self.pandasmodel = DataFrameModel(self.Invoicedisplay)
            self.meetingProxy.setSourceModel(self.pandasmodel)
            self.filter_proxy_model.setSourceModel(self.meetingProxy)
            self.Invoicedisplay.setModel(self.filter_proxy_model)
        else:
            pass

        
        
    def clientbar(self,InvoiceNumber, companyCIN):
        clientBanner = QtWidgets.QWidget()
        pyside_dynamic.loadUi('Resources/ui/clientbar.ui',clientBanner)
        clientBanner.InvoiceNumber.setText(InvoiceNumber.upper())
        clientBanner.InvoiceNumber.clicked.connect(self.viewCompanyFn)
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
        
