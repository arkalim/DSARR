import numpy as np
import cv2

cap = cv2.VideoCapture(0)

cv2.namedWindow('Isolated Blob')

def nothing(x):
    pass

cv2.createTrackbar('lh', 'Isolated Blob', 0, 180, nothing)
cv2.createTrackbar('uh', 'Isolated Blob', 0, 180, nothing)
cv2.createTrackbar('ls', 'Isolated Blob', 0, 255, nothing)
cv2.createTrackbar('us', 'Isolated Blob', 0, 255, nothing)
cv2.createTrackbar('lv', 'Isolated Blob', 0, 255, nothing)
cv2.createTrackbar('uv', 'Isolated Blob', 0, 255, nothing)

while(1):
     _ , frame = cap.read()

     lh = cv2.getTrackbarPos('lh', 'Isolated Blob')
     uh = cv2.getTrackbarPos('uh', 'Isolated Blob')
     ls = cv2.getTrackbarPos('ls', 'Isolated Blob')
     us = cv2.getTrackbarPos('us', 'Isolated Blob')
     lv = cv2.getTrackbarPos('lv', 'Isolated Blob')
     uv = cv2.getTrackbarPos('uv', 'Isolated Blob')

     hsv = cv2.cvtColor(frame , cv2.COLOR_BGR2HSV)

     lower_pink = np.array([lh , ls , lv ])
     upper_pink = np.array([uh , us , uv ])

     mask = cv2.inRange(hsv , lower_pink , upper_pink)

     res = cv2.bitwise_and(frame , frame , mask = mask)

     cv2.imshow('video' , frame)
     cv2.imshow('Isolated Blob' , res)
     cv2.imshow('mask' , mask)

     k = cv2.waitKey(1) & 0xFF

     if k == ord('q'):
         break
     if k == ord('s'):
         print('lh : ' , lh)   
         print('uh : ' , uh)
         print('ls : ' , ls)
         print('us : ' , us)
         print('lv : ' , lv)
         print('uv : ' , uv)
    

cap.release()
cv2.destroyAllWindows()

    
     
                
