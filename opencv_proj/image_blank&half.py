import cv2
import numpy as np

img = cv2.imread("D:\\STOCK\\Capital_vercel_new\\opencv_proj\\images\\lena.png")
print("Original Image Size is "+str(img.shape))

Blank_img = np.zeros((400,400,3),np.uint8)
print("Blank Image Size is "+str(Blank_img.shape))
cv2.imshow("Image1",Blank_img)

Blank_img[200:300,100:300] = 255,200,0
print("Half Image Size is "+str(Blank_img.shape))
cv2.imshow("Image2",Blank_img)

Blank_img[:] = 255,200,0
print("Whole Image Size is "+str(Blank_img.shape))
cv2.imshow("Image3",Blank_img)

cv2.line(Blank_img,(0,0),(300,300),(0,255,0),3) #STARTING POINT, ENDINGPOINT , COLOUR, LINE THIKNESS
cv2.imshow("Image4",Blank_img)

cv2.line(Blank_img,(0,0),(img.shape[1],img.shape[0]),(0,255,0),3) #STARTING POINT, ENDINGPOINT , COLOUR, LINE THIKNESS
cv2.imshow("Image5",Blank_img)

cv2.rectangle(Blank_img,(0,0),(250,350),(0,0,255),3) #STARTING POINT, ENDINGPOINT , COLOUR, LINE THIKNESS
cv2.imshow("Image6",Blank_img)

cv2.rectangle(Blank_img,(0,0),(250,350),(0,0,255),cv2.FILLED) #STARTING POINT, ENDINGPOINT , COLOUR, LINE THIKNESS
cv2.imshow("Image7",Blank_img)

cv2.circle(Blank_img,(400,50),30,(255,0,0),cv2.FILLED) #CENTER POINT, RADIUS , COLOUR, LINE THIKNESS
cv2.imshow("Image8",Blank_img)

cv2.putText(Blank_img,"OPENCV", (200,150) ,cv2.FONT_HERSHEY_COMPLEX,1,(200,0,0),3) #ORIGIN POINT, FONTFACE , FONTSCLAE,COLUR, THIKNESS
cv2.imshow("Image8",Blank_img)
cv2.waitKey(0)
