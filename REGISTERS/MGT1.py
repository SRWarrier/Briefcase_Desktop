from PySide2 import QtWidgets, QtUiTools,QtCore, QtGui
from PySide2.QtPrintSupport import QPrintDialog, QPrinter
import sys
import HomePage
import os
from functions import pyside_dynamic
#from functions.Gdrive import Gdrive
import requests_html
import sqlite3
import pandas as pd
import pickle
from functions import Database_Manager as db
import math
import datetime
from functools import partial

class Ui(QtWidgets.QWidget):
    def __init__(self, CIN):
        super(Ui, self).__init__()
        pyside_dynamic.loadUi('Resources/ui/MGT1.ui',self)
        self.CIN = CIN
        with open('Config','rb') as f:
            self.Config = pickle.loads(f.read())
            f.close()
        self.preventSave = False
        self.dbfilepath = os.path.join(self.Config['Database'],'C3_DataBase.db')
        self.Nameentry = self.findChild(QtWidgets.QComboBox, 'CompanySelect')
        self.conn = sqlite3.connect(self.dbfilepath)
        self.cur = self.conn.cursor()
        CompanyDetails= self.cur.execute(f'SELECT "company_name", "company_registered_address" from Masterdata WHERE company_cin = "{CIN}"').fetchall()[0]
        self.CompanyName.setText(CompanyDetails[0])
        self.RegOffice.setText(CompanyDetails[1])
        self.AddMember.clicked.connect(self.hideIndex)
        self.saveButton.setEnabled(False)
        self.saveButton.clicked.connect(self.saveData)
        self.ExportToPDF.setEnabled(False)
        self.ExportToPDF.clicked.connect(self.printFolio)
        self.bindRegister.clicked.connect(self.BindAllFolio)
        self.ExportToPDF.setStyleSheet("background-color:rgb(233, 233, 233);color:rgb(12,12,12);border-radius:2")
        self.saveButton.setStyleSheet("background-color:rgb(233, 233, 233);color:rgb(12,12,12);border-radius:2")
        self.gotoIndex.clicked.connect(self.openIndex)
        self.exportIndex.clicked.connect(self.exportIndexPDF)
        self.tabWidget.setCurrentIndex(0)
        self.tabWidget.setTabEnabled(1,False)
        self.tabWidget.setTabEnabled(2,False)
        self.addRow.clicked.connect(self.addOneRow)
        self.sharesTable.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.sharesTable.customContextMenuRequested.connect(self.contextMenu2)
        self.sharesTable.currentCellChanged.connect(self.refreshShareTable)
        self.sharesTable.setItemDelegate(ValidatedItemDelegate())
        self.showFolio.clicked.connect(self.showFolioNos)
        self.updateIndex()
        self.update = False
        self.registeredaddress = self.findChild(QtWidgets.QLineEdit, 'RegisteredOffice')

    def showFolioNos(self):
        widget = QtWidgets.QWidget()
        pyside_dynamic.loadUi('Resources/ui/showFolio.ui',widget)
        table = widget.display
        filterDict = self.ShareholdersList[self.shareClass.text().upper()]
        table.setRowCount(len(filterDict))
        for ROW, key in enumerate(filterDict.keys()):
            item = QtWidgets.QTableWidgetItem()
            item.setFlags(~QtCore.Qt.ItemIsEditable)
            table.setItem(ROW, 0, item)
            item.setText(key)
            item = QtWidgets.QTableWidgetItem()
            item.setFlags(~QtCore.Qt.ItemIsEditable)
            table.setItem(ROW, 1, item)
            item.setText(filterDict[key][1])
        widget.show()
            
    def BindAllFolio(self):
        fn, _ = QtWidgets.QFileDialog.getSaveFileName(self, 'Export PDF', None, 'PDF files (.pdf);;All Files()')
        if fn != '':
            blockUser = QtWidgets.QMessageBox(self)
            blockUser.setText("The Register is being bind. Plase wait till the preocess is complete")
            blockUser.setStandardButtons(QtWidgets.QMessageBox.NoButton)
            blockUser.setModal(False); 
            blockUser.show()
            if QtCore.QFileInfo(fn).suffix() == "" : fn += '.pdf'
            printer = QPrinter(QPrinter.HighResolution)
            printer.setOutputFormat(QPrinter.PdfFormat)
            printer.setPaperSize(QPrinter.A4)
            printer.setOutputFileName(fn)
            printer.setFullPage(True)
            #printer.setPageMargins(12, 16, 12, 20, QPrinter.Millimeter)
            printer.setOrientation(QPrinter.Landscape)
            document = QtGui.QTextDocument()
            pageSize = printer.paperSize(QPrinter.Point)
            document.setPageSize(pageSize)
            document.setDocumentMargin(20)
            childTables = self.IndexWindow.findChildren(QtWidgets.QTableWidget)
            html = '<HTML><BODY>'
            html = html+"<style>table, th, td {border: 1px solid black;border-collapse: collapse;font-size: 10px;padding: 1px}</style>"# HTML STYLE
            html = html+f'\n<H1 style="text-align:center;margin: 0;"><b>MGT-1</b></H1>'
            html = html+f'\n<H2 style="text-align:center;margin: 0;"><b>{self.subtitle.text()}</b><br></H2>'
            html = html+f'\n<H2 style="text-align:center;margin: 0;"><b><u>INDEX</u></b><br></H2>'
            for table in childTables:
                html = html+ f'\n<H3 style="text-align:center;margin: 0;"><b><u>{table.item(0,3).text()}</u></b><br></H3>'
                html = html+ '<table style="width:100%;">'
                html = html+'<tr>\n'
                for column in range(5):
                    if column!=3:
                        html =html+f'<th>{table.horizontalHeaderItem(column).text()}</th>\n'
                html = html+'</tr>'
                for row in range(table.rowCount()):
                    html = html+'<tr>\n'
                    for column in range(5):
                        if column !=3:
                            try:
                                html = html+'<td>'+table.item(row, column).text()+'</td>\n'
                            except:
                                html = html+'<td>'+''+'</td>\n'
                    html = html+'</tr>\n'
                html = html+ '</table>\n'
            html= html+'\n</BODY></HTML>'
            document.setHtml(html)
            document.print_(printer)
            painter = QtGui.QPainter()
            painter.begin(printer)
            document.drawContents(painter, printer.pageRect())
            
            for table in childTables:
                for row in range(table.rowCount()-1):
                    print("Test")
                    folioNo = table.item(row,0).text()
                    ClassName = table.item(row,3).text()
                    self.activateMember(folioNo, ClassName)
                    html = '<HTML><BODY>'
                    html = html+"<style>table, th, td {border: 1px solid black;border-collapse: collapse;font-size: 10px;padding: 1px}</style>"# HTML STYLE
                    html = html+f'\n<H1 style="text-align:center;margin: 0;"><b>MGT-1</b></H1>'
                    html = html+f'\n<H2 style="text-align:center;margin: 0;"><b>{self.subtitle.text()}</b></H2>'
                    html = html+f'\n<H4 style="text-align:center;margin: 0;"><b>{self.info.text()}</b><br></H4>'
                    html = html+f'\n<H4 style="text-align:left;margin: 0;">Name of the company:\t{self.CompanyName.text()}</H4>'
                    html = html+f'\n<H4 style="text-align:left;margin: 0;">Registered office address:\t{self.RegOffice.text()}<br></H4>'
                    html = html+f'\n<H4 style="text-align:left;margin: 0;"><b>(TO BE MAINTAINED SEPARATELY FOR EACH CLASS OF SHARES)</b><br></H4>'
                    html = html+ '<table style="width:100%;">'
                    html = html+f'<tr><td width="40%">Class of shares:</td><td width="60%">{self.shareClass.text().upper()}</td></tr>'
                    html = html+f'<tr><td width="40%">Nominal value per share (in Rs.)::</td><td width="60%">{self.nominalValue.text()}</td></tr>'
                    html = html+f'<tr><td width="40%">Total shares held:</td><td width="60%">{self.totalShares.text()}</td></tr>'
                    model = self.personalInfo
                    for row in range(model.rowCount()):
                        if row==9:continue
                        label = model.verticalHeaderItem(row).text()
                        for column in range(model.columnCount()):
                            html = html+'<tr>'
                            html = html+'<td width="40%">'+label+'</td>'
                            try:
                                html = html+'<td width="60%">'+model.item(row, column).text()+'</td>'
                            except:
                                html = html+'<td width="60%">'+'-'+'</td>'
                    html = html+ '</table>'
                    html= html+'\n</BODY></HTML>'
                    document.setHtml(html)
                    printer.newPage()
    
                    # Draw the first page removing the pageRect offset due to margins.
                    document.drawContents(painter, printer.pageRect())#.translated( -printer.pageRect().x(), -    printer.pageRect().y() ))

                    sharesTable = self.sharesTable
                    rowFactor = math.ceil(sharesTable.rowCount()//20)
                    for fax in range(1 if rowFactor==0 else rowFactor):
                        html = '<HTML><BODY>'
                        html = html+"<style>table, th, td {border: 1px solid black;border-collapse:collapse;font-size: 9px;padding: 0.5px} tr {height: 5%}</style>"# HTML STYLE
                        html = html+f'\n<H2 style="text-align:left;float:left;margin: 0;"><b>ALLOTMENTS</b></H2>'
                        html = html+f'\n<H3 style="text-align:right;float:left;margin: 0;"><b>Class:{ClassName}</b></H3>'
                        html = html+f'\n<H3 style="text-align:right;float:left;margin: 0;"><b>Folio No:{model.item(0, 0).text()}</b></H3>'
                        html = html+ '<table style="width:100%;">'
                        html = html+'<tr>'
                        for column in range(14):
                            html =html+f'<th>{sharesTable.horizontalHeaderItem(column).text()}</th>\n'
                        html = html+'</tr>'
                        for row in range(20*fax,20*(fax+1),1):
                            html = html+'<tr>'
                            for column in range(14):
                                try:
                                    html = html+'<td>'+sharesTable.item(row, column).text()+'</td>'
                                except:
                                    html = html+'<td>'+'-'+'</td>'
                            html = html+'</tr>'
                        document.setHtml(html)

                        # A new page
                        printer.newPage()

                        # The second page
                        document.drawContents(painter, printer.pageRect().translated( -printer.pageRect().x(), -printer.pageRect().y() ))

                        html = '<HTML><BODY>'
                        html = html+"<style>table, th, td {border: 1px solid black;border-collapse: collapse;font-size: 9px;padding: 0.5px}</style>"# HTML STYLE
                        html = html+f'\n<H2 style="text-align:left;float:left;margin: 0;"><b>TRANSFERS</b></H2>'
                        html = html+f'\n<H3 style="text-align:right;float:left;margin: 0;"><b>Class:{ClassName}</b></H3>'
                        html = html+f'\n<H3 style="text-align:right;float:left;margin: 0;"><b>Folio No:{model.item(0, 0).text()}</b></H3>'
                        html = html+ '<table style="width:100%;">'
                        html = html+'<tr>\n'
                        for column in range(14,sharesTable.columnCount(),1):
                            html =html+f'<th>{sharesTable.horizontalHeaderItem(column).text()}</th>\n'
                        html = html+'</tr>'
                        for row in range(20*fax,20*(fax+1),1):
                            html = html+'<tr>\n'
                            for column in range(14,sharesTable.columnCount(),1):
                                try:
                                    html = html+'<td height="40%";>'+sharesTable.item(row, column).text()+'</td>\n'
                                except:
                                    html = html+'<td height="40%";>'+''+'</td>\n'
                            html = html+'</tr>\n'
                        document.setHtml(html)

                        # A new page
                        printer.newPage()

                        # The Third page
                        document.drawContents(painter, printer.pageRect().translated( -printer.pageRect().x(), -printer.pageRect().y() ))
                        
                        
            painter.end()
            blockUser.done(1)
            self.tabWidget.setTabEnabled(1,False)
            self.tabWidget.setTabEnabled(2,False)

                            
    def addOneRow(self):
        self.sharesTable.insertRow(self.sharesTable.rowCount())

    def exportIndexPDF(self):
        fn, _ = QtWidgets.QFileDialog.getSaveFileName(self, 'Export PDF', None, 'PDF files (.pdf);;All Files()')
        if fn != '':
            if QtCore.QFileInfo(fn).suffix() == "" : fn += '.pdf'
            self.conn = sqlite3.connect(self.registerPath)
            self.cur = self.conn.cursor()
            printer = QPrinter(QPrinter.HighResolution)
            printer.setOutputFormat(QPrinter.PdfFormat)
            printer.setPaperSize(QPrinter.A4)
            printer.setOutputFileName(fn)
            printer.setFullPage(True)
            #printer.setPageMargins(12, 16, 12, 20, QPrinter.Millimeter)
            printer.setOrientation(QPrinter.Landscape)
            document = QtGui.QTextDocument()
            pageSize = printer.paperSize(QPrinter.Point)
            document.setPageSize(pageSize)
            document.setDocumentMargin(20)
            childTables = self.IndexWindow.findChildren(QtWidgets.QTableWidget)
            html = '<HTML><BODY>'
            html = html+"<style>table, th, td {border: 1px solid black;border-collapse: collapse;font-size: 10px;padding: 1px}</style>"# HTML STYLE
            html = html+f'\n<H3 style="text-align:center;margin: 0;"><b>LIST OF SHAREHOLDERS OF {self.CompanyName.text().upper()} as on {datetime.datetime.now().strftime("%d.%m.%Y")}</b><br><br></H3>'
            for table in childTables:
                faceValue = self.cur.execute(f'SELECT "nominal_value" from MGT1PERSONAL WHERE company_cin = "{self.CIN}" AND class = "{table.item(0,3).text()}"').fetchall()[0][0] 
                html = html+ f'\n<H3 style="text-align:center;margin: 0;"><b><u>{table.item(0,3).text()}</u></b><br></H3>'
                html = html+ '<table style="width:100%;">'
                html = html+'<tr>\n'
                for column in range(5):
                    if column!=3:
                        html =html+f'<th>{table.horizontalHeaderItem(column).text()}</th>\n'
                html =html+f'<th>Face Value in Rs.</th>\n'
                html =html+f'<th>Value of Shares in Rs.</th>\n'
                html = html+'</tr>'
                for row in range(table.rowCount()):
                    try:
                        if table.item(row, 4).text() !='' and table.item(row, 4).text() != '0':
                            html = html+'<tr>\n'
                            for column in range(5):
                                if column !=3:
                                    width = '5%' if column==0 else str(95/6)+'%'
                                    try:
                                        html = html+f'<td width="{width}">'+table.item(row, column).text()+'</td>\n'
                                    except:
                                        html = html+'<td width="{width}">'+''+'</td>\n'
                            html = html+f'<td width="{width}">'+faceValue+'/-'+'</td>\n'
                            html = html+f'<td width="{width}">'+str(float(faceValue)*int(table.item(row, column).text()))+'/-'+'</td>\n'
                            html = html+'</tr>\n'
                    except:
                        pass
                html = html+ '</table>\n<br><br>'
            html= html+'\n</BODY></HTML>'
            document.setHtml(html)
            document.print_(printer)
    
    def openIndex(self, decision=False):
        if not decision:
            decision = QtWidgets.QMessageBox.warning(self, 'Unsaved Information', "Do want to proceed to Index page? All unsaved data will be lost", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
        if decision == QtWidgets.QMessageBox.Yes or decision == True:
            self.ExportToPDF.setEnabled(False)
            self.ExportToPDF.setStyleSheet("background-color:rgb(233, 233, 233);color:rgb(12,12,12);border-radius:2")
            self.saveButton.setStyleSheet("background-color:rgb(233, 233, 233);color:rgb(12,12,12);border-radius:2")
            self.saveButton.setEnabled(False)
            self.bindRegister.setStyleSheet("background-color:rgb(231, 29, 54);color:rgb(255,255,255);border-radius:2")
            self.bindRegister.setEnabled(True)
            self.tabWidget.setTabEnabled(0,True)
            self.tabWidget.setTabEnabled(1,False)
            self.tabWidget.setTabEnabled(2,False)
            self.tabWidget.setCurrentIndex(0)
        else:
            pass
        
    def hideIndex(self):
        self.ExportToPDF.setEnabled(True)
        self.ExportToPDF.setStyleSheet("background-color:rgb(255, 159, 28);color: rgb(255, 255, 255);border-radius:2")
        self.saveButton.setStyleSheet("background-color:rgb(46, 196, 182);color: rgb(255, 255, 255);border-radius:2")
        self.saveButton.setEnabled(True)
        self.bindRegister.setStyleSheet("background-color:rgb(233, 233, 233);color:rgb(12,12,12);border-radius:2")
        self.bindRegister.setEnabled(False)
        self.tabWidget.setTabEnabled(0,False)
        self.tabWidget.setTabEnabled(1,True)
        self.tabWidget.setTabEnabled(2,True)
        self.tabWidget.setCurrentIndex(1)
        for ROW in range(self.sharesTable.rowCount()):
            item = QtWidgets.QTableWidgetItem()
            item.setFlags(~QtCore.Qt.ItemIsEditable)
            self.sharesTable.setItem(ROW, 20, item)
            item = QtWidgets.QTableWidgetItem()
            item.setFlags(~QtCore.Qt.ItemIsEditable)
            self.sharesTable.setItem(ROW, 19, item)
            item = QtWidgets.QTableWidgetItem()
            item.setFlags(~QtCore.Qt.ItemIsEditable)
            self.sharesTable.setItem(ROW, 6, item)

    def updateIndex(self):
        clearLayout(self.IndexWindow.layout())
        self.registerPath = os.path.join(self.Config['Database'],'registers.db')
        if os.path.isfile(self.registerPath):
            self.conn = sqlite3.connect(self.registerPath)
            self.cur = self.conn.cursor()
            getShareClasses = self.cur.execute(f'SELECT "class" from MGT1PERSONAL WHERE company_cin = "{self.CIN}"').fetchall()
            classList = []
            for xclass in getShareClasses:
                classList.append(xclass[0])
            classList  = list(set(classList))
            self.ShareholdersList = {}
            for shareClass in classList:
                self.ShareholdersList[shareClass]={}
                indexData= self.cur.execute(f'SELECT "folio_no","name", "address","class","total_shares","mem_date","cessation_date","folio_no" from MGT1PERSONAL WHERE company_cin = "{self.CIN}" AND class = "{shareClass}"').fetchall()
                indexTbl = QtWidgets.QWidget()
                indexTbl.setObjectName(shareClass.replace(' ',''))
                pyside_dynamic.loadUi('Resources/ui/MGT1Index.ui',indexTbl)
                indexTbl.IndexTable.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
                indexTbl.IndexTable.customContextMenuRequested.connect(self.contextMenu)
                indexTbl.IndexTable.setColumnWidth(0, 80)
                indexTbl.IndexTable.setColumnWidth(1, 200)
                indexTbl.IndexTable.setColumnWidth(2, 250)
                indexTbl.IndexTable.setColumnWidth(3, 120)
                indexTbl.IndexTable.setColumnWidth(4, 110)
                indexTbl.IndexTable.setColumnWidth(5, 110)
                indexTbl.IndexTable.setColumnWidth(6, 120)
                roCount = len(indexData)+1 if len(indexData)>0 else 0
                indexTbl.IndexTable.setRowCount(roCount)
                summation=0
                for ROW, member in enumerate(indexData):
                    self.ShareholdersList[shareClass][member[0]]=[]
                    for COLUMN in range(len(member[:-1])):
                        item = QtWidgets.QTableWidgetItem()
                        indexTbl.IndexTable.setItem(ROW, COLUMN, item)
                        item.setText(str(member[COLUMN]))
                        self.ShareholdersList[shareClass][member[0]].append(str(member[COLUMN]))
                        if COLUMN==4:
                            item.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignBottom)
                        item.setFlags(QtCore.Qt.ItemIsEnabled)
                    MoreInfo = QtWidgets.QPushButton()
                    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
                    sizePolicy.setHorizontalStretch(0)
                    sizePolicy.setVerticalStretch(0)
                    sizePolicy.setHeightForWidth(MoreInfo.sizePolicy().hasHeightForWidth())
                    MoreInfo.setSizePolicy(sizePolicy)
                    MoreInfo.setMaximumSize(QtCore.QSize(120, 16777215))
                    font = QtGui.QFont()
                    font.setFamily("Open Sans")
                    font.setPointSize(10)
                    font.setStyleStrategy(QtGui.QFont.PreferAntialias)
                    MoreInfo.setFont(font)
                    MoreInfo.setStyleSheet("background-color: rgb(85, 255, 255);")
                    MoreInfo.setText('Edit')
                    MoreInfo.setObjectName(shareClass.replace(' ','~')+'|'+str(member[-1]))
                    MoreInfo.clicked.connect(self.editMember)
                    indexTbl.IndexTable.setCellWidget(ROW, 7, MoreInfo)
                    summation = summation+int(indexTbl.IndexTable.item(ROW,4).text())
                item = QtWidgets.QTableWidgetItem()
                indexTbl.IndexTable.setItem(indexTbl.IndexTable.rowCount()-1, 3, item)
                item.setText("TOTAL")
                item.setFlags(QtCore.Qt.ItemIsEnabled)
                item = QtWidgets.QTableWidgetItem()
                indexTbl.IndexTable.setItem(indexTbl.IndexTable.rowCount()-1, 4, item)
                item.setText(str(summation))
                item.setTextAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignBottom)
                item.setFlags(QtCore.Qt.ItemIsEnabled)
                self.IndexWindow.layout().addWidget(indexTbl)
        

    def activateMember(self,folioNo,ShareClass):
        self.tabWidget.setTabEnabled(1,True)
        self.tabWidget.setTabEnabled(2,True)
        PersonalInfo= self.cur.execute(f'SELECT * from MGT1PERSONAL WHERE company_cin = "{self.CIN}" AND folio_no = "{folioNo}" AND class = "{ShareClass}"').fetchall()[0]
        shareInfo = self.cur.execute(f'SELECT * from MGT1SH WHERE company_cin = "{self.CIN}" AND folio_no = "{folioNo}" AND class = "{ShareClass}"').fetchall()
        self.shareClass.setText(PersonalInfo[1].upper())
        self.nominalValue.setText(PersonalInfo[2])
        self.totalShares.setText(PersonalInfo[3])
        for ROW, info in enumerate(PersonalInfo[4:]):
            item = QtWidgets.QTableWidgetItem()
            self.personalInfo.setItem(ROW, 0, item)
            item.setText(str(info))
        self.sharesTable.setRowCount(len(shareInfo))
        for ROW, share in enumerate(shareInfo):
            for COLUMN in range(len(share[3:])):
                item = QtWidgets.QTableWidgetItem()
                self.sharesTable.setItem(ROW, COLUMN, item)
                item.setText(str(share[COLUMN+3]))
        
        
    def editMember(self):
        sender = self.sender()
        TableData = sender.objectName().split('|')
        folioNo = TableData[1]
        TableName = TableData[0].replace('~',' ')
        parent = sender.parent()
        self.update = True
        self.ExportToPDF.setEnabled(True)
        self.ExportToPDF.setStyleSheet("background-color:rgb(255, 159, 28);color: rgb(255, 255, 255);border-radius:2")
        self.saveButton.setStyleSheet("background-color:rgb(46, 196, 182);color: rgb(255, 255, 255);border-radius:2")
        self.saveButton.setEnabled(True)
        self.bindRegister.setStyleSheet("background-color:rgb(233, 233, 233);color:rgb(12,12,12);border-radius:2")
        self.bindRegister.setEnabled(False)
        self.tabWidget.setTabEnabled(0,False)
        self.tabWidget.setTabEnabled(1,True)
        self.tabWidget.setTabEnabled(2,True)
        self.tabWidget.setCurrentIndex(1)
        PersonalInfo= self.cur.execute(f'SELECT * from MGT1PERSONAL WHERE company_cin = "{self.CIN}" AND folio_no = "{folioNo}" AND class = "{TableName}"').fetchall()[0]
        shareInfo = self.cur.execute(f'SELECT * from MGT1SH WHERE company_cin = "{self.CIN}" AND folio_no = "{folioNo}" AND class = "{TableName}"').fetchall()
        self.shareClass.setText(PersonalInfo[1].upper())
        self.nominalValue.setText(PersonalInfo[2])
        self.totalShares.setText(PersonalInfo[3])
        for ROW, info in enumerate(PersonalInfo[4:]):
            item = QtWidgets.QTableWidgetItem()
            self.personalInfo.setItem(ROW, 0, item)
            item.setText(str(info))
        self.sharesTable.setRowCount(len(shareInfo))
        for ROW, share in enumerate(shareInfo):
            for COLUMN in range(len(share[3:])):
                item = QtWidgets.QTableWidgetItem()
                if COLUMN in (20,19,6):
                    item.setFlags(~QtCore.Qt.ItemIsEditable)
                self.sharesTable.setItem(ROW, COLUMN, item)
                item.setText(str(share[COLUMN+3]))

            
    def contextMenu(self, pos):
        sender = self.sender()
        x,y = pos.x(), pos.y()
        it = sender.indexAt(pos)
        self.selectedrow = it.row()
        self.companyName = sender.model().index(self.selectedrow, 1).data()
        self.LFNO = sender.model().index(self.selectedrow, 0).data()
        self.delClass = sender.model().index(self.selectedrow, 3).data()
        if it is None: return
        menu = QtWidgets.QMenu()
        delete = menu.addAction("Delete")
        action = menu.exec_(sender.viewport().mapToGlobal(pos))
        if action == delete:
            msgBox = QtWidgets.QMessageBox(self)
            msgBox.setIcon(QtWidgets.QMessageBox.Warning)
            msgBox.setText(f"Do you really want to delete {self.companyName}?")
            msgBox.setWindowTitle("Delete?")
            msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
            msgBox.buttonClicked.connect(self.decision)
            msgBox.show()

    def contextMenu2(self, pos):
        x,y = pos.x(), pos.y()
        it = self.sharesTable.indexAt(pos)
        selectedrow = it.row()
        if it is None: return
        menu = QtWidgets.QMenu()
        delete = menu.addAction("Delete")
        action = menu.exec_(self.sharesTable.viewport().mapToGlobal(pos))
        if action == delete:
            self.sharesTable.removeRow(selectedrow)

    def decision(self,button):
        if button.text()=='OK':
            conn = sqlite3.connect(self.registerPath)
            cur = conn.cursor()
            cur.execute(f'DELETE FROM MGT1PERSONAL WHERE company_cin = {repr(self.CIN)} AND folio_no = "{self.LFNO}" AND class = "{self.delClass}"')
            cur.execute(f'DELETE FROM MGT1SH WHERE company_cin = {repr(self.CIN)} AND folio_no = "{self.LFNO}" AND class = "{self.delClass}"')
            cur.close()
            conn.commit()
            conn.close()
            self.updateIndex()
        else:
            pass      


    def printFolio(self):
        print("Printing")
        fn, _ = QtWidgets.QFileDialog.getSaveFileName(self, 'Export PDF', None, 'PDF files (.pdf);;All Files()')
        if fn != '':
            if QtCore.QFileInfo(fn).suffix() == "" : fn += '.pdf'
            printer = QPrinter(QPrinter.HighResolution)
            printer.setOutputFormat(QPrinter.PdfFormat)
            printer.setPaperSize(QPrinter.A4)
            printer.setOutputFileName(fn)
            printer.setFullPage(True)
            #printer.setPageMargins(12, 16, 12, 20, QPrinter.Millimeter)
            printer.setOrientation(QPrinter.Landscape)
            document = QtGui.QTextDocument()
            pageSize = printer.paperSize(QPrinter.Point)
            print(pageSize)
            document.setPageSize(pageSize)
            document.setDocumentMargin(20)
            html = '<HTML><BODY>'
            html = html+"<style>table, th, td {border: 1px solid black;border-collapse: collapse;font-size: 10px;padding: 1px}</style>"# HTML STYLE
            html = html+f'\n<H1 style="text-align:center;margin: 0;"><b>MGT-1</b></H1>'
            html = html+f'\n<H2 style="text-align:center;margin: 0;"><b>{self.subtitle.text()}</b></H2>'
            html = html+f'\n<H4 style="text-align:center;margin: 0;"><b>{self.info.text()}</b><br></H4>'
            html = html+f'\n<H4 style="text-align:left;margin: 0;">Name of the company:\t{self.CompanyName.text()}</H4>'
            html = html+f'\n<H4 style="text-align:left;margin: 0;">Registered office address:\t{self.RegOffice.text()}<br></H4>'
            html = html+f'\n<H4 style="text-align:left;margin: 0;"><b>(TO BE MAINTAINED SEPARATELY FOR EACH CLASS OF SHARES)</b><br></H4>'
            html = html+ '<table style="width:100%;">'
            html = html+f'<tr><td width="40%">Class of shares:</td><td width="60%">{self.shareClass.text().upper()}</td></tr>'
            html = html+f'<tr><td width="40%">Nominal value per share (in Rs.)::</td><td width="60%">{self.nominalValue.text()}</td></tr>'
            html = html+f'<tr><td width="40%">Total shares held:</td><td width="60%">{self.totalShares.text()}</td></tr>'
            model = self.personalInfo
            for row in range(model.rowCount()):
                if row==9:continue
                label = model.verticalHeaderItem(row).text()
                for column in range(model.columnCount()):
                    html = html+'<tr>'
                    html = html+'<td width="40%">'+label+'</td>'
                    try:
                        html = html+'<td width="60%">'+model.item(row, column).text()+'</td>'
                    except:
                        html = html+'<td width="60%">'+'-'+'</td>'
            html = html+ '</table>'
            html= html+'\n</BODY></HTML>'
            document.setHtml(html)
            document.print_(printer)
            # Create a QPainter to draw our content    
            painter = QtGui.QPainter()
            painter.begin(printer)

            # Draw the first page removing the pageRect offset due to margins.
            document.drawContents(painter, printer.pageRect())#.translated( -printer.pageRect().x(), -    printer.pageRect().y() ))

            sharesTable = self.sharesTable
            rowFactor = math.ceil(sharesTable.rowCount()//20)
            for fax in range(1 if rowFactor==0 else rowFactor):
                html = '<HTML><BODY>'
                html = html+"<style>table, th, td {border: 1px solid black;border-collapse:collapse;font-size: 9px;padding: 0.5px} tr {height: 5%}</style>"# HTML STYLE
                html = html+f'\n<H2 style="text-align:left;float:left;margin: 0;"><b>ALLOTMENTS</b></H2>'
                html = html+f'\n<H3 style="text-align:right;float:left;margin: 0;"><b>Class:{self.shareClass.text()}</b></H3>'
                html = html+f'\n<H3 style="text-align:right;float:left;margin: 0;"><b>Folio No:{model.item(0, 0).text()}</b></H3>'
                html = html+ '<table style="width:100%;">'
                html = html+'<tr>'
                for column in range(14):
                    html =html+f'<th>{sharesTable.horizontalHeaderItem(column).text()}</th>\n'
                html = html+'</tr>'
                for row in range(20*fax,20*fax+1,1):
                    html = html+'<tr>'
                    for column in range(14):
                        try:
                            html = html+'<td>'+sharesTable.item(row, column).text()+'</td>'
                        except:
                            html = html+'<td>'+'-'+'</td>'
                    html = html+'</tr>'
                document.setHtml(html)

                # A new page
                printer.newPage()

                # The second page
                document.drawContents(painter, printer.pageRect().translated( -printer.pageRect().x(), -printer.pageRect().y() ))

                html = '<HTML><BODY>'
                html = html+"<style>table, th, td {border: 1px solid black;border-collapse: collapse;font-size: 9px;padding: 0.5px}</style>"# HTML STYLE
                html = html+f'\n<H2 style="text-align:left;float:left;margin: 0;"><b>TRANSFERS</b></H2>'
                html = html+f'\n<H3 style="text-align:right;float:left;margin: 0;"><b>Class:{self.shareClass.text()}</b></H3>'
                html = html+f'\n<H3 style="text-align:right;float:left;margin: 0;"><b>Folio No:{model.item(0, 0).text()}</b></H3>'
                html = html+ '<table style="width:100%;">'
                html = html+'<tr>\n'
                for column in range(14,sharesTable.columnCount(),1):
                    html =html+f'<th>{sharesTable.horizontalHeaderItem(column).text()}</th>\n'
                html = html+'</tr>'
                for row in range(20*fax,20*fax+1,1):
                    html = html+'<tr>\n'
                    for column in range(14,sharesTable.columnCount(),1):
                        try:
                            html = html+'<td height="40%";>'+sharesTable.item(row, column).text()+'</td>\n'
                        except:
                            html = html+'<td height="40%";>'+''+'</td>\n'
                    html = html+'</tr>\n'
                document.setHtml(html)

                # A new page
                printer.newPage()

                # The Third page
                document.drawContents(painter, printer.pageRect().translated( -printer.pageRect().x(), -printer.pageRect().y() ))

                # Done.
            painter.end()
            #painter.print_(printer)
            
    def refreshShareTable(self,currentRow, currentColumn, previousRow, previousColumn):
        if previousColumn==2 or previousColumn==15:
            self.preventSave = False
            totalSum = 0
            for row in range(self.sharesTable.rowCount()):
                    rowSum = 0
                    try:
                        rowSum = rowSum + int(self.sharesTable.item(row, 2).text())
                    except:
                        pass
                    try:
                        rowSum = rowSum - int(self.sharesTable.item(row, 15).text())
                    except:
                        pass
                    totalSum = totalSum+rowSum
                    item = QtWidgets.QTableWidgetItem()
                    item.setFlags(~QtCore.Qt.ItemIsEditable)
                    self.sharesTable.setItem(row, 20, item)
                    item.setText(str(totalSum))
                    if totalSum<0:
                        self.sharesTable.item(row, 20).setBackground(QtCore.Qt.red)
                        self.preventSave = True

        elif previousColumn==18 or previousColumn==5:
            filterDict = self.ShareholdersList[self.shareClass.text().upper()]
            folioNO = self.sharesTable.item(previousRow, previousColumn).text()
            if folioNO == self.personalInfo.item(0,0).text():
               QtWidgets.QMessageBox.warning(self, 'Invalid Folio', f"Share cannot be transferred within the same folio")
               item = QtWidgets.QTableWidgetItem()
               item.setFlags(~QtCore.Qt.ItemIsEditable)
               self.sharesTable.setItem(previousRow, previousColumn+1, item)
               item.setText('')
               item = QtWidgets.QTableWidgetItem()
               self.sharesTable.setItem(previousRow, previousColumn, item)
               item.setText('')
            elif folioNO in filterDict.keys():
                item = QtWidgets.QTableWidgetItem()
                item.setFlags(~QtCore.Qt.ItemIsEditable)
                self.sharesTable.setItem(previousRow, previousColumn+1, item)
                item.setText(str(filterDict[folioNO][1]))
            elif folioNO=='':
                pass
            else:
                item = QtWidgets.QTableWidgetItem()
                item.setFlags(~QtCore.Qt.ItemIsEditable)
                self.sharesTable.setItem(previousRow, previousColumn+1, item)
                item.setText('')
                item = QtWidgets.QTableWidgetItem()
                self.sharesTable.setItem(previousRow, previousColumn, item)
                item.setText('')
                QtWidgets.QMessageBox.warning(self, 'Invalid Folio', "Folio not found. Please add folio before transfers")
                  
            
        elif previousColumn==1 or previousColumn==14:
            try:
                activeCell = self.sharesTable.item(previousRow, previousColumn)
                if activeCell is not None and activeCell.text() != '':
                    entered_date = datetime.datetime.strptime(activeCell.text(),'%d/%m/%Y')
                    if previousColumn==14 and self.sharesTable.item(previousRow, 1).text()!='':
                        if entered_date<datetime.datetime.strptime(self.sharesTable.item(previousRow, 1).text(),'%d/%m/%Y'):
                            QtWidgets.QMessageBox.warning(self, 'Invalid Date', "Transfer date cannot be earlier than allotment date")
                            item = QtWidgets.QTableWidgetItem()
                            self.sharesTable.setItem(previousRow, previousColumn, item)
                            item.setText('')
            except Exception as e:
                QtWidgets.QMessageBox.warning(self, 'Invalid Date', "Please use dates in dd/mm/yyyy format")
            


    def saveData(self):
        if self.preventSave:
            QtWidgets.QMessageBox.warning(self, 'InValid Entries', "Share Value should not be negetive. Please check and try again.")
        else:
            self.deleteOld()
            self.totalShares.setText(self.sharesTable.item(self.sharesTable.rowCount()-1, 20).text())
            personalInfo = [self.CIN, self.shareClass.text().upper(),self.nominalValue.text(),self.totalShares.text()]
            for x in range(self.personalInfo.rowCount()):
                try:
                    personalInfo.append(self.personalInfo.item(x,0).text())
                except:
                    personalInfo.append('')
            db.MGT1PER(personalInfo)
            sharesDetails=[]
            for x in range(self.sharesTable.rowCount()):
                    m=[self.CIN, self.shareClass.text().upper(),self.personalInfo.item(0,0).text()]
                    for y in range(self.sharesTable.columnCount()):
                        try:
                            m.append(self.sharesTable.item(x,y).text())
                        except:
                            m.append('')
                    sharesDetails.append(tuple(m))
            db.MGT1SH(sharesDetails)
            QtWidgets.QMessageBox.information(self, 'Information saved', f"{self.personalInfo.item(1,0).text()} have been added to Register")
            self.updateIndex()
            self.openIndex(True)        


                    
            
    def deleteOld(self):
        conn = sqlite3.connect(self.registerPath)
        cur = conn.cursor()
        self.deleteCIN = self.CIN
        try:
            cur.execute(f'DELETE FROM MGT1SH WHERE company_cin = {repr(self.CIN)} AND class = {repr(self.shareClass.text())} AND folio_no = {repr(self.personalInfo.item(0,0).text())}')
            cur.execute(f'DELETE FROM MGT1PERSONAL WHERE company_cin = {repr(self.CIN)} AND class = {repr(self.shareClass.text())} AND folio_no = {repr(self.personalInfo.item(0,0).text())}')
        except:
            pass
        cur.close()
        conn.commit()
        conn.close()              
                        
    def getdata(self):
        CurrentSelection = self.Nameentry.currentText()
        self.Masterdata = self.cur.execute(f'SELECT * from Masterdata WHERE company_name = "{CurrentSelection}"').fetchall()[0]
        self.registeredaddress.setText(self.Masterdata[11])
        
def clearLayout(layout):
    while layout.count():
        child = layout.takeAt(0)
        if child.widget() is not None:
            child.widget().deleteLater()
        elif child.layout() is not None:
            clearLayout(child.layout())

class ValidatedItemDelegate(QtWidgets.QStyledItemDelegate):
    def createEditor(self, widget, option, index):
        sharesTable = widget.parent()
        if not index.isValid():
            return 0
        if index.column() == 0: #only on the cells in the first column
            editor = QtWidgets.QLineEdit(widget)
            validator = QtGui.QRegExpValidator(QtCore.QRegExp("\d{11}"), editor)
            editor.setValidator(validator)
            return editor
        elif index.column()==2 or index.column()==15:
            editor = QtWidgets.QLineEdit(widget)
            validator = QtGui.QIntValidator(editor)
            validator.setBottom(0)
            editor.setValidator(validator)
            return editor
        elif index.column()==1 or index.column()==14:
            editor = QtWidgets.QLineEdit(widget)
            validator = QtGui.QRegExpValidator(QtCore.QRegExp("(0[1-9]|[12][0-9]|3[01])/(0[1-9]|[1][0-2])/(19[0-9][0-9]|20[0-9][0-9])"), editor)
            editor.setValidator(validator)
            return editor
        return super(ValidatedItemDelegate, self).createEditor(widget, option, index)
