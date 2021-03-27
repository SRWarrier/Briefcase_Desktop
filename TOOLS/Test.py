##from skimage. filters import threshold_local

import numpy as np

import cv2

#import imutils

def order_coordinates(pts):

            rectangle = np.zeros((4, 2), dtype = "float32")

            s = pts.sum(axis = 1)

            rectangle[0] = pts[np.argmin(s)]

            rectangle[2] = pts[np.argmax(s)]

            difference = np.diff(pts, axis = 1)

            rectangle[1] = pts[np.argmin(difference)]

            rectangle[3] = pts[np.argmax(difference)]

            return rectangle
def point_transform(image, pts):

            rect = order_coordinates(pts)

            (upper_left, upper_right, bottom_right, bottom_left) = rect

            width1 = np.sqrt(((bottom_right[0] - bottom_left[0]) ** 2) + ((bottom_right[1] - bottom_left[1]) ** 2))

            width2 = np.sqrt(((upper_right[0] - upper_left[0]) ** 2) +((upper_right[1] - upper_left[1]) ** 2))

            Width = max(int(width1), int(width2)) #considers maximum width value as Width

            height1 = np.sqrt(((upper_right[0] - bottom_right[0]) ** 2) +((upper_right[1] - bottom_right[1]) ** 2))

            height2 = np.sqrt(((upper_left[0] - bottom_left[0]) ** 2) + ((upper_left[1] - bottom_left[1]) ** 2))

            Height = max(int(height1), int(height2)) #considers maximum height value as Height

            distance = np.array([[0, 0],[Width - 1, 0],[Width - 1, Height - 1],[0,Height - 1]], dtype ="float32")

            Matrix = cv2.getPerspectiveTransform(rect, distance) 

            warped_image = cv2.warpPerspective(image, Matrix, (Width, Height))

            return warped_image
capture=cv2.VideoCapture(0)

while(True):

    ret,image=capture.read()

    image=cv2.imread('C:/Users/Warrier/Desktop/A4-Paper-PSD-MockUp-full1.jpg')

    ratio=image.shape[0]/image.shape[1]

    original = image.copy()

    image=cv2.resize(image,(500,500))

    gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

    gray=cv2.GaussianBlur(gray,(5,5),0)

    edged=cv2.Canny(gray,75,200)

    contours = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    #contours = imutils.grab_contours(contours )

    #contours = sorted(contours , key = cv2.contourArea, reverse = True)[:5]

    for ci in contours :

             #perimeter = cv2.arcLength(ci, True)

             approx = cv2.approxPolyDP(ci, 0.02 * perimeter, True)

             if len(approx) == 4:

                         screenCnt = approx

                         break

    warped = point_transform(original, screenCnt.reshape(4, 2) * ratio)

    warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)

##    T = threshold_local(warped, 11, offset = 10, method = "gaussian")
##
##    warped = (warped > T).astype("uint8") * 255

    cv2.imshow("Original", cv2.resize(original, height = 650))

    cv2.imshow("Scanned", imutils.resize(warped, height = 650))

    if cv2.waitKey(0):

        break

capture.release()

cv2.destroyAllWindows()
