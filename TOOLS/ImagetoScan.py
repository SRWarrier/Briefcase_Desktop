from PySide2 import QtWidgets, QtUiTools,QtCore, QtGui
import sys
import HomePage
import cv2
import numpy as np
from functions import pyside_dynamic
from PIL import Image, ImageChops
import os



class Ui(QtWidgets.QWidget):
    def __init__(self):
        super(Ui, self).__init__()
        pyside_dynamic.loadUi('../Resources/ui/ImagetoScan.ui', self)
        self.ButtonOpenImage.clicked.connect(self.OpenFile)
        self.PreviewOriginalView = self.findChild(QtWidgets.QLabel, 'PreviewOriginalView')
        self.PreviewExtendedView = self.findChild(QtWidgets.QLabel, 'PreviewExtendedView')
        self.buttonSharpen = self.findChild(QtWidgets.QCheckBox, 'buttonSharpen')
        self.buttonSharpen.clicked.connect(self.Sharpen)
        self.buttonRotate = self.findChild(QtWidgets.QPushButton, 'buttonRotate')
        self.buttonRotate.clicked.connect(self.rotateImage)
        self.RetryButton = self.findChild(QtWidgets.QPushButton, 'RetryButton')
        self.RetryButton.clicked.connect(self.restart)
        self.SaveButton = self.findChild(QtWidgets.QPushButton, 'SaveButton')
        self.SaveButton.clicked.connect(self.saveImage)
        self.buttonRotate = self.findChild(QtWidgets.QPushButton, 'buttonRotate')
        self.buttonRotate.clicked.connect(self.rotateImage)
        self.backtohome = self.findChild(QtWidgets.QPushButton, 'backtohome')
        self.backtohome.clicked.connect(self.GobackToHomePage)
        

    def OpenFile(self):
        try:
            self.PreviewOriginalView.setText('')
            self.PreviewExtendedView.setText('')
            self.fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self.ButtonOpenImage,"Open an Image file", "","Image File (*.jpg *.png *.jpeg)")
            originalImage = QtGui.QPixmap(self.fileName)
            self.PreviewOriginalView.setPixmap(originalImage)
            self.PreviewOriginalView.setScaledContents(True)
            self.OutputImage = Scanner()
            self.OutputArray = self.OutputImage.getImage(self.fileName)
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
        except:
            pass
        
    def restart(self):
        try:
            self.OutputArray = self.OutputImage.getImage(self.fileName)
            self.Sharpen()
        except:
            pass

    def GobackToHomePage(self):
        self.hide()
        self.ui = HomePage.Ui()


class Scanner():
    def getImage(self,img):
        self.cordinates = []
        image = Image.open(img, 'r')
        image = self.cut_the_white(image)
        image.show()
        image = np.array(image)
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
        (thresh, dst) = cv2.threshold(dst, 190, 255, cv2.THRESH_BINARY)
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
        output = clahe.apply(dst)
        return output
        

    
    def cut_the_white(self, letter):
        background = Image.new(letter.mode, letter.size, 255)
        diff = ImageChops.difference(letter, background)
        bbox = diff.getbbox()
        return letter.crop(bbox)
        
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


