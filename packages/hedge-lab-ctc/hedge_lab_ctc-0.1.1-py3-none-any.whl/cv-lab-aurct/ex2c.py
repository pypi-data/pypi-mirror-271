import cv2
import numpy as np
img = cv2.imread('image.jpg')
img_cvt = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, timg = cv2.threshold(img_cvt, 127, 255, cv2.THRESH_BINARY)


cont , hie = cv2.findContours(timg, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
img_copy = img.copy()
cv2.drawContours(img_copy, cont, -1, (0, 255, 0), 2, cv2.LINE_AA)


img2 = img.copy()
detector = cv2.SimpleBlobDetector_create()
keyss = detector.detect(img2)
imk = cv2.drawKeypoints(img2, keyss, None, (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

cv2.imshow("threshold",timg)
cv2.waitKey(0)

cv2.imshow("Contours",img_copy)
cv2.waitKey(0)

cv2.imshow("blob", imk)
cv2.waitKey(0)

cv2.destroyAllWindows()
