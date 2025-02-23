import cv2

faceCascade= cv2.CascadeClassifier("D:\STOCK\Capital_vercel_new\opencv_proj\haarcascades\haarcascade_frontalface_default.xml")
img = cv2.imread('D:\\STOCK\\Capital_vercel_new\\opencv_proj\\images\\team19.jpg')
imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

faces = faceCascade.detectMultiScale(imgGray,1.1,3)

for (x,y,w,h) in faces:
    cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)

img1= cv2.resize(img,(750,750))
cv2.imshow("Result", img1)
cv2.waitKey(0)