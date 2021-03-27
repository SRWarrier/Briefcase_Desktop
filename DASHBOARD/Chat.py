from PySide2 import QtWidgets, QtUiTools,QtCore, QtGui
import sys
import HomePage
import os
import numpy as np
from functions import Database_Manager as db
from functions import pyside_dynamic
import pickle
import webbrowser
import re
import datetime
import sqlite3





def getUsers():
    with open('Config','rb') as f:
            Config = pickle.loads(f.read())
            f.close()
    with open('_temp/_currentuser','rb') as f:
            UserFile = pickle.loads(f.read())
            f.close()
    dbfilepath = os.path.join(Config['Database'],'C3_DataBase.db')
    NameList = []
    if os.path.isfile(dbfilepath):
        conn = sqlite3.connect(dbfilepath)
        cur = conn.cursor()
        usernames = cur.execute("SELECT NAME from Users").fetchall()
        for names in usernames:
            if names[0]!=UserFile['CurrentUser']:
                NameList.append('@'+names[0].replace(' ','_'))
    return NameList



class Ui(QtWidgets.QWidget):
    def __init__(self):
        super(Ui, self).__init__()
        pyside_dynamic.loadUi('Resources/ui/chat.ui',self)
        with open('Config','rb') as f:
            Config = pickle.loads(f.read())
            f.close()
        self.dbfilepath = os.path.join(Config['Database'],'Chat.db')
        self.Displaylayout = QtWidgets.QGridLayout(self.ChatWindow)
        self.Displaylayout.setObjectName("gridLayout_2")
        self.Displaylayout.setContentsMargins(0, 0, 0, 0)
        self.ChatWindow.setLayout(self.Displaylayout)
        #spacerItem = QtWidgets.QSpacerItem(20, 555, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.send.clicked.connect(self.sendMessage)
        self.fileattach.clicked.connect(self.attach)
        self.folderattach.clicked.connect(self.attach)
        with open('_temp/_currentuser','rb') as currentUser:
            Userdata = pickle.loads(currentUser.read())
            currentUser.close()
        self.currentuser = (Userdata['CurrentUser'])
        self.message.setCompleter(CustomCompleter())
        foldericon = QtGui.QIcon()
        foldericon.addPixmap(QtGui.QPixmap(QtGui.QImage("Resources/Icon/folder.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.folderattach.setIcon(foldericon)
        fileicon = QtGui.QIcon()
        fileicon.addPixmap(QtGui.QPixmap(QtGui.QImage("Resources/Icon/file.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.fileattach.setIcon(fileicon)
        self.isfileattached = False
        self.isfolderattached = False
        self.loadChat()
        #self.show()

    def sendMessage(self):
        Message = self.message.text()
        self.createBadge(Message)

    def attach(self):
        sender =(self.sender().objectName())
        if sender == 'fileattach':
            self.attachedfile = QtWidgets.QFileDialog.getOpenFileName(self, 'Select file', '../../Clients',"All files (*)")
            filename = os.path.basename(self.attachedfile[0])
            if len(filename)>32:
                filename = filename[:12]+'...'+os.path.splitext(filename)[1]
            self.filepreview.setText(filename)
            self.isfileattached = True
        if sender == 'folderattach':
            self.attachfolder = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Folder', '../../Clients')
            self.folderpreview.setText(os.path.basename(self.attachfolder))
            self.isfolderattached = True
                                     

    def createBadge(self,text,isMessage=False, userName =None, attachment = '',timestamp=None):
        self.ButtonPanel = QtWidgets.QWidget(self.ChatWindow)
        pyside_dynamic.loadUi('Resources/ui/messageBox.ui',self.ButtonPanel)         
        self.ButtonPanel.message.setOpenLinks(False)
        self.ButtonPanel.message.setOpenExternalLinks(True)
        self.ButtonPanel.message.setReadOnly(True)
        self.ButtonPanel.message.anchorClicked.connect(self.filebrowse)
        if isMessage:
            self.ButtonPanel.userName.setText(f'{userName}')
            self.ButtonPanel.message.setText(f'{text}{attachment}')
            self.ButtonPanel.sentTime.setText(f'{timestamp}')
            self.Displaylayout.addWidget(self.ButtonPanel, self.Displaylayout.rowCount()+1,1,1,1)
        else:
            userName = self.currentuser
            if self.isfileattached or self.isfolderattached:
                if self.isfileattached:
                    attachment = attachment+'<br>'+f'<br><a href = "{os.path.realpath(self.attachedfile[0])}" target = "_self">{os.path.basename(self.attachedfile[0])}</a>'
                if self.isfolderattached:
                    attachment = attachment+'<br>'+f'<br><a href = "{os.path.abspath(self.attachfolder)}" target = "_self">{os.path.basename(self.attachfolder)}</a>'
            if text!='':
                self.ButtonPanel.message.setText(f'{self.compileText(text)}{attachment}')
            else:
                attachment = attachment.replace("<br>","")
                self.ButtonPanel.message.setText(f'{attachment}')
            self.ButtonPanel.userName.setText(f'{userName}')
            Timestamp = datetime.datetime.strftime(datetime.datetime.now(),"%d/%m - %H:%M:%S")
            self.ButtonPanel.sentTime.setText(f'{Timestamp}')
            self.Displaylayout.addWidget(self.ButtonPanel, self.Displaylayout.rowCount()+1,1,1,1)
            chatInfo = [userName,self.compileText(text),attachment,Timestamp]
            db.chathistory(chatInfo)
            self.isfolderattached = False
            self.isfileattached = False
            self.attachedfile=''
            self.attachfolder=''
            self.message.clear()
            self.filepreview.clear()
            self.folderpreview.clear()
        scroll_bar =self.scrollArea.verticalScrollBar()
        scroll_bar.rangeChanged.connect(lambda: scroll_bar.setValue(scroll_bar.maximum()))
        

    def filebrowse(self,text):
        link = text.toString().replace('%5C','/')
        webbrowser.open(link)

    def compileText(self,text):
        httplinks = re.findall('(?:(?:https?|ftp):\/\/)?[\w/\-?=%.]+\.[\w/\-?=%.]+', text)
        for link in httplinks:
            linkText = link.lower().replace('https://','').replace('http://','')
            text = text.replace(link,f'<a href = "{linkText}">{link}</a>')
        return text

    def loadChat(self):
        try:
            self.conn = sqlite3.connect(self.dbfilepath)
            self.cur = self.conn.cursor()
            ChatList = self.cur.execute('SELECT * from chat').fetchall()
            for chat in ChatList:
                self.createBadge(chat[1],isMessage=True, userName =chat[0], attachment = chat[2],timestamp=chat[3])
        except:
            pass
        

class CustomCompleter(QtWidgets.QCompleter):

    def __init__(self):
        super().__init__()

    def splitPath(self, path):
        self.userNames = getUsers()
        if path.endswith('@'):
            self.setModel(QtCore.QStringListModel(self.userNames))
        return [path]

