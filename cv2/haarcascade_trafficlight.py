import numpy as np
import cv2
trafficlight_cascade = cv2.CascadeClassifier('C:\\Users\\gram_\\AppData\\Roaming\\Python\\Python310\\site-packages\\cv2\\data\\haarcascade_trafficlight.xml')

def detect(frame):

    light = trafficlight_cascade.detectMultiScale(frame, scaleFactor=1.05, minNeighbors=5, minSize=(100,100))

    for (x, y, w, h) in light:
        cv2.rectangle(frame, (x,y), (x+w, y + h), (255,0,0), 2)

    

    
    return frame

video_capture = cv2.VideoCapture(0)

while True:

    _, frame = video_capture.read()
    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    canvas = detect(frame)
    cv2.imshow('trafficlight_detected', canvas)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()