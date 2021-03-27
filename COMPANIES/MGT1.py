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


session = requests_html.HTMLSession()

class Ui(QtWidgets.QWidget):
    def __init__(self):
        super(Ui, self).__init__()
        pyside_dynamic.loadUi('Resources/ui/MGT1.ui',self)
        self.dbfilepath = 'Database/C3_DataBase.db'
        self.Nameentry = self.findChild(QtWidgets.QComboBox, 'CompanySelect')
        self.conn = sqlite3.connect(self.dbfilepath)
        self.cur = self.conn.cursor()
        CompanyListdb = self.cur.execute('SELECT "company_name" from Masterdata').fetchall()
        CompanyList=['']
        for item in CompanyListdb:
            CompanyList.append(item[0])
        self.Nameentry.addItems(CompanyList)
        self.Nameentry.activated.connect(self.getdata)
        self.ExportToPDF.clicked.connect(self.handlePaintRequest)
        self.registeredaddress = self.findChild(QtWidgets.QLineEdit, 'RegisteredOffice')

    def printPDF(self):
        print("Printing")
        fn, _ = QtWidgets.QFileDialog.getSaveFileName(self, 'Export PDF', None, 'PDF files (.pdf);;All Files()')
        if fn != '':
            if QtCore.QFileInfo(fn).suffix() == "" : fn += '.pdf'
            printer = QPrinter(QPrinter.HighResolution)
            printer.setOutputFormat(QPrinter.PdfFormat)
            printer.setPageSize(QPrinter.A6)
            printer.setOutputFileName(fn)
##            pixmap = QtGui.QPixmap.grabWidget(self.Register).scaled(
##            printer.pageRect(QPrinter.DevicePixel).size().toSize(),
##            QtCore.Qt.KeepAspectRatio)
            pixmap = QtGui.QPixmap()
            painter = QtGui.QPainter(printer)
            printer.setFullPage(True)
            printer.setOrientation(QPrinter.Landscape)
            self.Title.render(pixmap)
            self.subtitle.render(pixmap)
            self.info.render(pixmap)
            self.PersonalInfo.render(pixmap)
            painter.drawPixmap(0, 0, pixmap)
            pixmap.save("Test.png", 'PNG', 100)
            painter.end()


    def handlePaintRequest(self):
        print("Printing")
        fn, _ = QtWidgets.QFileDialog.getSaveFileName(self, 'Export PDF', None, 'PDF files (.pdf);;All Files()')
        if fn != '':
            if QtCore.QFileInfo(fn).suffix() == "" : fn += '.pdf'
            printer = QPrinter(QPrinter.HighResolution)
            printer.setOutputFormat(QPrinter.PdfFormat)
            printer.setPageSize(QPrinter.A4)
            printer.setOrientation(QPrinter.Landscape)
            printer.setOutputFileName(fn)
            printer.setFullPage(True)
            document = QtGui.QTextDocument()
            cursor = QtGui.QTextCursor(document)
            model = self.personalInfo
            table = cursor.insertTable(
                model.rowCount(), model.columnCount()+1)
            for row in range(model.rowCount()):
                label = model.verticalHeaderItem(row).text()
                for column in range(model.columnCount()):
                    
                        cursor.insertText(label)
                        cursor.movePosition(QtGui.QTextCursor.NextCell)
                        try:
                            cursor.insertText(model.item(row, column).text())
                        except:
                            cursor.insertText('')
                        cursor.movePosition(QtGui.QTextCursor.NextCell)
            document.print_(printer)

    def getdata(self):
        CurrentSelection = self.Nameentry.currentText()
        self.Masterdata = self.cur.execute(f'SELECT * from Masterdata WHERE company_name = "{CurrentSelection}"').fetchall()[0]
        self.registeredaddress.setText(self.Masterdata[11])
        
