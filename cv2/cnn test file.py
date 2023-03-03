import numpy as np
import cv2
faceCascade = cv2.CascadeClassifier('cv2\\haarcascade_frontalface_default.xml')

def detect(gray, frame):
    faces = faceCascade.detectMultiScale(gray, scaleFactor=1.05, minNeighbors=5,
    minSize=(100,100), flags=cv2.CASCADE_SCALE_IMAGE)
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x,y), (x+w, y + h), (255,0,0), 2)
    return frame

gray_image = cv2.imread("C:\\AnyMP4 Studio\\tnwjd.jpg")

gray = cv2.cvtColor(gray_image, cv2.COLOR_BGR2GRAY)

canvas = detect(gray, gray_image)

cv2.imshow('img', canvas)
cv2.waitKey(0)
cv2.destroyAllWindows()