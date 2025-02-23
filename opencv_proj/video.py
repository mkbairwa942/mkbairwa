import cv2
print("package imported")

# VIDEO EXAMPLES

video_clip = cv2.VideoCapture("C:\\Users\\h\\OneDrive\\Desktop\\Viddeo.mp4")
while True:
    sucess,imgg = video_clip.read()
    cv2.imshow("Video",imgg)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

vebcam = cv2.VideoCapture(0)
vebcam.set(3,640) #width
vebcam.set(4,480) #height
vebcam.set(10,100) #bightness

while True:
    sucess,imggg = vebcam.read()
    cv2.imshow("Video",imggg)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break