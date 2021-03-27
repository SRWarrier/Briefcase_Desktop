from PyQt5 import QtCore, QtGui, QtWidgets
import cv2
import numpy as np
from PIL import Image
import sys
import os
sys.path.append(os.path.abspath(os.path.join('..')))
import HomePage



class Ui_GetMeScanner(object):
    def setupUi(self, GetMeScanner,CurrentUser,Role):
        GetMeScanner.setObjectName("GetMeScanner")
        GetMeScanner.resize(800, 600)
        GetMeScanner.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.CurrentUser = CurrentUser
        self.Role = Role
        self.gridLayout_3 = QtWidgets.QGridLayout(GetMeScanner)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.Title = QtWidgets.QLabel(GetMeScanner)
        self.Title.setAlignment(QtCore.Qt.AlignCenter)
        self.Title.setObjectName("Title")
        self.gridLayout_3.addWidget(self.Title, 0, 0, 1, 1)
        self.frame = QtWidgets.QFrame(GetMeScanner)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.ButtonOpenImage = QtWidgets.QPushButton(self.frame)
        self.ButtonOpenImage.setObjectName("ButtonOpenImage")
        self.ButtonOpenImage.clicked.connect(self.OpenFile)
        self.horizontalLayout.addWidget(self.ButtonOpenImage)
        self.Addressbar = QtWidgets.QLineEdit(self.frame)
        self.Addressbar.setObjectName("Addressbar")
        self.horizontalLayout.addWidget(self.Addressbar)
        self.gridLayout_3.addWidget(self.frame, 1, 0, 1, 1)
        self.frame_2 = QtWidgets.QFrame(GetMeScanner)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.gridLayout = QtWidgets.QGridLayout(self.frame_2)
        self.gridLayout.setObjectName("gridLayout")
        self.previewOriginal = QtWidgets.QFrame(self.frame_2)
        self.previewOriginal.setMinimumSize(QtCore.QSize(351, 301))
        self.previewOriginal.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.previewOriginal.setFrameShadow(QtWidgets.QFrame.Raised)
        self.previewOriginal.setObjectName("previewOriginal")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.previewOriginal)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.PreviewOriginalView = QtWidgets.QLabel(self.previewOriginal)
        self.PreviewOriginalView.setText("")
        self.PreviewOriginalView.setObjectName("PreviewOriginalView")
        self.gridLayout_4.addWidget(self.PreviewOriginalView, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.previewOriginal, 1, 0, 1, 1)
        self.previewExtracted = QtWidgets.QFrame(self.frame_2)
        self.previewExtracted.setMinimumSize(QtCore.QSize(351, 301))
        self.previewExtracted.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.previewExtracted.setFrameShadow(QtWidgets.QFrame.Raised)
        self.previewExtracted.setObjectName("previewExtracted")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.previewExtracted)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.PreviewExtendedView = QtWidgets.QLabel(self.previewExtracted)
        self.PreviewExtendedView.setText("")
        self.PreviewExtendedView.setObjectName("PreviewExtendedView")
        self.gridLayout_5.addWidget(self.PreviewExtendedView, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.previewExtracted, 1, 1, 1, 1)
        self.labelOriginalImage = QtWidgets.QLabel(self.frame_2)
        self.labelOriginalImage.setAlignment(QtCore.Qt.AlignCenter)
        self.labelOriginalImage.setObjectName("labelOriginalImage")
        self.gridLayout.addWidget(self.labelOriginalImage, 0, 0, 1, 1)
        self.labelExtractedImage = QtWidgets.QLabel(self.frame_2)
        self.labelExtractedImage.setAlignment(QtCore.Qt.AlignCenter)
        self.labelExtractedImage.setObjectName("labelExtractedImage")
        self.gridLayout.addWidget(self.labelExtractedImage, 0, 1, 1, 1)
        self.buttonSharpen = QtWidgets.QCheckBox(self.frame_2)
        self.buttonSharpen.setTristate(False)
        self.buttonSharpen.setObjectName("buttonSharpen")
        self.buttonSharpen.stateChanged.connect(self.Sharpen)
        self.gridLayout.addWidget(self.buttonSharpen, 2, 1, 1, 2)
        self.RotateButton = QtWidgets.QPushButton(self.frame_2)
        self.RotateButton.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgb(76,175,80);")
        self.RotateButton.setObjectName("RotateButton")
        self.RotateButton.clicked.connect(self.rotateImage)
        self.gridLayout.addWidget(self.RotateButton, 2, 2, 2, 3)
        self.gridLayout_3.addWidget(self.frame_2, 2, 0, 1, 1)
        self.frame_3 = QtWidgets.QFrame(GetMeScanner)
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame_3)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.RetryButton = QtWidgets.QPushButton(self.frame_3)
        self.RetryButton.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgb(156,39,176);")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../Resources/Images/retry.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.RetryButton.setIcon(icon)
        self.RetryButton.setObjectName("RetryButton")
        self.RetryButton.clicked.connect(self.restart)
        self.gridLayout_2.addWidget(self.RetryButton, 1, 2, 1, 1)
        self.backtohome = QtWidgets.QPushButton(self.frame_3)
        self.backtohome.setStyleSheet("background-color:rgb(3,169,244);\n"
"color: rgb(255, 255, 255);")
        self.backtohome.setObjectName("backtohome")
        self.backtohome.clicked.connect(self.GobackToHomePage)
        self.gridLayout_2.addWidget(self.backtohome, 1, 0, 1, 1)
        self.SaveButton = QtWidgets.QPushButton(self.frame_3)
        self.SaveButton.setStyleSheet("color: rgb(255, 255, 255);\n"
"background-color: rgb(76,175,80);")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("../Resources/Images/save.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.SaveButton.setIcon(icon1)
        self.SaveButton.setObjectName("SaveButton")
        self.SaveButton.clicked.connect(self.saveImage)
        self.gridLayout_2.addWidget(self.SaveButton, 1, 3, 1, 1)
        self.gridLayout_3.addWidget(self.frame_3, 3, 0, 1, 1)

        self.retranslateUi(GetMeScanner)
        QtCore.QMetaObject.connectSlotsByName(GetMeScanner)

    def retranslateUi(self, GetMeScanner):
        _translate = QtCore.QCoreApplication.translate
        GetMeScanner.setWindowTitle(_translate("GetMeScanner", "GetMe Scanner"))
        self.Title.setText(_translate("GetMeScanner", "<html><head/><body><p><span style=\" font-size:14pt; font-weight:600; text-decoration: underline;\">GetMe Scanned Documents</span></p></body></html>"))
        self.ButtonOpenImage.setText(_translate("GetMeScanner", "Open Image"))
        self.labelOriginalImage.setText(_translate("GetMeScanner", "Original"))
        self.labelExtractedImage.setText(_translate("GetMeScanner", "Extracted"))
        self.buttonSharpen.setText(_translate("GetMeScanner", "Sharpen"))
        self.RetryButton.setText(_translate("GetMeScanner", "Retry"))
        self.backtohome.setText(_translate("GetMeScanner", "Back to Home"))
        self.SaveButton.setText(_translate("GetMeScanner", "Save"))
        self.RotateButton.setText(_translate("GetMeScanner", "Rotate"))

    def OpenFile(self):
        try:
            self.PreviewOriginalView.setText('')
            self.PreviewExtendedView.setText('')
            self.Addressbar.setText('')
            fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self.ButtonOpenImage,"Open an Image file", "","Image File (*.jpg *.png *.jpeg)")
            self.Addressbar.setText(fileName)
            originalImage = QtGui.QPixmap(fileName)
            self.PreviewOriginalView.setPixmap(originalImage)
            self.PreviewOriginalView.setScaledContents(True)
            self.OutputImage = Scanner()
            self.OutputArray = self.OutputImage.getImage(fileName)
            self.Sharpen()
        except:
            pass
        
    def Sharpen(self):
        try:
            if self.buttonSharpen.isChecked():
                kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
                output = cv2.filter2D(self.OutputArray, -1, kernel)
                cv2.imwrite('_temp/temp.jpg',output)
                outputImage = QtGui.QPixmap('_temp/temp.jpg')
                self.PreviewExtendedView.setPixmap(outputImage)
                self.PreviewExtendedView.setScaledContents(True)
            else:
                cv2.imwrite('_temp/temp.jpg',self.OutputArray)
                outputImage = QtGui.QPixmap('_temp/temp.jpg')
                self.PreviewExtendedView.setPixmap(outputImage)
                self.PreviewExtendedView.setScaledContents(True)
        except:
            pass

    def saveImage(self):
        try:
            fileName, filetype = QtWidgets.QFileDialog.getSaveFileName(self.ButtonOpenImage,"Save file", "","Image File (*.jpg *.png *.jpeg);;PDF File (*.pdf)")   
            print(type(filetype),filetype)
            print(os.path.splitext(fileName.lower())[1])
            if filetype=='PDF File (*.pdf)' or os.path.splitext(fileName.lower())[1]=='.pdf':
                print('saving to pdf')
                saveFile = Image.open('_temp/temp.jpg')
                saveFile.save(fileName,'PDF')
                
                            
            else:
                saveFile = Image.open('_temp/temp.jpg')
                saveFile.save(fileName,'JPEG')
        except:
            pass

##    def rotateImage(self):
##        try:
##            rotFile = Image.open('_temp/temp.jpg')
##            rotFile = rotFile.rotate(90)
##            rotFile.save('_temp/temp.jpg')
##            outputImage = QtGui.QPixmap('_temp/temp.jpg')
##            self.PreviewExtendedView.setPixmap(outputImage)
##            self.PreviewExtendedView.setScaledContents(True)
##        except:
##            pass

    def rotateImage(self):
        try:
            mat = cv2.imread('_temp/temp.jpg')
            height, width = mat.shape[:2] # image shape has 3 dimensions
            image_center = (width/2, height/2) # getRotationMatrix2D needs coordinates in reverse order (width, height) compared to shape

            rotation_mat = cv2.getRotationMatrix2D(image_center, 90, 1.)

            # rotation calculates the cos and sin, taking absolutes of those.
            abs_cos = abs(rotation_mat[0,0]) 
            abs_sin = abs(rotation_mat[0,1])

            # find the new width and height bounds
            bound_w = int(height * abs_sin + width * abs_cos)
            bound_h = int(height * abs_cos + width * abs_sin)

            # subtract old image center (bringing image back to origo) and adding the new image center coordinates
            rotation_mat[0, 2] += bound_w/2 - image_center[0]
            rotation_mat[1, 2] += bound_h/2 - image_center[1]

            # rotate image with the new bounds and translated rotation matrix
            rotated_mat = cv2.warpAffine(mat, rotation_mat, (bound_w, bound_h))
            cv2.imwrite('_temp/temp.jpg',rotated_mat)
            outputImage = QtGui.QPixmap('_temp/temp.jpg')
            self.PreviewExtendedView.setPixmap(outputImage)
            self.PreviewExtendedView.setScaledContents(True)
        except IndexError as e:
            pass
        
    def restart(self):
        NullPixamap = QtGui.QPixmap()
        self.PreviewOriginalView.setPixmap(NullPixamap)
        self.PreviewExtendedView.setPixmap(NullPixamap)
        os.remove('_temp/temp.jpg')
        self.OutputArray=''
        self.Addressbar.setText('')

    def GobackToHomePage(self):
        self.window = QtWidgets.QWidget()
        self.ui = HomePage.Ui_Form()
        self.ui.setupUi(self.window,self.CurrentUser,self.Role)
        self.window.show()

class Scanner():
    def getImage(self,img):
        self.cordinates = []
        image = cv2.imread(img)
        h,w,channels =image.shape
        if h>w:
            factor = h/740
        else:
            factor = w/740
        new_h,new_w = int(h/factor),int(w/factor)
        image = cv2.resize(image, (new_h, new_w))
        cv2.imshow('Select edges of the document', image)
        cv2.setMouseCallback('Select edges of the document', self.actions)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
        approx = self.rectify(np.array(self.cordinates))
        pts2 = np.float32([[0,0],[new_h,0],[new_h,new_w],[0,new_w]])

        M = cv2.getPerspectiveTransform(approx,pts2)
        dst = cv2.warpPerspective(image,M,(new_h,new_w))

        dst = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
        output = clahe.apply(dst)
        return output
        
        
        
    def rectify(self,h):
        h = h.reshape((4,2))
        hnew = np.zeros((4,2),dtype = np.float32)

        add = h.sum(1)
        hnew[0] = h[np.argmin(add)]
        hnew[2] = h[np.argmax(add)]

        diff = np.diff(h,axis = 1)
        hnew[1] = h[np.argmin(diff)]
        hnew[3] = h[np.argmax(diff)]
        return hnew


    def actions(self,event,x,y,flags,param):
        if event == cv2.EVENT_LBUTTONDOWN:
            location=(x,y)
            print(location)
            self.cordinates.append([list(location)])
            if len(self.cordinates)==4:
                cv2.destroyAllWindows()
                

        

                

