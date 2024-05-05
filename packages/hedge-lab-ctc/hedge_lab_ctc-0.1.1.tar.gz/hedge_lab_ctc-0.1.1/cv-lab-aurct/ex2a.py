import cv2
import numpy as np
img = cv2.imread('image.jpg')
resize_img = cv2.resize(img ,(300,200))
cv2.imshow("",resize_img)
cv2.waitKey(0)
cv2.destroyAllWindows()