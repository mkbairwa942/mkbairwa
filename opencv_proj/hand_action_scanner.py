import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector
import math
import time


cap = cv2.VideoCapture(0)
cap.set(3,640) #width
cap.set(4,480) #height
cap.set(10,100) #bightness

detector = HandDetector(detectionCon=0.5, maxHands=2)
offset = 20
imageSize = 400

folder = "D:\\STOCK\\Capital_vercel_new\\opencv_proj\\Scanned\\D"
#cv2.imwrite("D:\\STOCK\\Capital_vercel_new\\opencv_proj\\Scanned\\NoPlate_"+str(count)+".jpg",imgRoi)

counter = 0
while True:
    #time.sleep(2)
    success, img = cap.read()
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
            else :
                k = imageSize/w
                hCal = math.ceil(k*h)
                imgResize = cv2.resize(imgCrop,(imageSize,hCal))
                imgResizeShape = imgResize.shape
                hGap = math.ceil((imageSize-hCal)/2)
                imgWhite[hGap:hCal+hGap,:]= imgResize    

            cv2.imshow("imgCrop",imgCrop)
            cv2.imshow("imgWhite",imgWhite)

        except Exception as e:
            print(e)   
    cv2.imshow("Image",img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    if cv2.waitKey(1) & 0xFF == ord('s'):
        counter +=1
        cv2.imwrite(f'{folder}\\HandImage_{counter}.jpg',imgWhite)
        print(counter)

    # if 0xFF == ord('s'):
    #     cv2.imwrite("D:\\STOCK\\Capital_vercel_new\\opencv_proj\\Scanned\\HandImage_"+str(counter)+".jpg",imgWhite)
    #     #cv2.rectangle(img,(0,200),(640,300),(0,255,0),cv2.FILLED)
    #     cv2.putText(img,"Scan Saved",(150,265),cv2.FONT_HERSHEY_DUPLEX,2,(0,0,255),2)
    #     cv2.imshow("Result",img)
    #     cv2.waitKey(1)
    #     counter +=1
    #     print(counter)

    # print("111")
    # print("222")
