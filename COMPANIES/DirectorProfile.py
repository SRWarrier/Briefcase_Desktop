from PySide2 import QtWidgets, QtUiTools,QtCore, QtGui
import sys
import HomePage
import os
import numpy as np
from PIL import Image
from functions import directorProfile
from functions import pyside_dynamic
from functions.Gdrive import Gdrive
import requests_html
import sqlite3

session = requests_html.HTMLSession()

class Ui(QtWidgets.QWidget):
    def __init__(self):
        super(Ui, self).__init__()
        pyside_dynamic.loadUi('../Resources/ui/DirectorProfile.ui',self)
        self.DINField = self.findChild(QtWidgets.QLineEdit, 'DINField')
        self.NameField = self.findChild(QtWidgets.QLineEdit, 'NameField')
        self.FatherName = self.findChild(QtWidgets.QLineEdit, 'FatherName')
        self.DOB = self.findChild(QtWidgets.QLineEdit, 'DOB')
        self.AssociatedCompany_2 = self.findChild(QtWidgets.QTableWidget, 'AssociatedCompany_2')
        self.AssociatedCompany_2.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.AssociatedCompany_2.customContextMenuRequested.connect(self.handleHeaderMenu_client2)
        self.PersonalTable = self.findChild(QtWidgets.QTableWidget, 'PersonalTable')
        self.PersonalTable.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.PersonalTable.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.PersonalTable.customContextMenuRequested.connect(self.handleHeaderMenu_client)
        self.Prefill = self.findChild(QtWidgets.QPushButton, 'Prefill')
        self.Prefill.clicked.connect(self.getData)
        self.show()


    def getData(self):
        if self.DINField.text()!='' and self.DINField.text().isnumeric() and len(self.DINField.text())==8:
            self.Profile =   directorProfile.profileDirector(DIN =  self.DINField.text())
            print(self.Profile)
        elif self.NameField.text()!='':
            namestring = self.NameField.text()+','+self.FatherName.text()+','+self.DOB.text()
            self.Profile =   directorProfile.profileDirector(Name =  namestring)
        if isinstance(self.Profile,str):
            QtWidgets.QMessageBox.critical(self, "DIN Error", self.Profile)
        elif self.Profile['Status']=='Failed':
            QtWidgets.QMessageBox.critical(self, "DIN Error", "Data not found")
        elif self.Profile['Status']=='Selection':
            self.selection(self.Profile)
        else:
            self.PersonalTable.setRowCount(len(self.Profile['Personal']))
            self.PersonalTable.setColumnCount(2)
            THeader = list(self.Profile['Personal'].keys())
            TValues = list(self.Profile['Personal'].values())
            for x in range(len(self.Profile['Personal'])):
                item = QtWidgets.QTableWidgetItem()
                self.PersonalTable.setItem(x, 0, item)
                item.setText(str(THeader[x].replace('_',' ').title()))
                item.setFlags(QtCore.Qt.ItemIsSelectable)
                item = QtWidgets.QTableWidgetItem()
                self.PersonalTable.setItem(x, 1, item)
                item.setText(str(TValues[x]))
                item.setFlags(QtCore.Qt.ItemIsSelectable)
            #self.PersonalTable.resizeRowsToContents()
            self.PersonalTable.resizeColumnsToContents()
            self.AssociatedCompany_2.setRowCount(len(self.Profile['Companies']))
            for x in range(len(self.Profile['Companies'])):
                        CompInfo = list(self.Profile['Companies'][x+1].values())
                        for y in range(len(self.Profile['Companies'][x+1])):
                            item = QtWidgets.QTableWidgetItem()
                            item.setFlags(QtCore.Qt.ItemIsSelectable)
                            self.AssociatedCompany_2.setItem(x, y, item)
                            item.setText(str(CompInfo[y]))
            self.AssociatedCompany_2.resizeRowsToContents()
            self.AssociatedCompany_2.resizeColumnsToContents()

    def handleHeaderMenu_client(self, pos):
        x,y = pos.x(), pos.y()
        it = self.PersonalTable.indexAt(pos)
        self.selectedrow = it.row()
        self.selectedCol = it.column()
        if it is None: return
        menu = QtWidgets.QMenu()
        edit = menu.addAction("Copy")
        action = menu.exec_(self.PersonalTable.viewport().mapToGlobal(pos))
        if action == edit:
            clipboard = QtWidgets.QApplication.clipboard()
            clipboard.clear(mode=clipboard.Clipboard )
            clipboard.setText(self.PersonalTable.item(self.selectedrow,self.selectedCol).text(), mode=clipboard.Clipboard)

    def handleHeaderMenu_client2(self, pos):
        x,y = pos.x(), pos.y()
        it = self.AssociatedCompany_2.indexAt(pos)
        self.selectedrow = it.row()
        self.selectedCol = it.column()
        if it is None: return
        menu = QtWidgets.QMenu()
        edit = menu.addAction("Copy")
        action = menu.exec_(self.AssociatedCompany_2.viewport().mapToGlobal(pos))
        if action == edit:
            clipboard = QtWidgets.QApplication.clipboard()
            clipboard.clear(mode=clipboard.Clipboard )
            clipboard.setText(self.AssociatedCompany_2.item(self.selectedrow,self.selectedCol).text(), mode=clipboard.Clipboard)

    def selection(self, data):
        self.dlg = QtWidgets.QDialog()
        self.dlg.resize(471, 362)
        self.dlg.setStyleSheet("background-color: rgb(255, 255, 255);\n"
    "color: rgb(0, 0, 0);")
        self.dlg.setWindowTitle("Select a Company")
        self.dlg.gridLayout = QtWidgets.QGridLayout(self.dlg)
        self.dlg.gridLayout.setObjectName("gridLayout")
        self.dlg.label = QtWidgets.QLabel(self.dlg)
        self.dlg.label.setMaximumSize(QtCore.QSize(16777215, 12))
        self.dlg.label.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.dlg.label.setObjectName("label")
        self.dlg.label.setText("Multiple Companies Found!")
        self.dlg.gridLayout.addWidget(self.dlg.label, 0, 2, 1, 1)
        ButtonGroup=QtWidgets.QButtonGroup(self.dlg)
        for x in range(len(data['data'])):
            Name=data['data'][x+1]['NAME']
            FName = data['data'][x+1]['FATHER NAME']
            Dob = data['data'][x+1]['DOB']
            Button= QtWidgets.QRadioButton(f"{Name} (Father: {FName} - DOB: {Dob})")
            ButtonGroup.addButton(Button)
            self.dlg.gridLayout.addWidget(Button,x+1, 2, 1, 1)
        ButtonGroup.buttonClicked.connect(self.Choice)
        self.dlg.buttonBox = QtWidgets.QDialogButtonBox(self.dlg)
        self.dlg.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.dlg.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.dlg.buttonBox.setObjectName("buttonBox")
        self.dlg.gridLayout.addWidget(self.dlg.buttonBox, x+2, 2, 1, 1)
        self.dlg.buttonBox.accepted.connect(self.accept)
        self.dlg.buttonBox.rejected.connect(self.reject)
        self.dlg.show()

    def Choice(self,selected):
        for x in range(len(self.Profile['data'])):
            if self.Profile['data'][x+1]['NAME'].strip() == selected.text().split('(')[0].strip():
                self.dir_choice = self.Profile['data'][x+1]['DIN']

    def accept(self):
        self.dlg.close()
        print(self.dir_choice)
        self.DINField.setText(self.dir_choice)
        self.Prefill.click()

    def reject(self):
        self.dlg.close()
                                           
                                           
            
         
                
