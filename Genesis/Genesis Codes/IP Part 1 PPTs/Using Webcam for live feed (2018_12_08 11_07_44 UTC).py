import cv2

# To start the camera 
cap = cv2.VideoCapture(0)

while (True) :
	# to capture a frame since video is nothing but images one after another
	_ , frame = cap.read()
	
	# lets convert it to gray scale
	gray = cv2.cvtColor(frame , cv2.COLOR_BGR2GRAY)
	
	# displaying the video as images 
	cv2.imshow(' show video ' , gray)
	cv2.imshow('  show colored' , frame)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break 

cap.release()
cv2.destroyAllWindows()
