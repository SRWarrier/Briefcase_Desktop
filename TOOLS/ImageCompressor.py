from PySide2 import QtWidgets, QtUiTools,QtCore, QtGui
from PIL import Image
import os
from io import BytesIO

class Ui_Form(object):
    def setupUi(self, ImageCompressor,CurrentUser, Role):
        ImageCompressor.setObjectName("ImageCompressor")
        ImageCompressor.setWindowModality(QtCore.Qt.ApplicationModal)
        ImageCompressor.setFixedSize(600, 450)
        ImageCompressor.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.CurrentUser = CurrentUser
        self.Role = Role
        self.fileTray = []
        self.gridLayout = QtWidgets.QGridLayout(ImageCompressor)
        self.gridLayout.setObjectName("gridLayout")
        self.label_3 = QtWidgets.QLabel(ImageCompressor)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton = QtWidgets.QPushButton(ImageCompressor)
        self.pushButton.setStyleSheet("background-color: rgb(85, 170, 255);\n"
"color: rgb(255, 255, 255);\n"
"font: 12pt \"AvantGarde LT Medium\";")
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.SelectFile)
        self.horizontalLayout.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(ImageCompressor)
        self.pushButton_2.setStyleSheet("background-color: rgb(255, 0, 0);\n"
"font: 12pt \"AvantGarde LT Medium\";\n"
"color: rgb(255, 255, 255);")
        self.pushButton_2.setFlat(False)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.SelectFiles)
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.pushButton_4 = QtWidgets.QPushButton(ImageCompressor)
        self.pushButton_4.setStyleSheet("background-color: rgb(134, 23, 133);\n"
"font: 12pt \"AvantGarde LT Medium\";\n"
"color: rgb(255, 255, 255);")
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.clicked.connect(self.Clear_table)
        self.gridLayout.addWidget(self.pushButton_4, 6, 0, 1, 1)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(ImageCompressor)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.threshold = QtWidgets.QLineEdit(ImageCompressor)
        self.threshold.setObjectName("lineEdit")
        self.threshold.setText("0")
        self.horizontalLayout_2.addWidget(self.threshold)
        self.horizontalLayout_3.addLayout(self.horizontalLayout_2)
        self.gridLayout.addLayout(self.horizontalLayout_3, 2, 0, 1, 1)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.radioButton_3 = QtWidgets.QRadioButton(ImageCompressor)
        self.radioButton_3.setObjectName("radioButton_3")
        self.radioButton_3.setChecked(True)
        self.radioButton_3.clicked.connect(self.Compression_Choice)
        self.horizontalLayout_5.addWidget(self.radioButton_3)
        self.radioButton_2 = QtWidgets.QRadioButton(ImageCompressor)
        self.radioButton_2.setObjectName("radioButton_2")
        self.radioButton_2.clicked.connect(self.Compression_Choice)
        self.horizontalLayout_5.addWidget(self.radioButton_2)
        self.radioButton = QtWidgets.QRadioButton(ImageCompressor)
        self.radioButton.setObjectName("radioButton")
        self.radioButton.clicked.connect(self.Compression_Choice)
        self.horizontalLayout_5.addWidget(self.radioButton)
        self.gridLayout.addLayout(self.horizontalLayout_5, 3, 0, 1, 1)
        self.tableView = QtWidgets.QTableWidget(ImageCompressor)
        self.tableView.setColumnCount(5)
        item = QtWidgets.QTableWidgetItem()
        self.tableView.setHorizontalHeaderItem(0, item)
        item.setText("File Name")
        item = QtWidgets.QTableWidgetItem()
        self.tableView.setHorizontalHeaderItem(1, item)
        item.setText("Compression %")
        item = QtWidgets.QTableWidgetItem()
        self.tableView.setHorizontalHeaderItem(2, item)
        item.setText("Old Size")
        item = QtWidgets.QTableWidgetItem()
        self.tableView.setHorizontalHeaderItem(3, item)
        item.setText("New Size")
        item = QtWidgets.QTableWidgetItem()
        self.tableView.setHorizontalHeaderItem(4, item)
        item.setText("Status")
        self.tableView.horizontalHeader().setCascadingSectionResizes(True)
        self.tableView.setGridStyle(QtCore.Qt.SolidLine)
        self.tableView.setObjectName("tableView")
        self.tableView.horizontalHeader().setDefaultSectionSize(115)
        self.tableView.horizontalHeader().setSectionResizeMode(115)
        self.tableView.setShowGrid(True)
        self.gridLayout.addWidget(self.tableView, 4, 0, 1, 1)
        self.pushButton_3 = QtWidgets.QPushButton(ImageCompressor)
        self.pushButton_3.setStyleSheet("background-color: rgb(85, 170, 0);\n"
"font: 12pt \"AvantGarde LT Medium\";\n"
"color: rgb(255, 255, 255);")
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.Compress)
        self.gridLayout.addWidget(self.pushButton_3, 5, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(ImageCompressor)
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 7, 0, 1, 1)
        self.label_2.raise_()
        self.label.raise_()
        self.label.raise_()
        self.label_3.raise_()
        self.pushButton_3.raise_()
        self.tableView.raise_()


        self.retranslateUi(ImageCompressor)
        QtCore.QMetaObject.connectSlotsByName(ImageCompressor)

    def retranslateUi(self, ImageCompressor):
        _translate = QtCore.QCoreApplication.translate
        ImageCompressor.setWindowTitle(_translate("ImageCompressor", "Compress Images"))
        self.label_3.setText(_translate("ImageCompressor", "<html><head/><body><p><span style=\" font-size:11pt; font-weight:600;\">COMPRESS IMAGES</span></p></body></html>"))
        self.pushButton.setText(_translate("ImageCompressor", "Add Image"))
        self.pushButton_2.setText(_translate("ImageCompressor", "Batch Images"))
        self.label.setToolTip(_translate("ImageCompressor", "<html><head/><body><p>Ignore Image if the compression does not reach this level.</p></body></html>"))
        self.label.setText(_translate("ImageCompressor", "Threshold"))
        self.radioButton_3.setText(_translate("ImageCompressor", "High Quality"))
        self.radioButton_2.setText(_translate("ImageCompressor", "Medium Quality"))
        self.radioButton.setText(_translate("ImageCompressor", "Low Quality"))
        self.pushButton_3.setText(_translate("ImageCompressor", "Compress"))
        self.pushButton_4.setText(_translate("ImageCompressor", "Clear"))
        self.label_2.setText(_translate("ImageCompressor", "<html><head/><body><p>Compressed images are in the source folder under folder named \'Compressed\'</p></body></html>"))

    def Compression_Choice(self):
        if self.radioButton_3.isChecked():            
            self.CompressionMode='85'
        elif self.radioButton_2.isChecked():
            self.CompressionMode='60'
        elif self.radioButton.isChecked():
            self.CompressionMode='45'
            
    def Compress(self):
        if len(self.fileTray)!=0:
            self.Compression_Choice()
            xfile = self.fileTray
            if isinstance(xfile,str):
                    xfile = [xfile]
            loop_count=0
            def format_bytes(size):
                power = 2**10
                n = 0
                power_labels = {0 : '', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
                while size > power:
                    size /= power
                    n += 1
                return str(round(size,2))+' '+power_labels[n]+'B'
            for file in xfile:
                    filename = os.path.split(file)[-1]
                    if len(filename)>30:
                            
                            dfilename = filename[:27]+'. . .'
                    else:
                            dfilename = filename
                    dfilename = filename
                    folder = os.path.dirname(file)
                    oldsize = (os.stat(file).st_size)
                    str_oldsize = format_bytes(os.stat(file).st_size)
                    picture = Image.open(file)
                    if picture.mode =='RGBA':
                        remove_Alpha = Image.new("RGB", picture.size, (255, 255, 255))
                        remove_Alpha.paste(picture, mask=picture.split()[3])
                        picture = remove_Alpha
                    Img_Type = picture.format
                    dim = picture.size
                    if not os.path.isdir(os.path.join(folder,'Compressed')):
                        os.mkdir(os.path.join(folder,'Compressed'))
                    tempstore = BytesIO()
                    picture.save(tempstore,'JPEG',optimize=True,quality=int(self.CompressionMode))
                    newsize = (tempstore.tell())
                    str_newsize = format_bytes(tempstore.tell())
                    percent = round((oldsize-newsize)/float(oldsize)*100,2)
                    if percent> int(self.threshold.text()):
                            
                            item = QtWidgets.QTableWidgetItem()
                            self.tableView.setItem(loop_count, 1, item)
                            item.setText(str(percent)+ '%')
                            item.setTextAlignment(QtCore.Qt.AlignCenter)
                            item.setFlags(QtCore.Qt.ItemIsEnabled)
                            
                            item = QtWidgets.QTableWidgetItem()
                            self.tableView.setItem(loop_count, 2, item)
                            item.setText(str_oldsize)
                            item.setTextAlignment(QtCore.Qt.AlignCenter)
                            item.setFlags(QtCore.Qt.ItemIsEnabled)
                            
                            item = QtWidgets.QTableWidgetItem()
                            self.tableView.setItem(loop_count, 3, item)
                            item.setText(str_newsize)
                            item.setTextAlignment(QtCore.Qt.AlignCenter)
                            item.setFlags(QtCore.Qt.ItemIsEnabled)
                            
                            item = QtWidgets.QTableWidgetItem()
                            self.tableView.setItem(loop_count, 4, item)
                            item.setText('SAVED')
                            item.setTextAlignment(QtCore.Qt.AlignCenter)
                            item.setFlags(QtCore.Qt.ItemIsEnabled)

                            loop_count +=1
                            picture.save(os.path.join(folder,'Compressed',"Compressed_"+filename),'JPEG',optimize=True,quality=85)
                    else:
                            
                            item = QtWidgets.QTableWidgetItem()
                            item.setFlags(QtCore.Qt.ItemIsEnabled)
                            self.tableView.setItem(loop_count, 1, item)
                            item.setText(str(percent)+ '%')
                            item.setTextAlignment(QtCore.Qt.AlignCenter)

                            item = QtWidgets.QTableWidgetItem()
                            self.tableView.setItem(loop_count, 2, item)
                            item.setText(str_oldsize)
                            item.setTextAlignment(QtCore.Qt.AlignCenter)
                            item.setFlags(QtCore.Qt.ItemIsEnabled)
                            
                            item = QtWidgets.QTableWidgetItem()
                            self.tableView.setItem(loop_count, 3, item)
                            item.setText(str_newsize)
                            item.setTextAlignment(QtCore.Qt.AlignCenter)
                            item.setFlags(QtCore.Qt.ItemIsEnabled)
                            
                            item = QtWidgets.QTableWidgetItem()
                            item.setFlags(QtCore.Qt.ItemIsEnabled)
                            self.tableView.setItem(loop_count, 4, item)
                            item.setText('IGNORED')
                            item.setTextAlignment(QtCore.Qt.AlignCenter)
                            loop_count +=1
        else:
            pass
    def SelectFile(self):
        filewindow = QtWidgets.QFileDialog()
        filewindow.setFileMode(QtWidgets.QFileDialog.ExistingFiles)
        self.Imagefile,_ = filewindow.getOpenFileName(self.pushButton,"Select Image",'',"Image files (*.jpg *.gif *.png *.jpeg)")
        self.fileTray.append(self.Imagefile)
        self.displayTable()

    def SelectFiles(self):
        xfilter = "Image files (*.jpg *.gif *.png *.jpeg)"
        fileswindow = QtWidgets.QFileDialog()
        fileswindow.setFileMode(QtWidgets.QFileDialog.ExistingFiles)
        self.Imagefile,_ = fileswindow.getOpenFileNames(self.pushButton_2,"Select Image",'', xfilter)
        for item in self.Imagefile:
            self.fileTray.append(item)
        self.displayTable()
        
    def Clear_table(self):
        self.tableView.setRowCount(0)
        self.fileTray = []

    def displayTable(self):
        if len(self.fileTray)!=0:
            self.tableView.setRowCount(0)
            self.tableView.setRowCount(len(self.fileTray))
            loop_count =0
            for file in self.fileTray:
                    filename = os.path.split(file)[-1]
                    item = QtWidgets.QTableWidgetItem()
                    self.tableView.setItem(loop_count, 0, item)
                    item.setText(filename)
                    item.setTextAlignment(QtCore.Qt.AlignCenter)
                    item.setFlags(QtCore.Qt.ItemIsEnabled)
                    loop_count +=1
        else:
            pass

    def GobackToHomePage(self):
        self.window = QtWidgets.QWidget()
        self.ui = HomePage.Ui_Form()
        self.ui.setupUi(self.window,self.CurrentUser, self.Role)
        self.window.show()


