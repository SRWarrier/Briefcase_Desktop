from PySide2 import QtWidgets, QtUiTools,QtCore, QtGui
import sys
import HomePage
import os
from functions import pyside_dynamic
#from functions.Gdrive import Gdrive
import requests_html
import sqlite3
import pandas as pd


session = requests_html.HTMLSession()

class Ui(QtWidgets.QWidget):
    def __init__(self):
        super(Ui, self).__init__()
        pyside_dynamic.loadUi('Resources/ui/DeleteCompany.ui',self)
        with open('Config','rb') as f:
            Config = pickle.loads(f.read())
            f.close()
        self.dbfilepath = os.path.join(Config['Database'],'C3_DataBase.db')

        #ClientTable
        self.Clinettable = self.findChild(QtWidgets.QTableView, 'Companydisplay')
        self.done = self.findChild(QtWidgets.QPushButton, 'savebutton')
        self.done.clicked.connect(self.closeself)
        try:
            clienttablepd = self.readSQL('SELECT company_cin,company_name,company_roc,company_date_of_incorporation,company_last_update from Masterdata',None)
            self.clienttablepd = clienttablepd.sort_values(by=["company_name"],ascending = True).reset_index(drop=True)
        except:
            clienttablepd = pd.DataFrame(columns = ['CIN','Company Name','Registrar','Date of Incorporation', 'Last Update'])
        self.clienttablepd.columns = ['CIN','Company Name','Registrar','Date of Incorporation', 'Last Update']
        self.pandasmodel = DataFrameModel(self.clienttablepd)
        trows = len(self.clienttablepd)
        tcols = len(self.clienttablepd.T)
        self.filter_proxy_model = QtCore.QSortFilterProxyModel()
        self.filter_proxy_model.setSourceModel(self.pandasmodel)
        self.filter_proxy_model.setFilterCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.filter_proxy_model.setFilterKeyColumn(1)
        self.Clinettable.setModel(self.filter_proxy_model)
        self.Clinettable.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.Clinettable.customContextMenuRequested.connect(self.handleHeaderMenu_client)
        self.Clinettable.resizeColumnsToContents()
        #SearchBar
        self.Searchbar = self.findChild(QtWidgets.QLineEdit, 'Searchbar')
        self.Searchbar.textChanged.connect(self.filter_proxy_model.setFilterRegExp)
        self.show()
        
        

    def readSQL(self,Query, Index):
        conn = sqlite3.connect(self.dbfilepath)
        cur = conn.cursor()
        table = pd.read_sql_query(Query,conn,index_col=Index)
        cur.close()
        conn.close()
        return table


    def handleHeaderMenu_client(self, pos):
        x,y = pos.x(), pos.y()
        it = self.Clinettable.indexAt(pos)
        self.selectedrow = it.row()
        self.companyName = self.Clinettable.model().index(self.selectedrow, 1).data()
        self.CIN = self.Clinettable.model().index(self.selectedrow, 0).data()
        if it is None: return
        menu = QtWidgets.QMenu()
        edit = menu.addAction("Delete Company")
        action = menu.exec_(self.Clinettable.viewport().mapToGlobal(pos))
        if action == edit:
            msgBox = QtWidgets.QMessageBox(self)
            msgBox.setIcon(QtWidgets.QMessageBox.Warning)
            msgBox.setText(f"Do you really want to delete {self.companyName}?")
            msgBox.setWindowTitle("Delete?")
            msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
            msgBox.buttonClicked.connect(self.decision)
            msgBox.show()
            

    def decision(self,button):
        if button.text()=='OK':
            conn = sqlite3.connect(self.dbfilepath)
            cur = conn.cursor()
            cur.execute(f'DELETE FROM Masterdata WHERE company_cin = {repr(self.CIN)}')
            cur.execute(f'DELETE FROM Signatories WHERE company_cin = {repr(self.CIN)}')
            cur.execute(f'DELETE FROM Contacts WHERE company_cin = {repr(self.CIN)}')
            cur.close()
            conn.commit()
            conn.close()
            self.Clinettable.reset()
            index = self.clienttablepd.loc[self.clienttablepd['CIN']==self.CIN].index[0]
            self.clienttablepd = self.clienttablepd.drop(index)
            self.pandasmodel = DataFrameModel(self.clienttablepd)
            self.filter_proxy_model.setSourceModel(self.pandasmodel)
            self.Clinettable.setModel(self.filter_proxy_model)
            
        else:
            pass
            
            

            
    def closeself(self):
        self.close()


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
        
