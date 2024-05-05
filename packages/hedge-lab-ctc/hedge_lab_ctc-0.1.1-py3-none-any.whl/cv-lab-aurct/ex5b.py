import cv2
import numpy as np
image = cv2.imread("image.jpg")
edges = cv2.Canny(image, 50, 150)
lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=100, minLineLength=100, maxLineGap=10)
for line in lines:
    x1, y1, x2, y2 = line[0]
    cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
cv2.imshow(" ",image)
cv2.waitKey(0)
cv2.destroyAllWindows()