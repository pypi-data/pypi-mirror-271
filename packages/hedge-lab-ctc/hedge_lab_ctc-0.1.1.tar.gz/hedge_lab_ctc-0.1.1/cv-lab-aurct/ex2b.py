import cv2
import numpy as np
img = cv2.imread('image.jpg')
x , y, h, w = 100, 100, 200, 200
crop_img = img[y:y+h,x:x+h]
cv2.imshow("",crop_img)
cv2.waitKey(0)
cv2.destroyAllWindows()