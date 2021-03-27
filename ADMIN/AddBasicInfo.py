from PySide2 import QtWidgets, QtUiTools,QtCore, QtGui
import sys
import os
sys.path.append(os.path.abspath(os.path.join('..')))
import HomePage
from functions import Database_Manager as db
from functions import pyside_dynamic, KeyWordCompletor
import re
import json


class Ui(QtWidgets.QWidget):
    def __init__(self):
        super(Ui, self).__init__()
        pyside_dynamic.loadUi('Resources/ui/AddBasicInfo.ui',self)
        self.savebutton.clicked.connect(self.saveInfo)
        

    def saveInfo(self):
        Name = self.Name.text()
        Address = self.Address.text()
        Pan = self.Pan.text()
        Gstin = self.Gstin.text()
        Bank = self.Bank.text()
        Branch = self.Branch.text()
        AccountNo = self.Account.text()
        Ifsc = self.Ifsc.text()
        Micr = self.Micr.text()
        self.DataDict = [Name,Address,Pan,Gstin,Bank,Branch,AccountNo,Ifsc,Micr]
        self.Message()
            

    def Message(self):
        Message = QtWidgets.QMessageBox(self)
        Message.setWindowTitle("Information")
        Message.setText('Any existing information will be replaced. Do you wnat to continue?')
        Message.setModal(False)
        self.doneButtion = QtWidgets.QPushButton()
        self.doneButtion.setText('Yes')
        self.doneButtion.clicked.connect(self.done)
        Message.addButton(self.doneButtion, QtWidgets.QMessageBox.YesRole)
        Message.show()

    def done(self):
        db.basicInfo(self.DataDict)
