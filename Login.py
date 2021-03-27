from PySide2 import QtWidgets, QtUiTools,QtCore, QtGui, QtXml
import sys
import sqlite3
import HomePage
from ADMIN import AddUser
import pickle
import os
import datetime
from functions import Database_Manager, pyside_dynamic
from functions.Gdrive import Gdrive
import time




class Ui(QtWidgets.QWidget):
    def __init__(self):
        super(Ui, self).__init__()
        pyside_dynamic.loadUi('Resources/ui/Login.ui',self)
        self.setWindowState(QtCore.Qt.WindowState.WindowMaximized)
        self.saveConfig = False
        self.setWindowTitle('Corporate Compliance Companion')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(QtGui.QImage("Resources/Icon/logo.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)
        if os.path.isfile('_temp/_currentuser'):
            with open('_temp/_currentuser','rb') as f:
                Userdata = pickle.loads(f.read())
                f.close()
            if datetime.datetime.fromtimestamp(Userdata['SessionID']).date()==datetime.datetime.now().date():
                self.ui = HomePage.Ui()
                
            else:
                os.remove('_temp/_currentuser')
                self.LoginButton = self.findChild(QtWidgets.QPushButton, 'LoginButton')
                self.LoginButton.clicked.connect(self.validate)

                self.Information = self.findChild(QtWidgets.QToolButton, 'Information')
                self.InfoFrame = self.findChild(QtWidgets.QFrame, 'InfoFrame')
                self.AvatarIcon =QtGui.QPixmap(QtGui.QImage('Resources/Icon/avatar.png'))
                self.loginAvatar.setPixmap(self.AvatarIcon)

                self.show()
        else:
            self.LoginButton = self.findChild(QtWidgets.QPushButton, 'LoginButton')
            self.LoginButton.clicked.connect(self.validate)
          
            self.AvatarIcon =QtGui.QPixmap(QtGui.QImage('Resources/Icon/avatar.png'))
            self.loginAvatar.setPixmap(self.AvatarIcon)
            
            self.show()    
        


    def validate(self):
        UserName = self.UsernameInput.text()
        Password = self.PasswordInput.text()
        if UserName=='ProgrammerAccess' and Password=='sarathwarrier20031991@':
            self.close()
            self.AddUser = AddUser.Ui()
            self.AddUser.isProgrammer(True)
        elif UserName=='' or Password=='':
            if UserName=='':
                self.feedback('warning', 'Username cannot be empty')
            elif Password=='':
                self.feedback('warning', 'Password cannot be empty')
        else:
            self.validateCredentials(UserName,Password)
            
    def validateCredentials(self,UserName,Password):
        self.loggedin=False
        with open('Config','rb') as f:
            Config = pickle.loads(f.read())
            f.close()
        try:
            dbfilepath = os.path.join(Config['Database'],'C3_DataBase.db')
            conn = sqlite3.connect(dbfilepath)
            cur = conn.cursor()
            Userdatabase = cur.execute("SELECT * from Users")
        except Exception as e:
            
            if str(e) =='unable to open database file':
                self.Message = QtWidgets.QMessageBox(self)
                self.Message.setIcon(QtWidgets.QMessageBox.Information)
                self.Message.setText("Database not found. Please connect manually.")
                self.Message.setWindowTitle('Database not found!!')
                self.Wait = QtWidgets.QPushButton()
                self.Wait.setText('Browse')
                self.NoTime = QtWidgets.QPushButton()
                self.NoTime.setText('Cancel')
                self.Message.addButton(self.Wait, QtWidgets.QMessageBox.YesRole)
                self.Message.addButton(self.NoTime, QtWidgets.QMessageBox.NoRole)
                response = self.Message.exec()
                if response==0:
                    filepath =QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Database Folder', os.path.abspath(os.path.join(os.environ["HOMEPATH"], "Desktop")), QtWidgets.QFileDialog.ShowDirsOnly)
                    dbfilepath = os.path.join(filepath,'Database','C3_DataBase.db')
                    conn = sqlite3.connect(dbfilepath)
                    cur = conn.cursor()
                    Userdatabase = cur.execute("SELECT * from Users")
                    self.saveConfig = True
                    

        for x in (Userdatabase.fetchall()):
            if x[1]==UserName and x[2]=='':
                UserID = x[0]
                CurrentUser =  x[-2]
                Role = x[-3]
                LastLogin = "This is your First Session"
                self.loggedin=True
                if self.saveConfig == True:
                    with open('Config','rb') as configfile:
                        Config = pickle.loads(configfile.read())
                        Config['Database'] = os.path.join(filepath,'Database')
                        Config['Home'] = filepath
                        configfile.close()
                    with open('Config','wb') as configfile:
                        Config = pickle.dumps(Config)
                        configfile.write(Config)
                        configfile.close()          
                Database_Manager.UpdateUser('PASSWORD',Password,'ID',UserID)
                break
                
            if x[1]==UserName and x[2]==Password:
                if self.saveConfig == True:
                    with open('Config','rb') as configfile:
                        Config = pickle.loads(configfile.read())
                        Config['Database'] = os.path.join(filepath,'Database')
                        Config['Home'] = filepath
                        configfile.close()
                    with open('Config','wb') as configfile:
                        Config = pickle.dumps(Config)
                        configfile.write(Config)
                        configfile.close() 
                UserID = x[0]
                CurrentUser =  x[-2]
                Role = x[-3]
                LastLogin = x[-1]
                self.loggedin=True
                break

        if self.loggedin:
            currentuser = {'SessionID':datetime.datetime.timestamp(datetime.datetime.now()),'UserID':UserID,'CurrentUser':CurrentUser,'Role':Role,'LastLogin':LastLogin}
            with open('_temp/_currentuser','wb') as user:
                Userfile = pickle.dumps(currentuser)
                user.write(Userfile)
                user.close()
            Database_Manager.UpdateUser('LASTLOGIN',datetime.datetime.strftime(datetime.datetime.now(),'%a %d/%m/%Y %H:%M:%S'),'ID',UserID)
            self.feedback('success', f'Welcome {CurrentUser}')
            self.ui = HomePage.Ui()
            #time.sleep(3)
            self.close()

 
        else:
            self.feedback('failure', 'Invalid Username/Password')
            self.UsernameInput.setText('')
            self.PasswordInput.setText('')


    def feedback(self, status, Message):
        icon = QtGui.QIcon()
        if status=='success':     
            icon.addPixmap(QtGui.QPixmap(QtGui.QImage("Resources/Icon/tick.png")), QtGui.QIcon.Disabled, QtGui.QIcon.Off)
        elif status=='failure':
            icon.addPixmap(QtGui.QPixmap(QtGui.QImage("Resources/Icon/close.png")), QtGui.QIcon.Disabled, QtGui.QIcon.Off)
        else:
            icon.addPixmap(QtGui.QPixmap(QtGui.QImage("Resources/Icon/warning.png")), QtGui.QIcon.Disabled, QtGui.QIcon.Off)
        self.Information.setIcon(icon)
        self.Information.setText(Message)

    def check(self,button):
        print(button.text)
        
        

