import numpy as np
import cv2
faceCascade = cv2.CascadeClassifier('C:\\Users\\gram_\\AppData\\Roaming\\Python\\Python310\\site-packages\\cv2\\data\\haarcascade_frontalface_default.xml')



gray_image = cv2.imread("C:\\Users\\gram_\\OneDrive\\바탕 화면\\PythonWorkspace\\cv2\\img.jpg")

gray = cv2.cvtColor(gray_image, cv2.COLOR_BGR2GRAY)

faces = faceCascade.detectMultiScale(gray, scaleFactor=1.05, minNeighbors=5, minSize=(100,100), flags=cv2.CASCADE_SCALE_IMAGE)

for (x, y, w, h) in faces:
    cv2.rectangle(gray, (x,y), (x+w, y + h), (255,0,0), 2)

cv2.imshow('img', gray)
cv2.waitkey(0)
cv2.destroyAllWindows()