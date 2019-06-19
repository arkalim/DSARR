# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np
import RPi.GPIO as GPIO
import pigpio
import os

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (480,368)
camera.framerate = 32
camera.vflip = True
camera.brightness = 65
rawCapture = PiRGBArray(camera, size=(480,368))

cmd = "sudo pigpiod"
os.system(cmd)
time.sleep(0.5)

GPIO.setmode(GPIO.BOARD)
pi = pigpio.pi()

Green = 5
Blue = 7
Red = 11
pan = 27
tilt = 22
L = 19
C = 21
R = 23
left_view = 0
right_view = 0
left = True
right = False
i = 0

GPIO.setup(Blue,GPIO.OUT)
GPIO.setup(Green,GPIO.OUT)
GPIO.setup(Red,GPIO.OUT)
GPIO.setup(L,GPIO.OUT)
GPIO.setup(C,GPIO.OUT)
GPIO.setup(R,GPIO.OUT)

pan_dc = 1450
tilt_dc = 1450

pi.set_servo_pulsewidth(pan,1450)
#pi.set_servo_pulsewidth(tilt,1450)

# allow the camera to warmup and some animation
time.sleep(0.1)
GPIO.output(Blue,True)
GPIO.output(Red,False)
GPIO.output(Green,False)
time.sleep(0.3)
GPIO.output(Blue,False)
GPIO.output(Red,True)
GPIO.output(Green,False)
time.sleep(0.1)

GPIO.output(Blue,True)
GPIO.output(Red,False)
GPIO.output(Green,False)
time.sleep(0.3)
GPIO.output(Blue,False)
GPIO.output(Red,True)
GPIO.output(Green,False)
time.sleep(0.1)
 
GPIO.output(Blue,True)
GPIO.output(Red,False)
GPIO.output(Green,False)
time.sleep(0.3)
GPIO.output(Blue,False)
GPIO.output(Red,True)
GPIO.output(Green,False)

GPIO.output(L,False)
GPIO.output(C,False)
GPIO.output(R,False)

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
     frame = frame.array
     
     hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
     lower_yellow = np.array([0,117,201])                 #select range of HSV values      
     upper_yellow = np.array([13,201,255])
     mask = cv2.inRange(hsv, lower_yellow, upper_yellow)   #mask the selected colour

     kernel = np.ones((3,3),np.uint8)                           
     opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)     #Morphological transformation (opening) to reduce noise

     _, contours,_ = cv2.findContours(opening,1,2)                #finding contours 
     if len(contours) == 0:
          GPIO.output(Red,True)
          GPIO.output(Blue,False)
          GPIO.output(Green,False)
          GPIO.output(L,False)
          GPIO.output(C,False)
          GPIO.output(R,False)
          print('stop')
          
          if(left == False and right == False and tilt_dc > 1550):
              if(i == 10):
                  GPIO.output(L,False)
                  GPIO.output(C,False)
                  GPIO.output(R,False)
                  print('stop')
                  left = True
                  right = False
                  tilt_dc = 1450
                  i=0 
              if(i < 10):
                  i += 1;
                  GPIO.output(L,True)
                  GPIO.output(C,False)
                  GPIO.output(R,True)
                  print('front')
          
          if(left == False and right == True):
              if(pan_dc >= 900 and left_view == 0 and right_view == 0):
                  pan_dc -= 100
              if(pan_dc <= 900):
                  left_view = 1

              if(pan_dc <= 2000 and left_view == 1 and right_view == 0):
                  pan_dc += 100    
              if(pan_dc >= 2000):
                  right_view = 1

              if(left_view == 1 and right_view == 1):
                  if(pan_dc < 1400):
                      pan_dc += 100
                  if(pan_dc > 1500):
                      pan_dc -= 100
                  if(pan_dc > 1400 and pan_dc < 1500):
                      left_view = 0
                      right_view = 0  
                      pan_dc = 1450
                      pi.set_servo_pulsewidth(pan,pan_dc)
                      GPIO.output(L,False)
                      GPIO.output(C,False)
                      GPIO.output(R,True)
                      print('right')
                      time.sleep(3)
                      GPIO.output(L,False)
                      GPIO.output(C,False)
                      GPIO.output(R,False)

          if(left == True and right == False):
              if(pan_dc <= 2000 and left_view == 0 and right_view == 0):
                  pan_dc += 100    
              if(pan_dc >= 2000):
                  right_view = 1
                  
              if(pan_dc >= 900 and left_view == 0 and right_view == 1):
                  pan_dc -= 100
              if(pan_dc <= 900):
                  left_view = 1

              if(left_view == 1 and right_view == 1):
                  if(pan_dc < 1400):
                      pan_dc += 100
                  if(pan_dc > 1500):
                      pan_dc -= 100
                  if(pan_dc > 1400 and pan_dc < 1500):
                      left_view = 0
                      right_view = 0  
                      pan_dc = 1450
                      pi.set_servo_pulsewidth(pan,pan_dc)
                      GPIO.output(L,True)
                      GPIO.output(C,False)
                      GPIO.output(R,False)
                      print('left')
                      time.sleep(3)
                      GPIO.output(L,False)
                      GPIO.output(C,False)
                      GPIO.output(R,False)
            
          pi.set_servo_pulsewidth(pan,pan_dc)
               
    
     for contour in contours:
         area = cv2.contourArea(contour)
         if area > 50:
             GPIO.output(Red,False)
             GPIO.output(Blue,False)
             GPIO.output(Green,True)
             
             cv2.drawContours(frame, contours,-1, (200,120,0), 2)
             (x,y),radius = cv2.minEnclosingCircle(contour)
             cv2.circle(frame,(int(x),int(y)),int(radius), (255,0,0), 2)
             
             if radius < 35:
                  GPIO.output(L,True)
                  GPIO.output(C,False)
                  GPIO.output(R,True)
                  print('forward')

             if y > 260:
                  GPIO.output(L,False)
                  GPIO.output(C,False)
                  GPIO.output(R,False)
                  print('stop')


             if x < 160 and pan_dc > 1000:
                  pan_dc -= 100
       
             if x > 320 and pan_dc < 2000:
                  pan_dc += 100

             if y < 120 and tilt_dc < 2000:
                  tilt_dc += 100

             if y > 240 and tilt_dc > 1000:
                  tilt_dc -= 100

             if pan_dc < 1350:
                  GPIO.output(L,False)
                  GPIO.output(C,False)
                  GPIO.output(R,True)
                  print('right')
                  right = True
                  left = False

             if pan_dc > 1550:
                  GPIO.output(L,True)
                  GPIO.output(C,False)
                  GPIO.output(R,False)
                  print('left')
                  left = True
                  right = False

             if pan_dc >= 1350 and pan_dc <= 1550:
                  right = False
                  left = False

                  
             pi.set_servo_pulsewidth(pan, pan_dc)
             print(pan_dc)
             
     
     # show the frame
     cv2.imshow('Frame',frame)
     key = cv2.waitKey(1) & 0xFF

     # clear the stream in preparation for the next frame
     rawCapture.truncate(0)
     
     # if the `q` key was pressed, break from the loop
     if key == ord("q"):
         break
GPIO.cleanup()
