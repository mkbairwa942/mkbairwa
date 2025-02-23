import cv2
import numpy as np

def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver

width,height = 500,500

img1 = cv2.imread("D:\\STOCK\\Capital_vercel_new\\static\\img\\testimonials\\scott-gummerson-JRuw7msjxds-unsplash.jpg")
img2 = cv2.imread("D:\\STOCK\Capital_vercel_new\\static\\img\\testimonials\\testimonials-5.jpg")

imgResize1 = cv2.resize(img1,(500,500))
imgResize2 = cv2.resize(img2,(500,500))

pts1 = np.float32([[111,219],[287,188],[154,482],[354,440]])
pts1 = np.float32([[100,100],[287,188],[154,482],[354,440]])
pts2 = np.float32([[0,0],[width,0],[0,height],[width,height]])
matrix = cv2.getPerspectiveTransform(pts1,pts2)
imgOutput = cv2.warpPerspective(imgResize1,matrix,(width,height),1,1)

cv2.imshow("Image1",imgResize1)
cv2.imshow("Image2",imgResize2)
cv2.imshow("Image3",imgOutput)

imgHor = np.hstack((imgResize1,imgResize2,imgResize1,imgResize2))
# imgResize11 = cv2.resize(imgHor,(500,250))
# cv2.imshow("Image4",imgResize11)

imgVer = np.vstack((imgResize1,imgResize2,imgResize1,imgResize2))
# imgResize22 = cv2.resize(imgVer,(250,500))
# cv2.imshow("Image5",imgResize22)
# cv2.waitKey(0)
imgGray = cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)

imgStack = stackImages(0.5,([imgResize1,imgGray,imgResize2],[imgGray,imgResize1,imgResize2]))
cv2.imshow("Horizontal",imgHor)
cv2.imshow("Vertical",imgVer)
cv2.imshow("ImageStack",imgStack)
cv2.waitKey(0)
