from PySide2 import QtWidgets, QtUiTools,QtCore, QtGui
import sys
import os
sys.path.append(os.path.abspath(os.path.join('..')))
import HomePage
from functions import Database_Manager as db
from functions import pyside_dynamic, KeyWordCompletor
import re
import json
import pickle
import sqlite3


class Ui(QtWidgets.QWidget):
    def __init__(self,ID):
        super(Ui, self).__init__()
        pyside_dynamic.loadUi('Resources/ui/EditResolution.ui',self)
        with open('Config','rb') as f:
            Config = pickle.loads(f.read())
            f.close()
        self.resolutionspath = os.path.join(Config['Database'],'Resolutions.db')
        try:
            #ResolutionsFile
            self.conn = sqlite3.connect(self.resolutionspath)
            self.cur = self.conn.cursor()
            self.ResolutionData = self.cur.execute(f'SELECT * from Resolutions WHERE ID = "{ID}"').fetchall()[0]
            self.DescriptionInput = self.findChild(QtWidgets.QLineEdit, 'DescriptionInput')
            self.NarrationInput = self.findChild(QtWidgets.QTextEdit, 'NarrationInput')
            #KeyWordCompletor.KeywordComplete(self.NarrationInput)
            self.TitleInput = self.findChild(QtWidgets.QLineEdit, 'TitleInput')
            self.Summary = self.findChild(QtWidgets.QTextEdit, 'summary')
            self.ResolutionInput = self.findChild(QtWidgets.QTextEdit, 'ResolutionInput')
            #KeyWordCompletor.KeywordComplete(self.ResolutionInput )
            self.AddVariables = self.findChild(QtWidgets.QPushButton, 'AddVariables')
            self.AddVariables.clicked.connect(self.AddVariableField)
            #DbFile
            self.DescriptionInput.setText(self.ResolutionData[1])
            self.category.setCurrentText(self.ResolutionData[3])
            self.TitleInput.setText(self.ResolutionData[2])
            self.Summary.setText(self.ResolutionData[4])
            self.NarrationInput.setText(self.ResolutionData[5].replace('\\n','\n'))
            self.ResolutionInput.setText(self.ResolutionData[6].replace('\\n','\n'))
        except:
            ErrorMessage =  QtWidgets.QMessageBox()
            ErrorMessage.setIcon(QtWidgets.QMessageBox.Warning)
            ErrorMessage.setText("No Resolutions Found in Database")
            ErrorMessage.setInformativeText("Please refer this to admin and add resolutions")
            ErrorMessage.setWindowTitle("Resolutions Not Found")
            ErrorMessage.setStandardButtons(QtWidgets.QMessageBox.Ok)
            ErrorMessage.buttonClicked.connect(self.GotoDashBoard)
            ErrorMessage.show()
        self.ParamDict = {}
        for param in eval(self.ResolutionData[7]):
            self.ParamDict[param[0]]=param[1]
       


    def GotoDashBoard(self):
        pass 
        
            
    def addRes(self):
        DESCRIPTION = self.DescriptionInput.text()
        SUMMARY   = self.Summary.toPlainText()
        CATEGORY = self.category.currentText()
        NARRATION = self.NarrationInput.toPlainText().replace('\\n','\n')
        TITLE = self.TitleInput.text()
        RESOLUTION = self.ResolutionInput.toPlainText().replace('\\n','\n')
        VaraibleTableValues=[]
        for row in range(self.AddVariableWindow.InputTable.rowCount()):
            FieldName = self.AddVariableWindow.InputTable.item(row, 0).text()
            FieldType = self.AddVariableWindow.InputTable.cellWidget(row, 1).currentText()
            self.AddVariableWindow.InputTable.cellWidget(row, 1).setStyleSheet("background-color: rgb(255,255,255);")
            if not FieldType in self.combo_box_options:
                self.InputError = QtWidgets.QMessageBox(self.AddVariableWindow)
                self.InputError.setWindowTitle("Invalid Selection")
                self.InputError.setText('You have selected an inavld field type. Please select again')
                self.InputError.setStandardButtons(QtWidgets.QMessageBox.Ok)
                self.InputError.buttonClicked.connect(self.closeMsg)     
                self.InputError.show()
                self.AddVariableWindow.InputTable.cellWidget(row, 1).setStyleSheet("background-color: rgb(190,45,77);")
                return None
            VaraibleTableValues.append((FieldName,FieldType))
        jsonedFields = json.dumps(VaraibleTableValues)
        ResolutionDict = {'DESCRIPTION':DESCRIPTION,'TITLE':TITLE,'CATEGORY':CATEGORY,'SUMMARY':SUMMARY,'NARRATION':NARRATION,'RESOLUTION':RESOLUTION,'FIELDS':jsonedFields}
        isSuccess=db.UpdateResolution(ResolutionDict)
        if isSuccess=='Success':
            Message = QtWidgets.QMessageBox(self.AddVariableWindow)
            Message.setWindowTitle("Success!!")
            Message.setText(self.TitleInput.text()+' has been successfully added to Drafts.')
            Message.setStandardButtons(QtWidgets.QMessageBox.Ok)
            #Message.buttonClicked.connect(self.CloseMessage)
            self.AddVariableWindow.hide()
            Message.show()
        elif isSuccess=='Duplicate':
            Message = QtWidgets.QMessageBox(self.AddVariableWindow)
            Message.setWindowTitle("Duplicate!!")
            Message.setText(self.TitleInput.text()+' is already registered in Draft. Either use Edit Resolution or rename Title')
            Message.setStandardButtons(QtWidgets.QMessageBox.Ok)
            Message.buttonClicked.connect(self.backtoEditor)
            Message.show()
            
                            
        
        
    def AddVariableField(self):
        NarrationText = self.NarrationInput.toPlainText()
        VariablesList = []
        VariablesList= VariablesList+re.findall(r"\{(\w+)\}",NarrationText)
        ResolutionText = self.ResolutionInput.toPlainText()
        VariablesList= VariablesList+re.findall(r"\{(\w+)\}",ResolutionText)
        VariablesList.reverse()
        self.AddVariableWindow = QtWidgets.QWidget()
        pyside_dynamic.loadUi('Resources/ui/InputEditor.ui', self.AddVariableWindow)
        self.AddVariableWindow.Title = self.AddVariableWindow.findChild(QtWidgets.QLabel, 'Title')
        self.AddVariableWindow.AddResolution = self.AddVariableWindow.findChild(QtWidgets.QPushButton, 'AddResolution')
        self.AddVariableWindow.AddResolution.clicked.connect(self.addRes)
        self.AddVariableWindow.BacktoEditor = self.AddVariableWindow.findChild(QtWidgets.QPushButton, 'BacktoEditor')
        self.AddVariableWindow.BacktoEditor.clicked.connect(self.backtoEditor)
        self.AddVariableWindow.Title.setText('Input Fields for Resolution')
        self.AddVariableWindow.InputTable = self.AddVariableWindow.findChild(QtWidgets.QTableWidget, 'InputTable')
        self.AddVariableWindow.InputTable.setColumnCount(2)
        self.AddVariableWindow.InputTable.setHorizontalHeaderLabels(['Input Field Name','Field Type'])
        self.VariablesList = list(set(VariablesList))
        self.AddVariableWindow.InputTable.setRowCount(len(self.VariablesList))
        header = self.AddVariableWindow.InputTable.horizontalHeader()       
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        self.combo_box_options = sorted(["Text Input","Date Input",'Time Input','DIN Input','CIN Input','Authorization'])
        for index in range(len(self.VariablesList)):
            var = self.VariablesList[index].replace('_',' ').upper()
            item1 = QtWidgets.QTableWidgetItem(var)
            self.AddVariableWindow.InputTable.setItem(index,0,item1)
            combo = QtWidgets.QComboBox()
            combo.setEditable(True)
            for t in self.combo_box_options:
                combo.addItem(t)
            try:
                combo.setCurrentText(self.ParamDict[var])
            except:
                pass
            self.AddVariableWindow.InputTable.setCellWidget(index,1,combo)
        self.AddVariableWindow.AddRow = self.AddVariableWindow.findChild(QtWidgets.QPushButton, 'AddRow')
        self.AddVariableWindow.AddRow.clicked.connect(self.AddRowFn)
        self.AddVariableWindow.show()

    def backtoEditor(self):
        self.AddVariableWindow.hide()


    def AddRowFn(self):
        rowPosition = self.AddVariableWindow.InputTable.rowCount()
        self.AddVariableWindow.InputTable.insertRow(rowPosition)
        item = QtWidgets.QTableWidgetItem('')
        self.AddVariableWindow.InputTable.setItem(rowPosition,0,item)
        combo = QtWidgets.QComboBox()
        combo.setEditable(True)
        for t in self.combo_box_options:
                combo.addItem(t)
        self.AddVariableWindow.InputTable.setCellWidget(rowPosition,1,combo)

    def closeMsg(self):
            self.InputError.close()
            
    
