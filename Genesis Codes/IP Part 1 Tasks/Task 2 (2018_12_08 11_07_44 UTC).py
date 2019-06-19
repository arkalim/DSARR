import cv2

cap = cv2.VideoCapture(0)

while(True) :
    _ , frame = cap.read()

    if cv2.waitKey(1) & 0xFF == ord('s'):
        cv2.imshow( ' image ' , frame )
        cv2.waitKey(0)

    cv2.imshow( ' frame ' , frame )
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
