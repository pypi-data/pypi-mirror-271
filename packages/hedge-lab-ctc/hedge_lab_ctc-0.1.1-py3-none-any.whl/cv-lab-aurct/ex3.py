import cv2
img = cv2.imread('image.jpg')

cv2.line(img, (100, 100), (300, 300), (0, 255, 0), 2)
cv2.rectangle(img, (200, 150), (400, 350), (255, 0, 0), 2)
cv2.circle(img, (300, 200), 50, (0, 0, 255), 2)
cv2.ellipse(img, (400, 250), (100, 50), 0, 0, 180, (255, 255, 0), 2)
cv2.putText(img, 'your_name', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)


cv2.imshow("",img)
cv2.waitKey(0)

cv2.destroyAllWindows()