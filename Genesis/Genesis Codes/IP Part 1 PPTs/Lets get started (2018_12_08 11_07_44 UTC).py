import cv2

# loading the image as coloured image
image = cv2.imread(r'C:\Users\Lenovo\Desktop\mypic.jpg' , 1)

# displaying the image
cv2.imshow('image ', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
