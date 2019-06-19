from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np

cv2.namedWindow('image')

def nothing(x):
    pass

# create trackbars for color change
cv2.createTrackbar('H_lower','image',0,180,nothing)
cv2.createTrackbar('H_upper','image',0,180,nothing)
cv2.createTrackbar('S_lower','image',0,255,nothing)
cv2.createTrackbar('S_upper','image',0,255,nothing)
cv2.createTrackbar('V_lower','image',0,255,nothing)
cv2.createTrackbar('V_upper','image',0,255,nothing)

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (480,368)
camera.framerate = 15
camera.vflip = True
camera.brightness = 65
rawCapture = PiRGBArray(camera, size=(480,368))

# allow the camera to warmup and some animation
time.sleep(0.1)

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    frame = frame.array

    # get current positions of four trackbars
    H_lower = cv2.getTrackbarPos('H_lower','image')
    H_upper = cv2.getTrackbarPos('H_upper','image')
    S_lower = cv2.getTrackbarPos('S_lower','image')
    S_upper = cv2.getTrackbarPos('S_upper','image')
    V_lower = cv2.getTrackbarPos('V_lower','image')
    V_upper = cv2.getTrackbarPos('V_upper','image') 
    
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    lower_color = np.array([H_lower,S_lower,V_lower])                 
    upper_color = np.array([H_upper,S_upper,V_upper])
    mask = cv2.inRange(hsv, lower_color, upper_color)   #mask the selected colour

    cv2.imshow('mask',mask)                           #black and white masking of the selected colour
    key = cv2.waitKey(1) & 0xFF

    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)
     
    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break
