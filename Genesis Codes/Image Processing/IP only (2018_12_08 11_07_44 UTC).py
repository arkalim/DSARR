import cv2
import numpy as np

cam = cv2.VideoCapture(0)

ll = np.array([25,80,1])                       # for ball
ul = np.array([42,255 ,137])


cv2.namedWindow('Isolated Contour')

background = np.zeros((480,640,3), np.uint8)

kernel = np.ones((3,3))

draw = False
lift = 1

while True:
    _, frame = cam.read()
    frame = cv2.flip(frame, 1)
    blur = cv2.GaussianBlur(frame, (15,15) , 0)
    frame = cv2.morphologyEx(frame, cv2.MORPH_OPEN, kernel)
    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, ll, ul)
    res = cv2.bitwise_or(frame,frame, mask=mask)

    im2, contours, hierarchy = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    maxarea = 0

    try:
        c = max(contours, key = cv2.contourArea)
        if cv2.contourArea(c) > 150:
            
            (xcirc , ycirc) , radius = cv2.minEnclosingCircle(c)
            center = (int(xcirc) , int(ycirc))
            radius = int(radius)

            xdraw = int(xcirc)
            ydraw = int(ycirc)

            print(xdraw , ydraw)
            
            cv2.circle(res , center , radius , (255 , 0 ,0) , 3)
            cv2.circle(res , center , 1 , (0,255,0) , 4)

            
            if draw == True:
                cv2.line(background ,(xdraw,ydraw),(xdraw+1,ydraw+1),(0,255,0),8)

    except:
        pass

    cv2.imshow('Live Feed',frame)
    cv2.imshow('Isolated Contour' , res)
    cv2.imshow('black ' , background)  

    key = cv2.waitKey(1)
    if key == ord('u') & 0xFF:
        print('pen lifted')
        lift = 1
        draw = False
        
    if key == ord('d') & 0xFF:
        print('pen dropped')
        lift = 0
        draw = True
            
    if key == ord('q') & 0xFF:
        break
    if key == ord('c') & 0xFF:
        background = np.zeros((480,640,3), np.uint8)
        print('screen cleared')

cam.release()
cv2.destroyAllWindows()
