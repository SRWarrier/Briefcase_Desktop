from PySide2 import QtWidgets, QtUiTools,QtCore, QtGui
import sys
import os
sys.path.append(os.path.abspath(os.path.join('..')))
import HomePage
import pickle
from functions import Database_Manager as db
from functions import ExportToDoc, pyside_dynamic
from functions import getDirName, prefillDIN
import sqlite3


class Ui(QtWidgets.QWidget):
    def __init__(self):
        super(Ui, self).__init__()
        pyside_dynamic.loadUi('../Resources/ui/QuickResolution.ui',self)
        with open('Config','rb') as f:
            Config = pickle.loads(f.read())
            f.close()
        self.dbfilepath = os.path.join(Config['Database'],'C3_DataBase.db')
        self.resolutionspath = os.path.join(Config['Database'],'Resolutions.db')
        self.adjustSize()
        self.AuthorizedContainer = []
        self.conn = sqlite3.connect(self.resolutionspath)
        self.cur = self.conn.cursor()
        self.Resolution = self.findChild(QtWidgets.QComboBox, 'ResolutionType')
        try:
            ResolutionListdb = self.cur.execute('SELECT "DESCRIPTION" from Resolutions').fetchall()
        except:
            ErrorMessage =  QtWidgets.QMessageBox()
            ErrorMessage.setIcon(QtWidgets.QMessageBox.Warning)
            ErrorMessage.setText("No Resolutions Found in Database")
            ErrorMessage.setInformativeText("Please refer this to admin and add resolutions")
            ErrorMessage.setWindowTitle("Resolutions Not Found")
            ErrorMessage.setStandardButtons(QtWidgets.QMessageBox.Ok)
            ErrorMessage.buttonClicked.connect(self.GotoDashBoard)
            ErrorMessage.show()
            
        ResolutionList=['']
        for item in ResolutionListdb:
            ResolutionList.append(item[0])
        self.Resolution.addItems(ResolutionList)
        self.Resolution.activated.connect(self.getResolution)
        self.InputFieldsShow = self.findChild(QtWidgets.QWidget, 'FieldView')
        self.InputLayout = QtWidgets.QFormLayout()
        self.CompanySelection = self.findChild(QtWidgets.QComboBox, 'CompanySelection')
        self.conn = sqlite3.connect(self.dbfilepath)
        self.cur = self.conn.cursor()
        CompanyListdb = self.cur.execute('SELECT "company_name" from Masterdata').fetchall()
        CompanyList=['']
        for item in CompanyListdb:
            CompanyList.append(item[0])
        self.CompanySelection.addItems(CompanyList)
        self.DateSelection = self.findChild(QtWidgets.QDateEdit, 'DateSelection')
        self.DateSelection.setDateTime(QtCore.QDateTime.currentDateTime())
        self.TimeSelect = self.findChild(QtWidgets.QTimeEdit, 'TimeSelect')
        self.TimeSelect.setTime(QtCore.QTime.currentTime())
        self.VenueSelect = self.findChild(QtWidgets.QLineEdit, 'VenueSelect')
        self.NarrationPreview = self.findChild(QtWidgets.QTextEdit, 'NarrationPreview')
        self.ResolutionPreview = self.findChild(QtWidgets.QTextEdit, 'ResolutionPreview')
        self.GenerateDoc = self.findChild(QtWidgets.QPushButton, 'GenerateDoc')  
        self.GenerateDoc.clicked.connect(self.ExportDocx)

        self.Authorization = self.findChild(QtWidgets.QPushButton, 'Authorizaton')
        self.Authorization.clicked.connect(self.AuthorizationSelection)
        self.show()


    def GotoDashBoard(self):
        pass
    
    def getResolution(self):
        CompanySelection = self.CompanySelection.currentText()
        if CompanySelection=='':
            QtWidgets.QMessageBox.warning(self,'Alert!!','Please select Company')
            self.Resolution.setCurrentIndex(0)
        else:
            CurrentSelection = self.Resolution.currentText()
            #ResolutionsFile
            self.conn = sqlite3.connect(self.resolutionspath)
            self.cur = self.conn.cursor()
            self.ResolutionData = self.cur.execute(f'SELECT * from Resolutions WHERE DESCRIPTION = "{CurrentSelection}"').fetchall()[0]

            #DbFile
            self.conn = sqlite3.connect(self.dbfilepath)
            self.cur = self.conn.cursor()
            self.CompanyData = self.cur.execute(f'SELECT * from Masterdata WHERE "company_name" = "{CompanySelection}"').fetchall()[0]
            self.CompanyCIN = self.CompanyData[0]
            self.SignatoriesData = self.cur.execute(f'SELECT * from Signatories WHERE "company_cin" = "{self.CompanyCIN}"').fetchall()
            self.ResolutionTitle = self.ResolutionData[2]
            self.Fields = self.ResolutionData[7]
            clearLayout(self.InputLayout)
            VariabeLayout = self.variblesView.layout()
            for field in eval(self.Fields):
                if field[1][0].isnumeric():
                    Label = QtWidgets.QLabel()
                    Label.setText(field[0])
                    Label.setObjectName(field[0])
                    if 'din' in field[1].lower():
                        DinField = QtWidgets.QLineEdit()
                        DinField.setValidator(QtGui.QIntValidator())
                        DinField.setMaxLength(8)
                        VarWidget = self.genVariableField(Label,DinField,Prefill='DIN')
                        Label.setObjectName('DinField')
                    elif 'date' in field[1].lower():
                        DateField = QtWidgets.QDateEdit()
                        DateField.setDisplayFormat('dd.MM.yyyy')
                        DateField.setDateTime(QtCore.QDateTime.currentDateTime())
                        VarWidget =self.genVariableField(Label,DateField)
                    elif 'time' in field[1].lower():
                        TimeField = QtWidgets.QTimeEdit()
                        TimeField.setDisplayFormat('h:mm AP')
                        TimeField.setTime(QtCore.QTime.currentTime())
                        VarWidget =self.genVariableField(Label,TimeField)
                    else:
                        TextField = QtWidgets.QLineEdit()
                        self.InputLayout.addRow(Label,TextField)
                        VarWidget =self.genVariableField(Label,TextField)
                    VariabeLayout.addWidget(VarWidget)
            VariabeLayout.addItem(QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding))
            self.NarrationText=(self.ResolutionData[4].replace('\\n','\n'))
            self.ResolutionText=(self.ResolutionData[5].replace('\\n','\n'))
            self.Title.setText(CurrentSelection.upper())
            self.NarrationPreview.setText(self.NarrationText)
            self.ResolutionPreview.setText(self.ResolutionText)


    def AuthorizationSelection(self):
        self.AuthorizationsWindow = QtWidgets.QWidget()
        pyside_dynamic.loadUi('../Resources/ui/AddAuthorizations.ui', self.AuthorizationsWindow)
        self.AuthorizationsWindow.Done = self.AuthorizationsWindow.findChild(QtWidgets.QPushButton, 'Done')
        self.AuthorizationsWindow.Done.clicked.connect(self.groupauthorized)
        self.AuthorizationsWindow.AddOfficer = self.AuthorizationsWindow.findChild(QtWidgets.QPushButton, 'AddOfficer')
        self.AuthorizationsWindow.BacktoRes = self.AuthorizationsWindow.findChild(QtWidgets.QPushButton, 'BacktoRes')
        self.AuthorizationsWindow.selectionWindow = self.AuthorizationsWindow.findChild(QtWidgets.QWidget, 'SelectionWindow')
        layout = QtWidgets.QVBoxLayout()
        Font = QtGui.QFont("Georgia", 11)
        self.DesignationPriority = {"Managing Director": 0, "Wholetime Director": 1, "Director": 2, "Additional Director": 3,
                               "Alternate Director": 4, "Nominee Director": 4,"Company Secretary": 5, "CEO(KMP)" : 6 , 'CFO(KMP)' : 7}
        self.SignatoriesData.sort(key=lambda val: self.DesignationPriority[val[4]])
        self.AuthorizationsWindow.BTGroup = QtWidgets.QButtonGroup()
        for director in self.SignatoriesData:
            item = QtWidgets.QCheckBox(director[2]+', '+director[4])
            item.setFont(Font)
            layout.addWidget(item)
            self.AuthorizationsWindow.BTGroup.addButton(item)
        self.AuthorizationsWindow.BTGroup.setExclusive(False)
        self.AuthorizationsWindow.BTGroup.buttonClicked.connect(self.AddAuthorized)
        self.AuthorizationsWindow.selectionWindow.setLayout(layout)
        self.AuthorizationsWindow.show()
        

    def AddAuthorized(self,button):
        if button.text() not in self.AuthorizedContainer:
            self.AuthorizedContainer.append(button.text())
        elif button.text() in self.AuthorizedContainer:
            self.AuthorizedContainer.remove(button.text())
        else:
            None

    def groupauthorized(self):
        self.AuthorizationsWindow.close()
        self.AuthorizationText = "hello"
        print(self.AuthorizedContainer)


    def PreviewResolution(self):
        CurrentSelection = self.Resolution.currentText()
        self.InputWindow = QtWidgets.QWidget()
        pyside_dynamic.loadUi('../Resources/ui/Preview.ui', self.InputWindow)
        self.InputWindow.NarrationPreview.setText(self.NarrationText)
        self.InputWindow.ResolutionPreview.setText(self.ResolutionText)
        self.InputWindow.show()
        

    def ExportDocx(self):
        self.conn = sqlite3.connect(self.dbfilepath)
        self.cur = self.conn.cursor()
        CompanyInfo = self.cur.execute(f'SELECT * from Masterdata WHERE "company_name" = "{self.CompanySelection.currentText()}"').fetchall()
        meta= self.cur.execute("PRAGMA table_info(Masterdata)").fetchall()
        tableDict = {}
        print(CompanyInfo)
        print(meta)
        loop_count = 0
        for item in meta:
            tableDict[item[1]] = CompanyInfo[0][loop_count]
            loop_count+=1
        Document = ExportToDoc.createDoc()
        Document.letterhead(tableDict['company_name'],tableDict['company_registered_address'],tableDict['company_cin'],tableDict['company_email_id'],tableDict['company_phone'])
        Document.ExtractHeader('Meeting of Board',tableDict['company_name'],tableDict['company_registered_address'],self.DateSelection.date().toPython(),self.TimeSelect.time().toPython())
        Document.ExtractText(self.Title.text(),self.NarrationPreview.toPlainText(),self.ResolutionPreview.toPlainText())
        Document.saveDoc(r'C:\Users\Warrier\Desktop\TestPyQt.docx')
        
    def ErrorWindow(host,Message):
        self.ErrorMessage = QtWidgets.QMessageBox(host)
        self.ErrorMessage.setIcon(QtWidgets.QMessageBox.Information)
        self.ErrorMessage.setText(Message)
        self.ErrorMessage.setWindowTitle('Alert!!')
        self.Ido = QtWidgets.QPushButton()
        self.Ido.setText('Yes I do')
        self.Ido.clicked.connect(self.accept)
        self.ErrorMessage.addButton(self.Ido, QtWidgets.QMessageBox.YesRole)
        self.ErrorMessage.addButton(self.idont, QtWidgets.QMessageBox.NoRole)
        self.ErrorMessage.show()

    def genVariableField(self,label,Widget,Prefill=None):
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(Widget)
        if Prefill=='DIN':
            PrefBtn = QtWidgets.QPushButton()
            PrefBtn.setText("Prefill")
            PrefBtn.clicked.connect(self.prefillDINData)
            layout.addWidget(PrefBtn)
        widget.setLayout(layout)
        return widget
        
    def prefillDINData(self):
        sender = self.sender()
        widget = sender.parent()
        label = widget.findChild(QtWidgets.QLabel).text()
        DIN = widget.findChild(QtWidgets.QLineEdit).text()
        Dinstatus=getDirName.getDirName(DIN)
        if isinstance(Dinstatus,str):
            return Dinstatus
        elif Dinstatus['data']['DIN Status']=='Lapsed' or Dinstatus['data']['DIN Status']=='Disabled' or Dinstatus['data']['DIN Status']=='Deactivated due to non-filing of DIR-3 KYC':
            Master['Status'] = 'Failed'
            Master['Personal'] = f"DIN {DIN} (Name: {Dinstatus['data']['Director Name']}) is {Dinstatus['data']['DIN Status']}."
            return Master
        else:
            Name = Dinstatus['data']['Director Name']
            DINInfo=prefillDIN.prefillDIN(DIN)
        print(DINInfo)
        

def clearLayout(layout):
    while layout.count():
        child = layout.takeAt(0)
        if child.widget() is not None:
            child.widget().deleteLater()
        elif child.layout() is not None:
            clearLayout(child.layout())
        
