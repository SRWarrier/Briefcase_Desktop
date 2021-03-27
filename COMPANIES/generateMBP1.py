from PySide2 import QtWidgets, QtUiTools,QtCore, QtGui
import sys
import os
from functions import SessionLogin, SessionLogout, getDirectorMasterdata, getLoginCaptcha
from functions.generateDocuments import MBP1, DIR8
from functions import pyside_dynamic
import sqlite3
import datetime
import requests_html
import pandas as pd



class Ui(QtWidgets.QWidget):
    def __init__(self):
        super(Ui, self).__init__()
        pyside_dynamic.loadUi('Resources/ui/generateMBP1.ui',self)
        self.CompanySelect = self.findChild(QtWidgets.QComboBox, 'NameField')
        dbfilepath = 'Database/C3_DataBase.db'
        self.DirectorContainer = []
        self.DINList = {}
        self.conn = sqlite3.connect(dbfilepath)
        self.cur = self.conn.cursor()
        CompanyListdb = self.cur.execute('SELECT "company_name" from Masterdata').fetchall()
        CompanyList=['']
        for item in CompanyListdb:
            CompanyList.append(item[0])
        self.CompanySelect.addItems(CompanyList)
        self.CompanySelect.activated.connect(self.getDirector)
        self.layout = self.findChild(QtWidgets.QGridLayout, 'DirectorsLayout')
        self.startdate = self.findChild(QtWidgets.QDateEdit, 'startDate')
        self.startdate.setDate(QtCore.QDate.fromString('01-04-'+str(QtCore.QDate.currentDate().year()),'dd-MM-yyyy'))
        self.enddate = self.findChild(QtWidgets.QDateEdit, 'Enddate')
        self.enddate.setDate(QtCore.QDate.fromString('01-04-'+str(QtCore.QDate.currentDate().year()+1),'dd-MM-yyyy'))
        self.generate = self.findChild(QtWidgets.QPushButton, 'generate')
        # self.Signdate = self.findChild(QtWidgets.QLineEdit, 'SignDate')
        # self.Signdate.setText(datetime.datetime.strftime(datetime.datetime.now().date(),'%B %d, %Y')) 
        # self.SignPlace = self.findChild(QtWidgets.QLineEdit, 'SignPlace')
        self.SelectDirectors = self.findChild(QtWidgets.QWidget, 'SelectDirectors')
        self.generate.clicked.connect(self.LoginCheck)
        self.show()


    def getDirector(self):
        clearLayout(self.layout)
        self.CompanySelection = self.CompanySelect.currentText()
        self.DirectorContainer=[]
        self.CompanyData = self.cur.execute(f'SELECT * from Masterdata WHERE "company_name" = "{self.CompanySelection}"').fetchall()[0]
        self.CompanyRegOffice = self.CompanyData[11]
        self.CompanyRegNo = self.CompanyData[3]
        self.NomCap = self.CompanyData[7]
        self.PaidCap = self.CompanyData[8]
        self.CompanyCIN = self.CompanyData[0]
        self.DirectorsList = self.cur.execute(f'SELECT * from Signatories WHERE "company_cin" = "{self.CompanyCIN}"').fetchall()
        DirectorsNameList = []
        for Director in self.DirectorsList:
            DirectorsNameList.append(Director[2])
        #print(DirectorsNameList)
        Font = QtGui.QFont("Georgia", 11)
        DesignationPriority = {"Managing Director": 0, "Wholetime Director": 1, "Director": 2, "Additional Director": 3,
                               "Alternate Director": 4, "Nominee Director": 4,"Company Secretary": 5, "CEO(KMP)" : 6 , 'CFO(KMP' : 7}
        self.DirectorsList.sort(key=lambda val: DesignationPriority[val[4]])
        self.SelectDirectors.BTGroup = QtWidgets.QButtonGroup()
        rowCounter = 0
        for director in self.DirectorsList:
            item = QtWidgets.QCheckBox(director[2]+', '+director[4])
            self.DINList[director[2]] = director[1]
            item.setFont(Font)
            placeBlock = QtWidgets.QLineEdit()
            placeBlock.setPlaceholderText = "Place"
            DateBlock = QtWidgets.QLineEdit()
            DateBlock.setText(datetime.datetime.strftime(datetime.datetime.now().date(),'%B %d, %Y'))
            if 'director'in director[4].lower():
                self.layout.addWidget(item,rowCounter,0)
                self.layout.addWidget(placeBlock,rowCounter,1)
                self.layout.addWidget(DateBlock,rowCounter,2)
                self.SelectDirectors.BTGroup.addButton(item)
                rowCounter +=1
        self.SelectDirectors.BTGroup.setExclusive(False)
        self.SelectDirectors.BTGroup.buttonClicked.connect(self.AddAuthorized)
        self.SelectDirectors.setLayout(self.layout)

        
    def AddAuthorized(self,button):
        if button.text() not in self.DirectorContainer:
            self.DirectorContainer.append(button.text())
        elif button.text() in self.DirectorContainer:
            self.DirectorContainer.remove(button.text())
        else:
            None

    def generateMBP(self):
        self.DirectorInterest = {}
        for Director in self.DirectorContainer:
            DirectorName = Director.split(',')[0]
            DirectorDIN = self.DINList[DirectorName]
            DirectorDesignation = self.cur.execute(f'SELECT Designation from Signatories WHERE "director_din" = "{DirectorDIN}"').fetchall()[0][0]
            DirectorGender = self.cur.execute(f'SELECT director_gender from Signatories WHERE "director_din" = "{DirectorDIN}"').fetchall()[0][0]
            DirectorFatherData = self.cur.execute(f'SELECT director_fathers_first_name,director_fathers_middle_name,director_fathers_last_name from Signatories WHERE "director_din" = "{DirectorDIN}"').fetchall()[0]
            DirectorAddress = self.cur.execute(f'SELECT director_address from Signatories WHERE "director_din" = "{DirectorDIN}"').fetchall()[0][0]
            DirectorFatherName = ''
            for Name in DirectorFatherData:
                if Name!='':
                    DirectorFatherName = DirectorFatherName+' '+Name
            startdate = datetime.datetime.strptime(self.startdate.date().toString(),'%a %b %d %Y')
            enddate = datetime.datetime.strptime(self.enddate.date().toString(),'%a %b %d %Y')
            MBPData = getDirectorMasterdata.getDirectorMasterdata(DirectorDIN)
            CompanyInterestList=[]
            if not isinstance(MBPData,str):
                MBPData[['Date of cessation','Date of appointment at current designation','Original date of appointment']] = MBPData[['Date of cessation','Date of appointment at current designation','Original date of appointment']].apply(pd.to_datetime,errors = 'coerce')
                TableData = MBPData.loc[(MBPData['Company/ LLP Status']=='Active') & ((MBPData['Original date of appointment']<= enddate)&(MBPData['Original date of appointment']<= enddate)&(MBPData['Date of cessation']> enddate)|(pd.isnull(MBPData['Date of cessation'])))]
                ChangeTable = TableData.loc[((TableData['Date of appointment at current designation']>=startdate)&(TableData['Date of appointment at current designation']<= enddate))]
                CessationTable=TableData.loc[((TableData['Date of cessation']>=startdate)&(TableData['Date of cessation']<= enddate))]
                looper = 1
                for x in (TableData.values):
                    if x[4]<=enddate and x[1].lower().replace(' ','')!=self.CompanySelection.lower().replace(' ',''):
                        tempDict = []
                        tempDict.append(str(looper)+'.')
                        CoName=''
                        for tx in x[1].title().split(' '):
                            if len(tx)<4:
                                    CoName=CoName+' '+tx.upper()
                            else:
                                    CoName=CoName+' '+tx
                        tempDict.append(CoName.strip())
                        tempDict.append(x[2])
                        tempDict.append('-')
                        if str(x[5])!='NaT':
                            if startdate<=x[5]<=enddate:
                                tempDict.append(datetime.datetime.strftime(x[5].date(),'%d.%m.%Y'))
                            else:
                                if not isinstance(x[3],str):
                                    if x[3]<=enddate:
                                        tempDict.append(datetime.datetime.strftime(x[3].date(),'%d.%m.%Y'))
                                else:
                                    tempDict.append(datetime.datetime.strftime(x[4].date(),'%d.%m.%Y'))
                        else:
                            if not isinstance(x[3],str):
                                if x[3]<=enddate:
                                    tempDict.append(datetime.datetime.strftime(x[3].date(),'%d.%m.%Y'))
                            else:
                                tempDict.append(datetime.datetime.strftime(x[4].date(),'%d.%m.%Y'))
                        CompanyInterestList.append(tempDict)
                        looper+=1
            if len(CompanyInterestList)==0 or isinstance(MBPData,str):
                CompanyInterestList=[['-','-','-','-','-']]
            Document = MBP1.createDoc()
            Document.HeadLine("FORM MBP – 1","Notice of interest by director","[Pursuant to section 184 (1) and rule 9(1)]")
            Document.NoticeAddressee(self.CompanySelection,self.CompanyRegOffice,"The Board of Directors")
            Document.MBP1(DirectorName,DirectorGender,DirectorFatherName,DirectorAddress,CompanyInterestList,DirectorDesignation,DirectorDIN)#,self.Signdate.text(),self.SignPlace.text())
            folderTree = os.path.join('Clients',self.CompanySelection,str(int(self.startdate.date().toPython().year))+'-'+str(int(self.startdate.date().toPython().year)+1),'MBP 1')
            if not os.path.isdir('../'+folderTree):
                os.makedirs('../'+folderTree)
            Document.saveDoc(os.path.join('..',folderTree,DirectorName+'_MBP-1'))
            if not os.path.isdir('../'+folderTree+'/Reference'):
                os.makedirs('../'+folderTree+'/Reference')
            MBPData.to_csv(os.path.join('..',folderTree,'Reference',DirectorName+'_Masterdata.csv'),index=False)
            if self.selectDIR.isChecked():
                CompanyInterestList=[]
                for x in (TableData.values):
                    if x[4]<=enddate and x[1].lower().replace(' ','')!=self.CompanySelection.lower().replace(' ',''):
                        tempDict = []
                        CoName=''
                        for tx in x[1].title().split(' '):
                            if len(tx)<4:
                                    CoName=CoName+' '+tx.upper()
                            else:
                                    CoName=CoName+' '+tx
                        tempDict.append(CoName.strip())
                        tempDict.append(datetime.datetime.strftime(x[4].date(),'%d.%m.%Y'))
                        if str(x[5])!='NaT':
                            if x[5]>startdate-datetime.timedelta(days=365*3):
                                if x[5]<=enddate:
                                    tempDict.append(datetime.datetime.strftime(x[5].date(),'%d.%m.%Y'))
                                else:
                                    tempDict.append('-')
                            else:
                                tempDict.append('-')
                        else:
                            tempDict.append('-')
                        CompanyInterestList.append(tempDict)
                Document = DIR8.createDoc()
                Document.HeadLine("FORM DIR-8","Intimation by Director","[Pursuant to Section 164(2) and rule 14(1) of Companies (Appointment and Qualification of Directors) Rules, 2014]")
                Document.preBlock(self.CompanyRegNo,self.NomCap,self.PaidCap,self.CompanySelection,self.CompanyRegOffice)
                Document.NoticeAddressee(self.CompanySelection)
                if len(CompanyInterestList)==0 or isinstance(MBPData,str):
                    CompanyInterestList=[['-','-','-']]
                Document.DIR8(DirectorName,DirectorGender,DirectorFatherName,DirectorAddress,CompanyInterestList,DirectorDesignation,DirectorDIN)#,self.Signdate.text(),self.SignPlace.text())
                folderTree = os.path.join('Clients',self.CompanySelection,str(int(self.startdate.date().toPython().year))+'-'+str(int(self.startdate.date().toPython().year)+1),'DIR-8')
                if not os.path.isdir('../'+folderTree):
                    os.makedirs('../'+folderTree)
                Document.saveDoc(os.path.join('..',folderTree,DirectorName+'_DIR-8'))
    

    def LoginCheck(self):
            if os.path.isfile('_temp/session'):
                filetimestamp = datetime.datetime.fromtimestamp(os.path.getmtime('_temp/session'))
                if not filetimestamp.date() == datetime.datetime.now().date() or not(filetimestamp+datetime.timedelta(minutes = 15)).time()>datetime.datetime.now().time():
                     self.session = requests_html.HTMLSession()
                     self.captcha(session = self.session)
                else:
                    self.generateMBP()
            elif not os.path.isfile('_temp/session'):
                self.session = requests_html.HTMLSession()
                self.captcha(session = self.session)
            else:
                self.generateMBP()
            #CompanyList = getDirDetails.getDirdetails(DirectorDIN)

    def Login(self):
        LoginStatus = SessionLogin.Login(AccessCode = self.AccessCode, session=self.session, captcha = self.CaptchaInput.text())
        if not LoginStatus:
            self.getCaptcha(self.session)
        else:
            self.captchaWindow.close()
            self.generateMBP()
            
    def captcha(self, session):
        self.captchaWindow = QtWidgets.QWidget()
        pyside_dynamic.loadUi('Resources/ui/captcha.ui',self.captchaWindow)
        #self.captchaWindow.move(300,300)
        self.captchaView = self.captchaWindow.findChild(QtWidgets.QLabel, 'captchaview')
        self.getCaptcha(self.session)
        self.captchaWindow.setWindowModality(QtCore.Qt.WindowModal)
        self.CaptchaInput = self.captchaWindow.findChild(QtWidgets.QLineEdit, 'captchainput')
        self.SubmitButton = self.captchaWindow.findChild(QtWidgets.QPushButton, 'submit')
        self.SubmitButton.clicked.connect(self.Login)
        self.refreshButton = self.captchaWindow.findChild(QtWidgets.QPushButton, 'refresh')
        self.refreshButton.clicked.connect(self.getCaptcha)
        self.captchaWindow.show()


    def getCaptcha(self,session):
        capcthaImage, self.AccessCode = getLoginCaptcha.getMCA_Captcha(session)
        pixmap = QtGui.QPixmap()
        pixmap.loadFromData(capcthaImage)
        self.captchaView.setScaledContents(True)
        self.captchaView.setPixmap(pixmap)
        self.captchaView.setAlignment(QtCore.Qt.AlignVCenter)
        self.captchaView.setAlignment(QtCore.Qt.AlignHCenter)

def clearLayout(layout):
    while layout.count():
        child = layout.takeAt(0)
        if child.widget() is not None:
            child.widget().deleteLater()
        elif child.layout() is not None:
            clearLayout(child.layout())
