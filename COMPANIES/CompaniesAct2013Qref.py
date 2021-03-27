from PySide2 import QtWidgets, QtUiTools,QtCore, QtGui
import sys
import os
sys.path.append(os.path.abspath(os.path.join('..')))
import HomePage
from functions import UpdateCompaniesAct, getCompaniesAct,pyside_dynamic


class Ui(QtWidgets.QWidget):
    def __init__(self,isSidebar=False):
        super(Ui, self).__init__()
        if isSidebar:
            pyside_dynamic.loadUi('Resources/ui/CompaniesActToolBox.ui',self)
        else:
            pyside_dynamic.loadUi('Resources/ui/CompaniesActQuickRef.ui',self)
        self.isSidebar = isSidebar
        self.ClauseInput = self.findChild(QtWidgets.QLineEdit, 'ClauseInput')
        self.SectionInput = self.findChild(QtWidgets.QLineEdit, 'SectionInput')
        self.ProvisoInput = self.findChild(QtWidgets.QLineEdit, 'ProvisoInput')
        self.SubSectionInput = self.findChild(QtWidgets.QLineEdit, 'SubSectionInput')
        self.ExplanationInput = self.findChild(QtWidgets.QLineEdit, 'ExplanationInput')
        self.TitleOutput = self.findChild(QtWidgets.QLineEdit, 'TitleOutput')
        self.SectionOutpit = self.findChild(QtWidgets.QTextBrowser, 'SectionOutpit')
        self.Footnote = self.findChild(QtWidgets.QTextBrowser, 'Footnote')
        self.RB_Updated = self.findChild(QtWidgets.QRadioButton, 'RB_Updated')
        self.RB_Quick = self.findChild(QtWidgets.QRadioButton, 'RB_Quick')
        self.UpdateDb = self.findChild(QtWidgets.QPushButton, 'UpdateDb')
        self.UpdateDb.clicked.connect(self.updateMessage)
        self.Search = self.findChild(QtWidgets.QPushButton, 'Search')
        self.Search.clicked.connect(self.getSection)
        #self.show()



    def updateMessage(self):
        self.Message = QtWidgets.QMessageBox(self)
        self.Message.setIcon(QtWidgets.QMessageBox.Information)
        self.Message.setText("During updating the program would be unresponsive. Please wait till the datatbase updates")
        self.Message.setWindowTitle('Updating')
        self.Wait = QtWidgets.QPushButton()
        self.Wait.setText('I will wait')
        self.Wait.clicked.connect(self.UpdateDatabase)
        self.NoTime = QtWidgets.QPushButton()
        self.NoTime.setText('I prefer not to')
        self.NoTime.clicked.connect(self.MessageClose)
        self.Message.addButton(self.Wait, QtWidgets.QMessageBox.YesRole)
        self.Message.addButton(self.NoTime, QtWidgets.QMessageBox.NoRole)
        self.Message.show()
        
        

    def UpdateDatabase(self):
        UpdateCompaniesAct.refreshDataBase()
        self.Message.close()

    def MessageClose(self):
        self.Message.close()
        
        
    def getSection(self):
        Section = self.SectionInput.text()
        SubSection = self.SubSectionInput.text()
        Clause = self.ClauseInput.text()
        Proviso = self.ProvisoInput.text()
        Explanation = self.ExplanationInput.text()
        if self.RB_Updated.isChecked():
            self.SectionData = getCompaniesAct.WhatIs(Section=Section,
                                    SubSection=SubSection,
                                    Clause=Clause,
                                    Proviso=Proviso,
                                    Explanation=Explanation,json=True,debug=True)
        elif self.RB_Quick.isChecked():
            self.SectionData = getCompaniesAct.findSection(Section=Section,
                                    SubSection=SubSection,
                                    Clause=Clause,
                                    Proviso=Proviso,
                                    Explanation=Explanation,json=True)
        if self.SectionData['Status']=='Success':
            if self.isSidebar:
                title = self.SectionData['result']['Section Title'][:27]+'...'
                self.TitleOutput.setText(title)
                self.TitleOutput.setToolTip(self.SectionData['result']['Section Title'])
            else:
                self.TitleOutput.setText(self.SectionData['result']['Section Title'])
            self.SectionOutpit.setText(self.SectionData['result']['Section Text'])
            if self.RB_Updated.isChecked():
                if len(self.SectionData['result']['FootNote'])>10:
                    self.Footnote.setText(self.SectionData['result']['FootNote'])
                else:
                    self.Footnote.setText('No Footnote')
        elif self.SectionData['Status']=='Failed':
            self.Error_Message()
            
        elif self.SectionData['Status']=='Failed/QSR':
            self.Error_Message()

    def Error_Message(self):
        self.ErrorMessage = QtWidgets.QMessageBox(self)
        self.ErrorMessage.setIcon(QtWidgets.QMessageBox.Information)
        self.ErrorMessage.setText(self.SectionData['Message'])
        self.ErrorMessage.setWindowTitle('Error!!')
        self.Ido = QtWidgets.QPushButton()
        self.Ido.setText('Yes I do')
        self.Ido.clicked.connect(self.accept)
        self.idont = QtWidgets.QPushButton()
        self.idont.setText("No I don't")
        self.idont.clicked.connect(self.reject)
        self.ErrorMessage.addButton(self.Ido, QtWidgets.QMessageBox.YesRole)
        self.ErrorMessage.addButton(self.idont, QtWidgets.QMessageBox.NoRole)
        self.ErrorMessage.show()
        

    def QuickSearch(self):
        self.dlg = QtWidgets.QDialog(self)
        self.dlg.resize(300, 200)
        self.dlg.setWindowTitle("Would you like to do a Quick Search?")
        self.dlg.gridLayout = QtWidgets.QGridLayout(self.dlg)
        self.dlg.gridLayout.setObjectName("gridLayout")
        self.dlg.label = QtWidgets.QLabel(self.dlg)
        self.dlg.label.setMaximumSize(QtCore.QSize(16777215, 12))
        self.dlg.label.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.dlg.label.setObjectName("label")
        self.dlg.label.setText(self.SectionData['Message'])
        self.dlg.buttonBox = QtWidgets.QDialogButtonBox(self.dlg)
        self.dlg.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.dlg.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.dlg.buttonBox.setObjectName("buttonBox")
        self.dlg.gridLayout.addWidget(self.dlg.buttonBox, x+2, 2, 1, 1)
        self.dlg.buttonBox.accepted.connect(self.accept)
        self.dlg.buttonBox.rejected.connect(self.reject)
        self.dlg.show()

    
    def accept(self):
        self.ErrorMessage.close()
        Section = self.SectionInput.text()
        SubSection = self.SubSectionInput.text()
        Clause = self.ClauseInput.text()
        Proviso = self.ProvisoInput.text()
        Explanation = self.ExplanationInput.text()
        self.SectionData = getCompaniesAct.findSection(Section=Section,
                                SubSection=SubSection,
                                Clause=Clause,
                                Proviso=Proviso,
                                Explanation=Explanation,json=True)
        if self.SectionData['Status']=='Success':
            self.SectionTitleShow.setText(self.SectionData['result']['Section Title'])
            self.textBrowser.setText(self.SectionData['result']['Section Text'])
        elif self.SectionData['Status']=='Failed':
            self.QuickMessage = QtWidgets.QMessageBox(self)
            self.QuickMessage.setIcon(QtWidgets.QMessageBox.Warning)
            self.QuickMessage.setText(self.SectionData['Message'])
            self.QuickMessage.setWindowTitle('Error!!')
            self.OkK = QtWidgets.QPushButton()
            self.OkK.setText('Ok')
            self.OkK.clicked.connect(self.backtoCA)
            self.QuickMessage.addButton(self.OkK, QtWidgets.QMessageBox.YesRole)
            self.QuickMessage.show()

    def backtoCA(self):
        self.QuickMessage.close()
        
    def reject(self):
        self.ErrorMessage.close()


