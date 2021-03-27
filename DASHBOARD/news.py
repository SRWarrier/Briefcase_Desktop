from PySide2 import QtWidgets, QtUiTools,QtCore, QtGui
import sys
import HomePage
import os
import numpy as np
from functions import Database_Manager as db
from functions import pyside_dynamic, getnews
import pickle
import webbrowser
import re
import datetime
import sqlite3



class Ui(QtWidgets.QWidget):
    def __init__(self):
        super(Ui, self).__init__()
        pyside_dynamic.loadUi('Resources/ui/news.ui',self)
        self.Displaylayout = QtWidgets.QGridLayout(self.newsWindow)
        self.Displaylayout.setObjectName("gridLayout_2")
        self.Displaylayout.setContentsMargins(0, 0, 0, 0)
        self.newsWindow.setLayout(self.Displaylayout)
        #spacerItem = QtWidgets.QSpacerItem(20, 555, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.update.clicked.connect(self.updateNews)
        self.filterMCA.clicked.connect(self.updateNews)
        self.filterIBBI.clicked.connect(self.updateNews)
        self.filterIT.clicked.connect(self.updateNews)
        self.filterGen.clicked.connect(self.updateNews)
        self.updateNews()
                                       
    def updateNews(self,lastnews=None):
        clearLayout(self.Displaylayout)
        attachment = ''
        tlayout = 2
##        try:
        if self.filterMCA.isChecked():
            NewsItem = getnews.getMCAUpdates(lastnews)
            title = 'MCA'
            self.NotifFolder = 'MCA Notification'
        elif self.filterIT.isChecked():
            NewsItem = getnews.getITUpdates(lastnews)
            title = 'Income Tax'
            self.NotifFolder = 'IT Notification'
        elif self.filterIBBI.isChecked():
            NewsItem = getnews.getIBBCUpdates(lastnews)
            title = 'IBBI'
            self.NotifFolder = 'IBBI Notification'
        elif self.filterGen.isChecked():
            NewsItem = getnews.getNews()
            title = 'General News'
##        except Exception as e:
##            title: 'Error'
##            NewsItem = [{'description':str(e), 'pdf':''}]
        for news in NewsItem:
            self.ButtonPanel = QtWidgets.QWidget(self.newsWindow)
            pyside_dynamic.loadUi('Resources/ui/NewsBox.ui',self.ButtonPanel)
            self.ButtonPanel.message.setOpenLinks(False)
            self.ButtonPanel.message.setOpenExternalLinks(True)
            self.ButtonPanel.message.setReadOnly(True)
            description = news['description']
            pdf = news['pdf']
            if 'amendment' in description.lower():
                self.ButtonPanel.setStyleSheet("background-color: rgb(85, 239, 196);color: rgb(255,255,255);")
                self.ButtonPanel.Newsman.setText(f'{title}: Amendment')
            elif 'notification' in description.lower():
                self.ButtonPanel.setStyleSheet("background-color: rgb(214, 48, 49);color: rgb(255,255,255);")
                self.ButtonPanel.Newsman.setText(f'{title}: Notification')
            elif 'extension' in description.lower():
                self.ButtonPanel.setStyleSheet("background-color: rgb(108, 92, 231); color: rgb(255,255,255);")
                self.ButtonPanel.Newsman.setText(f'{title}: Extension')
            else:
                self.ButtonPanel.setStyleSheet("background-color: rgb(45, 52, 54); color: rgb(255,255,255);")
                self.ButtonPanel.Newsman.setText(f'{title}: Updates')

            if pdf=='':
                self.ButtonPanel.message.setText(description)
            else:
                if self.filterGen.isChecked():
                    linkText = pdf.lower().replace('https://','').replace('http://','')
                    pdfFile = f'<br><a href = "{linkText}">Read more..</a>'
                else:
                    pdfFile = f'<br><a href = "{pdf}" target = "_self">{os.path.basename(pdf)}</a>'
                self.ButtonPanel.message.setText(description+pdfFile)
                self.ButtonPanel.message.anchorClicked.connect(self.filebrowse)
            self.Displaylayout.addWidget(self.ButtonPanel, self.Displaylayout.rowCount()+1,1,1,1)
        scroll_bar =self.scrollArea.verticalScrollBar()
        

    def filebrowse(self,text):
        if not self.filterGen.isChecked():
            link = text.toString().replace('%5C','/')
            if not os.path.isdir(os.path.join('..',self.NotifFolder)):
                os.mkdir(os.path.join('..',self.NotifFolder))
            if os.path.isfile(os.path.join('..',self.NotifFolder,os.path.basename(link))):
                webbrowser.open(os.path.realpath(os.path.join('..',self.NotifFolder,os.path.basename(link))))
            else:
                self.newsWindow.setEnabled(False)
                getnews.downloadPDF(link,os.path.join('..',self.NotifFolder),os.path.basename(link))
                webbrowser.open(os.path.realpath(os.path.join('..',self.NotifFolder,os.path.basename(link))))
                self.newsWindow.setEnabled(True)
        else:
            print(text.toString().replace('%5C','/'))
            webbrowser.open(text.path())
            
    def Test(self):
        Parent=(self.parent().parent().parent())
        print(Parent)
        print((Parent.MainWindow.findChild(QtWidgets.QWidget, 'Form').findChild(QtWidgets.QComboBox, 'CompanySelect').currentText()))#findChildren(QtWidgets.QWidget)))

       
def clearLayout(layout):
    while layout.count():
        child = layout.takeAt(0)
        if child.widget() is not None:
            child.widget().deleteLater()
        elif child.layout() is not None:
            clearLayout(child.layout())
