from PySide2 import QtWidgets, QtUiTools,QtCore, QtGui
from PIL import Image
import os
from io import BytesIO
import sys


class Ui_Form(object):
    def app(self, ImageResizer,CurrentUser, Role):
        ImageResizer.setObjectName("ImageResizer")
        ImageResizer.setWindowModality(QtCore.Qt.ApplicationModal)
        ImageResizer.setFixedSize(800, 650)
        ImageResizer.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.CurrentUser = CurrentUser
        self.Role = Role
        self.size_selected='KiloBytes'
        self.fileTray = []
        self.gridLayout = QtWidgets.QGridLayout(ImageResizer)
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton_3 = QtWidgets.QPushButton(ImageResizer)
        self.pushButton_3.setStyleSheet("background-color: rgb(85, 170, 0);\n"
"font: 12pt \"AvantGarde LT Medium\";\n"
"color: rgb(255, 255, 255);")
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.CompresstoSize)
        self.gridLayout.addWidget(self.pushButton_3, 4, 0, 1, 1)
        self.pushButton_4 = QtWidgets.QPushButton(ImageResizer)
        self.pushButton_4.setStyleSheet("background-color: rgb(134, 23, 133);\n"
"font: 12pt \"AvantGarde LT Medium\";\n"
"color: rgb(255, 255, 255);")
        self.pushButton_4.setObjectName("pushButton_3")
        self.pushButton_4.clicked.connect(self.Clear_table)
        self.gridLayout.addWidget(self.pushButton_4, 5, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(ImageResizer)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton = QtWidgets.QPushButton(ImageResizer)
        self.pushButton.setStyleSheet("background-color: rgb(85, 170, 255);\n"
"color: rgb(255, 255, 255);\n"
"font: 12pt \"AvantGarde LT Medium\";")
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.SelectFile)
        self.horizontalLayout.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(ImageResizer)
        self.pushButton_2.setStyleSheet("background-color: rgb(255, 0, 0);\n"
"font: 12pt \"AvantGarde LT Medium\";\n"
"color: rgb(255, 255, 255);")
        self.pushButton_2.setFlat(False)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.SelectFiles)
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.tableWidget = QtWidgets.QTableWidget(ImageResizer)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(155)
        self.tableWidget.horizontalHeader().setSectionResizeMode(155)
        self.horizontalLayout_5.addWidget(self.tableWidget)
        
        self.gridLayout.addLayout(self.horizontalLayout_5, 3, 0, 1, 1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(ImageResizer)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.lineEdit = QtWidgets.QLineEdit(ImageResizer)
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setText("100")
        self.horizontalLayout_2.addWidget(self.lineEdit)
        self.comboBox = QtWidgets.QComboBox(ImageResizer)
        self.comboBox.setStyleSheet("selection-color: rgb(0, 0, 0);")
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setCurrentIndex(1)
        self.comboBox.activated.connect(self.size_selection)
        self.horizontalLayout_2.addWidget(self.comboBox)
        self.label_4 = QtWidgets.QLabel(ImageResizer)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_2.addWidget(self.label_4)
        self.lineEdit_2 = QtWidgets.QLineEdit(ImageResizer)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_2.setText("Actual")
        self.horizontalLayout_2.addWidget(self.lineEdit_2)
        self.label_5 = QtWidgets.QLabel(ImageResizer)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_2.addWidget(self.label_5)
        self.lineEdit_3 = QtWidgets.QLineEdit(ImageResizer)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.lineEdit_3.setText("Actual")
        self.horizontalLayout_2.addWidget(self.lineEdit_3)
        self.horizontalLayout_3.addLayout(self.horizontalLayout_2)
        self.gridLayout.addLayout(self.horizontalLayout_3, 2, 0, 1, 1)
        self.progress = QtWidgets.QProgressBar(ImageResizer)
        self.progress.setGeometry(200, 80, 250, 20)
        self.gridLayout.addWidget(self.progress, 7, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(ImageResizer)
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 6, 0, 1, 1)
        self.label_2.raise_()
        self.label_3.raise_()
        self.pushButton_3.raise_()

        self.retranslateUi(ImageResizer)
        QtCore.QMetaObject.connectSlotsByName(ImageResizer)

    def retranslateUi(self, ImageResizer):
        _translate = QtCore.QCoreApplication.translate
        ImageResizer.setWindowTitle(_translate("ImageResizer", "Compress Images"))
        self.pushButton_3.setText(_translate("ImageResizer", "Resize"))
        self.pushButton_4.setText(_translate("ImageResizer", "Clear"))
        self.label_3.setText(_translate("ImageResizer", "<html><head/><body><p><span style=\" font-size:11pt; font-weight:600;\">RESIZE IMAGES</span></p></body></html>"))
        self.pushButton.setText(_translate("ImageResizer", "Single Image"))
        self.pushButton_2.setText(_translate("ImageResizer", "Batch Images"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("ImageResizer", "File Name"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("ImageResizer", "File Shape"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("ImageResizer", "Size"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("ImageResizer", "Quality"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("ImageResizer", "Status"))

        self.label.setText(_translate("ImageResizer", "<html><head/><body><p>Size</p></body></html>"))
        self.comboBox.setItemText(0, _translate("ImageResizer", "Bytes"))
        self.comboBox.setItemText(1, _translate("ImageResizer", "KiloBytes"))
        self.comboBox.setItemText(2, _translate("ImageResizer", "MegaBytes"))
        self.label_4.setText(_translate("ImageResizer", "Height"))
        self.label_5.setText(_translate("ImageResizer", "Width"))
        self.label_2.setText(_translate("ImageResizer", "<html><head/><body><p>Resized images are in the source folder under folder named \'Resized\'</p></body></html>"))


    def size_selection(self,index):
        self.size_selected=(self.comboBox.itemText(index))
        
        
    def CompresstoSize(self):
        if len(self.fileTray)!=0:
            self.progress.setValue(0)
            xfile = self.Imagefile
            size = self.to_bytes()        
            if isinstance(xfile,str):
                    xfile = [xfile]
            loop_count=0
            for file in xfile:
                    filename = os.path.split(file)[-1]
                    dfilename = filename
                    folder = os.path.dirname(file)
                    imgsize = (os.stat(file).st_size)
                    picture = Image.open(file)
                    Img_Type = picture.format
                    print(Img_Type)
                    if not os.path.isdir(os.path.join(folder,'Resized')):
                        os.mkdir(os.path.join(folder,'Resized'))
                    dim = picture.size
                    xWidth,xHeight = dim
                    aspect = (int(self.lineEdit_3.text()) if self.lineEdit_3.text()!='Actual' else xWidth,int(self.lineEdit_2.text()) if self.lineEdit_2.text()!='Actual' else xHeight)
                    quality =100
                    resize_image = picture.resize(aspect)
                    if resize_image.mode =='RGBA':
                        remove_Alpha = Image.new("RGB", resize_image.size, (255, 255, 255))
                        remove_Alpha.paste(resize_image, mask=resize_image.split()[3])
                        resize_image = remove_Alpha
                    while imgsize> self.to_bytes():
                            tempstore = BytesIO()
                            resize_image.save(tempstore,'JPEG',optimize=True,quality=quality)
                            imgsize = (tempstore.tell())
                            print(imgsize, ' & ', self.to_bytes())
                            if imgsize< self.to_bytes() or quality ==1:
                                    break
                            else:
                                    quality -=1
                    
                    item = QtWidgets.QTableWidgetItem()
                    self.tableWidget.setItem(loop_count, 1, item)
                    item.setText(str(dim))
                    item.setTextAlignment(QtCore.Qt.AlignCenter)
                    item.setFlags(QtCore.Qt.ItemIsEnabled)
                    
                    item = QtWidgets.QTableWidgetItem()
                    self.tableWidget.setItem(loop_count, 2, item)
                    item.setText(self.format_bytes(imgsize))
                    item.setTextAlignment(QtCore.Qt.AlignCenter)
                    item.setFlags(QtCore.Qt.ItemIsEnabled)
                    
                    item = QtWidgets.QTableWidgetItem()
                    self.tableWidget.setItem(loop_count, 3, item)
                    item.setText(str(quality))
                    item.setTextAlignment(QtCore.Qt.AlignCenter)
                    item.setFlags(QtCore.Qt.ItemIsEnabled)
                    
                    item = QtWidgets.QTableWidgetItem()
                    self.tableWidget.setItem(loop_count, 4, item)
                    item.setText('SAVED')
                    item.setTextAlignment(QtCore.Qt.AlignCenter)
                    item.setFlags(QtCore.Qt.ItemIsEnabled)

                    loop_count +=1
                    progress_pc = (loop_count/len(xfile)*100)
                    self.progress.setValue(progress_pc)
                    resize_image.save(os.path.join(folder,'Resized',"Resized"+filename),'JPEG',optimize=True,quality=quality)

        else:
            pass
    def format_bytes(self,size):
            if self.size_selected == 'KiloBytes':
                resultVal = round(float(size)/1024,2)
                ext = 'KB'
            elif self.size_selected == 'MegaBytes':
                resultVal = round(float(size)/(1024*1024),2)
                ext = 'MB'
            else:
                resultVal = round(float(size),2)
                ext = 'B'
                
            return str(resultVal)+' '+ext
        
    def to_bytes(self):
        if self.size_selected == 'KiloBytes':
            bytesVal = float(self.lineEdit.text())*1024
        elif self.size_selected == 'MegaBytes':
            bytesVal = float(self.lineEdit.text())*(1024*1024)
        else:
            bytesVal = float(self.lineEdit.text())
        return bytesVal
            

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

    def displayTable(self):
        if len(self.fileTray)!=0:
            self.tableWidget.setRowCount(0)
            self.tableWidget.setRowCount(len(self.fileTray))
            loop_count =0
            for file in self.fileTray:
                    filename = os.path.split(file)[-1]
                    item = QtWidgets.QTableWidgetItem()
                    self.tableWidget.setItem(loop_count, 0, item)
                    item.setText(filename)
                    item.setTextAlignment(QtCore.Qt.AlignCenter)
                    item.setFlags(QtCore.Qt.ItemIsEnabled)
                    loop_count +=1
        else:
            pass

        
            
    def Clear_table(self):
        self.tableWidget.setRowCount(0)
        self.fileTray = []

    def GobackToHomePage(self):
        self.window = QtWidgets.QWidget()
        self.ui = HomePage.Ui_Form()
        self.ui.setupUi(self.window,self.CurrentUser, self.Role)
        self.window.show()
##def main():
##    import sys
##    #app = QtWidgets.QApplication(sys.argv)
##    ImageResizer = QtWidgets.QWidget()
##    ui = ImageResizer()
##    ui.app(ImageResizer)
##    ImageResizer.show()
##    sys.exit(app.exec_())

