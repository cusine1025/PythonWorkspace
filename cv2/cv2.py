import cv2
img = cv2.VideoCapture(0)

while(1):
    ret, frame = img.read()
    canny = cv2.Canny(frame,100,200)
    cv2.imshow('image', canny)
    if cv2.waitKey(5) == 27:
        break