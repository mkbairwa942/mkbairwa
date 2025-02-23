import cv2
import numpy as np
print("package imported")

# IMAGE EXAMPLES

# cv2.imshow("Output",img)
# cv2.waitKey(1000)
# cap = cv2.VideoCapture(0)
# cap.set(10,150)

img = cv2.imread("D:\\STOCK\\Capital_vercel_new\\opencv_proj\\images\\lena.png")
kernel = np.ones((5,5),np.uint8)

cv2.imshow("Image",img)

imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
cv2.imshow("Grey Image",imgGray)

imgBlur = cv2.GaussianBlur(imgGray,(9,9),0)
cv2.imshow("Blur Image",imgBlur)

imgCanny = cv2.Canny(img,100,100)
cv2.imshow("Canny Image",imgCanny)

imgDialation = cv2.dilate(imgCanny,kernel,iterations=1)
cv2.imshow("Dialation Image",imgDialation)

imgEroded= cv2.dilate(imgDialation,kernel,iterations=1)
cv2.imshow("Eroded Image",imgEroded)

imgResize = cv2.resize(img,(200,300)) #WIDTH,HEIGHT
print("Resize Image Size is "+str(imgResize.shape))
cv2.imshow("Image1",imgResize)

imgCropped = img[0:200,100:300] #HEIGHT,WIDTH
print("Cropped Image Size is "+str(imgCropped.shape))
cv2.imshow("Image2",imgCropped)
cv2.waitKey(0)
