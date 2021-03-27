from PySide2 import QtWidgets, QtUiTools,QtCore, QtGui
import sys
import os
from functions import Database_Manager as db
from functions import pyside_dynamic
from functions import getMasterdata




class Ui(QtWidgets.QWidget):
    def __init__(self):
        super(Ui, self).__init__()
        

        
    def isProgrammer(self,isProg=False):
        self.Name = self.findChild(QtWidgets.QLineEdit, 'Name')
        self.Username = self.findChild(QtWidgets.QLineEdit, 'Username')
        self.RoleSelect = self.findChild(QtWidgets.QComboBox, 'RoleSelect')
        if isProg:
            self.RoleSelect.clear()
            self.RoleSelect.addItem("Administrator")
        self.AddUser.clicked.connect(self.Addtodb)
        self.show()

    def Addtodb(self):
        print("yes")
        Name = self.Name.text()
        UserName = self.Username.text()
        Role = self.RoleSelect.currentText()
        UserDict = {'USERNAME':UserName,'PASSWORD':'','ROLE':Role,'NAME':Name,'LASTLOGIN':''}
        Status = db.AddUser(UserDict)
        if Status=='Success':
            self.Message = QtWidgets.QMessageBox()
            self.Message.setIcon(QtWidgets.QMessageBox.Information)
            self.Message.setText(f'{Name} has been added as new {Role} User')
            self.Message.setWindowTitle('Success!!')
            self.Ido = QtWidgets.QPushButton()
            self.Ido.setText('Ok')
            self.Ido.clicked.connect(self.accept)
            self.Message.addButton(self.Ido, QtWidgets.QMessageBox.YesRole)
            self.Message.show()
        elif Status == 'Duplicate':
            self.Message = QtWidgets.QMessageBox()
            self.Message.setIcon(QtWidgets.QMessageBox.Information)
            self.Message.setText('Duplicate User. Please retry with another name')
            self.Message.setWindowTitle('Alert!!')
            self.Ido = QtWidgets.QPushButton()
            self.Ido.setText('Ok')
            self.Ido.clicked.connect(self.retry)
            self.Message.addButton(self.Ido, QtWidgets.QMessageBox.YesRole)
            self.Message.show()
        else:
            print("error")
            

    def accept(self):
        self.Message.close()
        self.close()

    def retry(self):
        self.Message.close()
