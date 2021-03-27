from PySide2 import QtWidgets, QtUiTools,QtCore, QtGui
import sys
import os
from functions import pyside_dynamic
from functions.Gdrive import Gdrive
from functions import Database_Manager as db
import sqlite3
import Login
import pickle
import subprocess


class Ui(QtWidgets.QWidget):
    def __init__(self):
        super(Ui, self).__init__()
        print(os.getcwd())
        pyside_dynamic.loadUi('../Resources/ui/Setup.ui',self)
        self.setWindowState(QtCore.Qt.WindowState.WindowMaximized)
        self.setWindowTitle('Corporate Compliance Companion')
        self.Masterlayout = self.display.layout()
        self.firstPage = QtWidgets.QWidget()
        pyside_dynamic.loadUi('../Resources/ui/Setup_page_1.ui',self.firstPage)
        self.firstPage.poster.setPixmap(QtGui.QPixmap(QtGui.QImage("../Resources/Icon/setup_Page_1.svg")))
        self.Masterlayout.addWidget(self.firstPage, *(0,0))
        self.firstPage.Next.clicked.connect(self.secondPage)
        self.show()

    def secondPage(self):
        clearLayout(self.Masterlayout)
        self.SecondPage = QtWidgets.QWidget()
        pyside_dynamic.loadUi('../Resources/ui/Setup_page_2.ui',self.SecondPage)
        self.SecondPage.poster.setPixmap(QtGui.QPixmap(QtGui.QImage("../Resources/Icon/setup_Page_2.svg")))
        self.Masterlayout.addWidget(self.SecondPage, *(0,0))
        self.SecondPage.Next.clicked.connect(self.thirdPage)

    def thirdPage(self):
        clearLayout(self.Masterlayout)
        self.ThirdPage = QtWidgets.QWidget()
        pyside_dynamic.loadUi('../Resources/ui/Setup_page_3.ui',self.ThirdPage)
        self.ThirdPage.poster.setPixmap(QtGui.QPixmap(QtGui.QImage("../Resources/Icon/setup_Page_3.svg")))
        self.Masterlayout.addWidget(self.ThirdPage, *(0,0))
        self.ThirdPage.Next.setEnabled(False)
        self.ThirdPage.Next.setStyleSheet("""border-width: 2px;
border-radius: 15px;
background-color: rgb(189,189,189);
color: rgb(255, 255, 255);""")
        self.ThirdPage.Next.clicked.connect(self.fourthpage)
        self.ThirdPage.Browse.clicked.connect(self.AddMasterFolder)

    def AddMasterFolder(self):
        self.MasterFolder = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select a folder', os.getcwd(), QtWidgets.QFileDialog.ShowDirsOnly)
        self.ThirdPage.Filename.setText(self.MasterFolder)
        if self.MasterFolder!='':
            self.ThirdPage.Next.setEnabled(True)
            self.ThirdPage.Next.setStyleSheet("""border-width: 2px;
border-radius: 15px;
background-color: rgb(0,150,136);
color: rgb(255, 255, 255);""")
        

    def fourthpage(self):
        clearLayout(self.Masterlayout)
        self.FourthPage = QtWidgets.QWidget()
        self.DatabaseFolder = os.path.join(self.MasterFolder,'Database')
        if os.path.isdir(self.DatabaseFolder) and os.path.isfile(os.path.join(self.DatabaseFolder,'C3_DataBase.db')):
            conn = sqlite3.connect(os.path.join(self.DatabaseFolder,'C3_DataBase.db'))
            cur = conn.cursor()
            AdminLIST = cur.execute(f"SELECT NAME from Users WHERE ROLE = {repr('Administrator')}").fetchall()
            pyside_dynamic.loadUi('../Resources/ui/Setup_page_4_User.ui',self.FourthPage)
            if len(AdminLIST)>1:
                AdminStrng = ''
                counter = 0
                for admin in AdminLIST:
                    if counter ==len(AdminLIST)-1:
                        AdminString = Adminstring+ ' and '+ admin[0]
                    elif counter==0:
                        AdminStrng = admin[0]
                    else:
                        AdminStrng = Adminstring+ ', '+ admin[0]
                    counter +=1
            else:
                AdminStrng = AdminLIST[0][0]
            self.FourthPage.Message.setText(f"You have linked to a system managed by {AdminStrng}")
            self.FourthPage.poster.setPixmap(QtGui.QPixmap(QtGui.QImage("../Resources/Icon/setup_Page_4.svg")))
            self.Masterlayout.addWidget(self.FourthPage, *(0,0))
            self.FourthPage.Done.clicked.connect(self.getLogin)                                                
        else:
            pyside_dynamic.loadUi('../Resources/ui/Setup_page_4.ui',self.FourthPage)
            self.FourthPage.poster.setPixmap(QtGui.QPixmap(QtGui.QImage("../Resources/Icon/setup_Page_4.svg")))
            self.Masterlayout.addWidget(self.FourthPage, *(0,0))
            reg_ex = QtCore.QRegExp("[A-Za-z][A-Za-z0-9]*")
            input_validator = QtGui.QRegExpValidator(reg_ex, self.FourthPage.UsernameInput)
            self.FourthPage.UsernameInput.setValidator(input_validator)
            input_validator = QtGui.QRegExpValidator(reg_ex, self.FourthPage.PasswordInput)
            self.FourthPage.PasswordInput.setValidator(input_validator)
            self.FourthPage.Done.clicked.connect(self.Login)

    def getLogin(self):
        with open('Config','wb') as configfile:
            Config = pickle.dumps({'Home':self.MasterFolder,'Database':self.DatabaseFolder})
            configfile.write(Config)
            configfile.close()
        loginPage = Login.Ui()
        self.close()
        
    def Login(self):
        if self.FourthPage.Nameinput.text()!='':
            if self.FourthPage.UsernameInput.text()!='':
                if self.FourthPage.PasswordInput.text()!='':                                        
                    os.mkdir(self.DatabaseFolder)
                    with open('Config','wb') as configfile:
                        Config = pickle.dumps({'Home':self.MasterFolder, 'Database':self.DatabaseFolder})
                        configfile.write(Config)
                        configfile.close()
                    db.createDBFile(self.DatabaseFolder)
                    subprocess.check_call(["attrib","+H",self.DatabaseFolder])
                    UserDict = {'USERNAME':self.FourthPage.UsernameInput.text(),'PASSWORD':self.FourthPage.PasswordInput.text(),'ROLE':'Administrator','NAME':self.FourthPage.Nameinput.text(),'LASTLOGIN':''}
                    Status = db.AddUser(UserDict)
                    loginPage = Login.Ui()
                    self.close()
                else:
                    self.feedback("failure","Password cannot be empty")
            else:
                self.feedback("failure","Username cannot be empty")
        else:
            self.feedback("failure","Please create a User before proceeding")


    def feedback(self, status, Message):
        icon = QtGui.QIcon()
        if status=='success':     
            icon.addPixmap(QtGui.QPixmap(QtGui.QImage("../Resources/Icon/tick.png")), QtGui.QIcon.Disabled, QtGui.QIcon.Off)
        elif status=='failure':
            icon.addPixmap(QtGui.QPixmap(QtGui.QImage("../Resources/Icon/close.png")), QtGui.QIcon.Disabled, QtGui.QIcon.Off)
        else:
            icon.addPixmap(QtGui.QPixmap(QtGui.QImage("../Resources/Icon/warning.png")), QtGui.QIcon.Disabled, QtGui.QIcon.Off)
        self.FourthPage.Information.setIcon(icon)
        self.FourthPage.Information.setText(Message)
                    
                    
            

         




def clearLayout(layout):
    while layout.count():
        child = layout.takeAt(0)
        if child.widget() is not None:
            child.widget().deleteLater()
        elif child.layout() is not None:
            clearLayout(child.layout())
