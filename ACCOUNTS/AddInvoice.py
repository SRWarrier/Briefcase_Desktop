from PySide2 import QtWidgets, QtUiTools,QtCore, QtGui
import sys
import HomePage
import os
import numpy as np
from functions import Database_Manager as db
from functions import pyside_dynamic
import sqlite3
import datetime
from functions.generateDocuments import Bills
import webbrowser
import pickle



class Ui(QtWidgets.QWidget):
    def __init__(self):
        super(Ui, self).__init__()
        pyside_dynamic.loadUi('Resources/ui/AddInvoice.ui',self)
        with open('Config','rb') as f:
            Config = pickle.loads(f.read())
            f.close()
        self.dbfilepath = os.path.join(Config['Database'],'C3_DataBase.db')
        self.DirectorContainer = []
        self.DINList = {}
        self.conn = sqlite3.connect(self.dbfilepath)
        self.cur = self.conn.cursor()
        CompanyListdb = self.cur.execute('SELECT "company_name" from Masterdata').fetchall()
        CompanyList=['']
        for item in CompanyListdb:
            CompanyList.append(item[0])
        self.CompanySelect.addItems(CompanyList)
        self.CompanySelect.activated.connect(self.getCompanyDetails)
        self.Date.setDateTime(QtCore.QDateTime.currentDateTime())
        self.BillTable.setColumnWidth(0, 720)
        self.BillTable.setColumnWidth(1, 250)
        self.BillTable.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.BillTable.customContextMenuRequested.connect(self.handleHeaderMenu_client)
        self.BillTable.setWordWrap(True)
        self.BillTable.cellChanged.connect(self.summ)
        self.NoOfItems.valueChanged.connect(self.expandItems)
        self.GST.editingFinished.connect(self.getStateCode)
        self.StateCode.valueChanged.connect(self.CalcGST)
        try:
            self.BasicInfo = self.cur.execute('SELECT * from basicInfo').fetchall()[0]
            self.fillBasic()
        #self.show()
        except:
            QtWidgets.QMessageBox.critical(self, "Basic Data Missing", "Basic information required for invoice is missing. Request Admin to fill in Basic data to proceed.")
        self.savebutton.clicked.connect(self.GenerateBill)

    def getCompanyDetails(self):
        self.CompanySelection = self.CompanySelect.currentText()
        self.CompanyData = self.cur.execute(f'SELECT * from Masterdata WHERE "company_name" = "{self.CompanySelection}"').fetchall()[0]
        self.CompanyRegOffice = self.CompanyData[10]
        self.Address.setText(self.CompanyRegOffice )
        self.generateHistory()
        

    def fillBasic(self):
        item = QtWidgets.QTableWidgetItem()
        self.PANGST.setItem(0, 0, item)
        item.setText(self.BasicInfo[2])
        item = QtWidgets.QTableWidgetItem()
        self.PANGST.setItem(1, 0, item)
        item.setText(self.BasicInfo[3])
        item = QtWidgets.QTableWidgetItem()
        self.BankDetails.setItem(0, 0, item)
        item.setText(self.BasicInfo[0])
        item = QtWidgets.QTableWidgetItem()
        self.BankDetails.setItem(1, 0, item)
        item.setText(self.BasicInfo[6])
        #
        item = QtWidgets.QTableWidgetItem()
        self.BankDetails.setItem(2, 0, item)
        item.setText(self.BasicInfo[7])
        item = QtWidgets.QTableWidgetItem()
        self.BankDetails.setItem(3, 0, item)
        item.setText(self.BasicInfo[8])
        item = QtWidgets.QTableWidgetItem()
        self.BankDetails.setItem(4, 0, item)
        item.setText(self.BasicInfo[4])
        item = QtWidgets.QTableWidgetItem()
        self.BankDetails.setItem(5, 0, item)
        item.setText(self.BasicInfo[5])
        
        
    def expandItems(self):
        self.BillTable.setRowCount(0)
        if self.BillTable.rowCount()<int(self.NoOfItems.value()+3):
            self.RowChange = False
            self.previousRowCount = self.BillTable.rowCount()
##            previousCount = (int(self.NoOfItems.value()))-((int(self.NoOfItems.value())+3)-self.BillTable.rowCount()-3)
##            print(previousCount)
            if self.BillTable.rowCount()>=4:
                subtotal = self.BillTable.item(self.BillTable.rowCount()-3, 2).text()
                GST = self.BillTable.item(self.BillTable.rowCount()-2, 2).text()
                Total = self.BillTable.item(self.BillTable.rowCount()-1, 2).text()
            else:
                subtotal = str(0)
                GST = str(0)
                Total = str(0)
            self.BillTable.setRowCount(int(self.NoOfItems.value())+3)
            summation=0
            item = QtWidgets.QTableWidgetItem()
            self.BillTable.setItem(self.previousRowCount-3, 0, item)
            item.setText('')
            item = QtWidgets.QTableWidgetItem()
            self.BillTable.setItem(self.previousRowCount-3, 1, item)
            item.setText('"00440100"/"998399"')
            item = QtWidgets.QTableWidgetItem()
            self.BillTable.setItem(self.previousRowCount-3, 2, item)
            item.setText('0')
            for row in range(self.BillTable.rowCount()):
                item = QtWidgets.QTableWidgetItem()
                self.BillTable.setItem(row, 1, item)
                if row<self.BillTable.rowCount()-2:
                    item.setText('"00440100"/"998399"')
                try:
                    summation = summation+float(self.BillTable.item(row,2).text())
                except:
                    summation = summation+0
                if row>self.previousRowCount-3:
                    item = QtWidgets.QTableWidgetItem()
                    self.BillTable.setItem(row, 0, item)
                    item.setText('')
                    item = QtWidgets.QTableWidgetItem()
                    self.BillTable.setItem(row, 2, item)
                    item.setText('0')
                if row==self.BillTable.rowCount()-3:
                    item = QtWidgets.QTableWidgetItem()
                    self.BillTable.setItem(row, 0, item)
                    item.setText('Sub Total')
                    item = QtWidgets.QTableWidgetItem()
                    self.BillTable.setItem(row, 2, item)
                    item.setText(subtotal)
                if row==self.BillTable.rowCount()-2:
                    item = QtWidgets.QTableWidgetItem()
                    self.BillTable.setItem(row, 0, item)
                    item.setText('GST')
                    item = QtWidgets.QTableWidgetItem()
                    self.BillTable.setItem(row, 2, item)
                    item.setText(GST)
                if row==self.BillTable.rowCount()-1:
                    item = QtWidgets.QTableWidgetItem()
                    self.BillTable.setItem(row, 0, item)
                    item.setText('Total')
                    item = QtWidgets.QTableWidgetItem()
                    self.BillTable.setItem(row, 2, item)
                    item.setText(Total)
            self.RowChange = True
        else:
            pass

    def summ(self,x):
        summation=0
        if x!=self.BillTable.rowCount()-1 and x!=self.BillTable.rowCount()-2 and x!=self.BillTable.rowCount()-3 and self.RowChange:
            if self.BillTable.currentColumn()==2:
                for row in range(self.BillTable.rowCount()-3):
                    try:
                        summation = summation+float(self.BillTable.item(row,2).text())
                    except:
                        summation = summation+0
                
                item = QtWidgets.QTableWidgetItem()
                self.BillTable.setItem((self.BillTable.rowCount()-3), 2, item)
                item.setText(str(summation))
                if self.StateCode.text()=='0' or self.StateCode.text()=='29':
                    item = QtWidgets.QTableWidgetItem()
                    self.GSTRate.setItem(0, 1, item)
                    item.setText(str(round(summation*(float(self.GSTRate.item(0,0).text())/100))))
                    item = QtWidgets.QTableWidgetItem()
                    self.GSTRate.setItem(1, 1, item)
                    item.setText(str(round(summation*(float(self.GSTRate.item(1,0).text())/100))))
                    item = QtWidgets.QTableWidgetItem()
                    self.GSTRate.setItem(2, 1, item)
                    item.setText(str(0))
                else:
                    item = QtWidgets.QTableWidgetItem()
                    self.GSTRate.setItem(2, 1, item)
                    item.setText(str(round(summation*(float(self.GSTRate.item(2,0).text())/100))))
                    item = QtWidgets.QTableWidgetItem()
                    self.GSTRate.setItem(0, 1, item)
                    item.setText(str(0))
                    item = QtWidgets.QTableWidgetItem()
                    self.GSTRate.setItem(1, 1, item)
                    item.setText(str(0))
                item = QtWidgets.QTableWidgetItem()
                self.GSTRate.setItem(3, 1, item)
                item.setText(str(round(float(self.GSTRate.item(0, 1).text())+float(self.GSTRate.item(1, 1).text())+float(self.GSTRate.item(2, 1).text()))))
                item = QtWidgets.QTableWidgetItem()
                self.BillTable.setItem(self.BillTable.rowCount()-2, 2, item)
                item.setText(str(float(self.GSTRate.item(3, 1).text())))
                item = QtWidgets.QTableWidgetItem()
                self.BillTable.setItem(self.BillTable.rowCount()-1, 2, item)
                item.setText(str(round(float(self.BillTable.item(self.BillTable.rowCount()-2, 2).text())+float(self.BillTable.item(self.BillTable.rowCount()-3, 2).text()))))

    def getStateCode(self):
        StateCode2 = self.GST.text()[:2]
        if StateCode2.isnumeric() and StateCode2!='':
            self.StateCode.setValue(int(StateCode2))
        else:
            self.StateCode.setValue(0)
                             
    def CalcGST(self):
        try:
            if int(self.StateCode.value())==0 or int(self.StateCode.value())==29:
                item = QtWidgets.QTableWidgetItem()
                self.GSTRate.setItem(0, 1, item)
                item.setText(str(round(float(self.BillTable.item(self.BillTable.rowCount()-3, 2).text())*(float(self.GSTRate.item(0,0).text())/100))))
                item = QtWidgets.QTableWidgetItem()
                self.GSTRate.setItem(1, 1, item)
                item.setText(str(round(float(self.BillTable.item(self.BillTable.rowCount()-3, 2).text())*(float(self.GSTRate.item(1,0).text())/100))))
                item = QtWidgets.QTableWidgetItem()
                self.GSTRate.setItem(2, 1, item)
                item.setText(str(0))
            else:
                item = QtWidgets.QTableWidgetItem()
                self.GSTRate.setItem(2, 1, item)
                item.setText(str(round(float(self.BillTable.item(self.BillTable.rowCount()-3, 2).text())*(float(self.GSTRate.item(2,0).text())/100))))
                item = QtWidgets.QTableWidgetItem()
                self.GSTRate.setItem(0, 1, item)
                item.setText(str(0))
                item = QtWidgets.QTableWidgetItem()
                self.GSTRate.setItem(1, 1, item)
                item.setText(str(0))
        except:
            pass
        
    def handleHeaderMenu_client(self, pos):
        x,y = pos.x(), pos.y()
        it = self.BillTable.indexAt(pos)
        row = it.row()
        if it is None or row>=self.BillTable.rowCount()-3: return
        menu = QtWidgets.QMenu()
        edit = menu.addAction("Delete")
        action = menu.exec_(self.BillTable.viewport().mapToGlobal(pos))
        if action == edit:
            self.BillTable.removeRow(row)
            self.NoOfItems.setValue(self.NoOfItems.value()-1)
            summation=0
            for row in range(self.BillTable.rowCount()-3):
                try:
                   summation = summation+float(self.BillTable.item(row,2).text())
                except:
                    summation = summation+0
            item = QtWidgets.QTableWidgetItem()
            self.BillTable.setItem((self.BillTable.rowCount()-3), 2, item)
            item.setText(str(summation))
            if self.StateCode.text()=='' or self.StateCode.text()=='29':
                item = QtWidgets.QTableWidgetItem()
                self.GSTRate.setItem(0, 1, item)
                item.setText(str(round(summation*(float(self.GSTRate.item(0,0).text())/100))))
                item = QtWidgets.QTableWidgetItem()
                self.GSTRate.setItem(1, 1, item)
                item.setText(str(round(summation*(float(self.GSTRate.item(1,0).text())/100))))
                item = QtWidgets.QTableWidgetItem()
                self.GSTRate.setItem(2, 1, item)
                item.setText(str(0))
            else:
                item = QtWidgets.QTableWidgetItem()
                self.GSTRate.setItem(2, 1, item)
                item.setText(str(round(summation*(float(self.GSTRate.item(2,0).text())/100))))
                item = QtWidgets.QTableWidgetItem()
                self.GSTRate.setItem(0, 1, item)
                item.setText(str(0))
                item = QtWidgets.QTableWidgetItem()
                self.GSTRate.setItem(1, 1, item)
                item.setText(str(0))
            item = QtWidgets.QTableWidgetItem()
            self.GSTRate.setItem(3, 1, item)
            item.setText(str(round(float(self.GSTRate.item(0, 1).text())+float(self.GSTRate.item(1, 1).text())+float(self.GSTRate.item(2, 1).text()))))
            item = QtWidgets.QTableWidgetItem()
            self.BillTable.setItem(self.BillTable.rowCount()-2, 2, item)
            item.setText(str(float(self.GSTRate.item(3, 1).text())))
            item = QtWidgets.QTableWidgetItem()
            self.BillTable.setItem(self.BillTable.rowCount()-1, 2, item)
            item.setText(str(round(float(self.BillTable.item(self.BillTable.rowCount()-2, 2).text())+float(self.BillTable.item(self.BillTable.rowCount()-3, 2).text()))))
                             
    def GenerateBill(self):
        print(os.getcwd())
        ClientName = self.CompanySelect.currentText()
        Address = self.Address.text()
        GSTNo = self.GST.text()
        StateCode = str(self.StateCode.value())
        BillNo = self.BillNo.text()
        Date = datetime.datetime.strftime(self.Date.date().toPython(),'%d.%m.%Y')
        if self.RB_Regular.isChecked():
            Regular=True
        else:
            Regular=False
        ParticularList=[]
        for x in range(self.BillTable.rowCount()-3):
            m=[]
            for y in range(self.BillTable.columnCount()):
                try:
                    if y==1:
                        m.append(self.BillTable.item(x,y).text().replace('/','/\n'))
                    else:
                        m.append(self.BillTable.item(x,y).text())
                    if y==2:
                        m.append(self.BillTable.item(x,y).text())
                except:
                    m.append('')
            ParticularList.append(m)
        if StateCode =='0' or StateCode =='29':
            GSTRate = {'CGST':[self.GSTRate.item(0, 0).text(),self.GSTRate.item(0, 1).text()],'SGST':[self.GSTRate.item(1, 0).text(),self.GSTRate.item(1, 1).text()]}
        else:
            GSTRate = {'IGST':[self.GSTRate.item(2, 0).text(),self.GSTRate.item(2, 1).text()]}
        infoList = [self.PANGST.item(0,0).text(),self.PANGST.item(1,0).text()]
        bankInfo = [self.BankDetails.item(0,0).text(),self.BankDetails.item(1,0).text(),self.BankDetails.item(2,0).text(),self.BankDetails.item(3,0).text(),self.BankDetails.item(4,0).text(),self.BankDetails.item(5,0).text()]
        TotalAmount = self.BillTable.item(self.BillTable.rowCount()-1, 2).text()
        Bill=Bills.createDoc()
        Bill.BillDetails(ClientName,Address,BillNo,Date,'',GSTNo,StateCode)
        Bill.BillParticulars(ParticularList,GSTRate,TotalAmount, Regular)
        Bill.infoTable(infoList,bankInfo)
        self.FilePath = os.path.join('BILLS',BillNo.split('/')[2]+'_'+ClientName)
        Bill.saveDoc(self.FilePath)
        dbFile = [BillNo,Date,ClientName,TotalAmount,'Regular' if Regular else 'Reimbursemet',os.path.abspath(self.FilePath)]
        db.Bills(dbFile)
        self.Feedback("Success","Document Generated Successfully",link="View Document")

    def generateHistory(self):
        self.conn = sqlite3.connect(self.dbfilepath)
        self.cur = self.conn.cursor()
        try:
            BillList = self.cur.execute(f'SELECT * from Bills WHERE "CLIENT" = "{self.CompanySelection}"').fetchall()
            IsBillsFound = True
        except Exception as e:
            IsBillsFound = False
            print(e)
        
        if IsBillsFound:
            print(BillList)
            self.History.setRowCount(len(BillList))
            for x in range(len(BillList)):
                item = QtWidgets.QTableWidgetItem()
                self.History.setItem(x, 0, item)
                item.setFlags(QtCore.Qt.ItemIsEnabled)
                item.setText(BillList[x][1])
                item = QtWidgets.QTableWidgetItem()
                self.History.setItem(x, 1, item)
                item.setFlags(QtCore.Qt.ItemIsEnabled)
                item.setText(BillList[x][0])
                item = QtWidgets.QTableWidgetItem()
                self.History.setItem(x, 2, item)
                item.setFlags(QtCore.Qt.ItemIsEnabled)
                item.setText(BillList[x][3])
                item = QtWidgets.QTableWidgetItem()
                self.History.setItem(x, 3, item)
                item.setFlags(QtCore.Qt.ItemIsEnabled)
                item.setText(BillList[x][4])
                item = QtWidgets.QTableWidgetItem()
                self.History.setItem(x, 4, item)
                item.setFlags(QtCore.Qt.ItemIsEnabled)
                item.setText(BillList[x][5].replace('\\\\','\\'))
            self.History.resizeColumnsToContents()
            self.History.itemDoubleClicked.connect(self.OpenLink)

    def OpenLink(self,item):
        if item.column() == 4:
            webbrowser.open((self.History.item(item.row(),4).text()+'.docx'))

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
        os.startfile('"'+self.FilePath+'.docx'+'"')
        
        
