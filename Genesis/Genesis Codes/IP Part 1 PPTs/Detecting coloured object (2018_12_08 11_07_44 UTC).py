import numpy as np
import cv2

cap = cv2.VideoCapture(0)

while (True) :
    _ , frame = cap.read()
    
    # converting BGR to HSV	
    hsv = cv2.cvtColor(frame , cv2.COLOR_BGR2HSV)
    
    # now we need to define the blue color range in hsv	
    lower_blue = np.array( [ 110 , 50 , 50])
    upper_blue = np.array( [ 130 , 255 , 255])
	
    # now we will threshold the image to get blue colors only using lower_blue and upper_blue
    mask = cv2.inRange( hsv , lower_blue , upper_blue)

    # now to only show the blue cap we perform bitwise and operation
    final_result = cv2.bitwise_and( frame ,  frame , mask = mask )

    cv2.imshow(' video ', frame)
    cv2.imshow('masked image ' , mask)
    cv2.imshow(' resultant ' , final_result)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
