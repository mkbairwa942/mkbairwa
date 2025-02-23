import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector #1.5.6 #mediapipe 0.8.10.1
from cvzone.ClassificationModule import Classifier
import math
import time
import tensorflow #2.9.1
import keras

print(keras.__version__)
print(tensorflow.__version__)

cap = cv2.VideoCapture(0)
cap.set(3,640) #width
cap.set(4,480) #height
cap.set(10,100) #bightness

detector = HandDetector(detectionCon=0.5, maxHands=2)
classifier = Classifier("D:\\STOCK\\Capital_vercel_new\\opencv_proj\\model\\keras_model.h5","D:\\STOCK\\Capital_vercel_new\\opencv_proj\\model\\labels.txt")
offset = 20
imageSize = 400

folder = "D:\\STOCK\\Capital_vercel_new\\opencv_proj\\Scanned\\D"
#cv2.imwrite("D:\\STOCK\\Capital_vercel_new\\opencv_proj\\Scanned\\NoPlate_"+str(count)+".jpg",imgRoi)

counter = 0
labels = ["A","B","C","D"]

while True:
    #time.sleep(2)
    success, img = cap.read()
    imgOutput = img.copy()
    hands, img = detector.findHands(img)
    if hands:
        try:
            hand = hands[0]
            x,y,w,h = hand['bbox']

            imgWhite = np.ones((imageSize,imageSize,3),np.uint8)*255
            imgCrop = img[y-offset:y+h+offset,x-offset:x+w+offset]
            
            
            aspectRatio = h/w
            if aspectRatio > 1:
                k = imageSize/h
                wCal = math.ceil(k*w)
                imgResize = cv2.resize(imgCrop,(wCal,imageSize))
                imgResizeShape = imgResize.shape
                wGap = math.ceil((imageSize-wCal)/2)
                imgWhite[:,wGap:wCal+wGap]= imgResize
                prediction,index = classifier.getPrediction(imgWhite,draw=False)
                print(prediction,index)
                
            else :
                k = imageSize/w
                hCal = math.ceil(k*h)
                imgResize = cv2.resize(imgCrop,(imageSize,hCal))
                imgResizeShape = imgResize.shape
                hGap = math.ceil((imageSize-hCal)/2)
                imgWhite[hGap:hCal+hGap,:]= imgResize  
                prediction,index = classifier.getPrediction(imgWhite,draw=False)  
            cv2.rectangle(imgOutput, (x - offset, y - offset-50),
                      (x - offset+90, y - offset-50+50), (255, 0, 255), cv2.FILLED)
            cv2.putText(imgOutput, labels[index], (x, y -26), cv2.FONT_HERSHEY_COMPLEX, 1.7, (255, 255, 255), 2)
            cv2.rectangle(imgOutput, (x-offset, y-offset),
                      (x + w+offset, y + h+offset), (255, 0, 255), 4)
            cv2.imshow("imgCrop",imgCrop)
            cv2.imshow("imgWhite",imgWhite)

        except Exception as e:
            print(e)   
    # cv2.rectangle(imgOutput,(x-offset,y-offset-50),(x-offset+90,y-offset-50+50),(255,0,255),4)
    # cv2.imshow("Image",imgOutput,labels[index],(x,y-30),cv2.FONT_HERSHEY_COMPLEX,1.7,(255,255,255),2)
    # cv2.rectangle(imgOutput,(x-offset,y-offset),(x+w+offset,y+h+offset),(255,0,255),4)
    cv2.imshow("Image", imgOutput)
    cv2.waitKey(1)


