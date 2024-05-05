import cv2

import numpy as np

img = cv2.imread('imageex5_.png')
img2 = cv2.imread('imageex5_.png')

orb = cv2.ORB_create()
keypoints, descriptors = orb.detectAndCompute(img, None)
image_with_keypoints = cv2.drawKeypoints(img, keypoints, None)

cv2.imshow(" ", image_with_keypoints)
cv2.waitKey(0)

imgg = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
img2g = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

orb = cv2.ORB_create()
queryKeypoints, queryDescriptors = orb.detectAndCompute(imgg,None)
trainKeypoints, trainDescriptors = orb.detectAndCompute(img2g,None)

matcher = cv2.BFMatcher()
matches = matcher.match(queryDescriptors,trainDescriptors)
final_img = cv2.drawMatches(img, queryKeypoints, img2, trainKeypoints, matches[:20],None)

final_img = cv2.resize(final_img, (1000,650))

cv2.imshow(" ", final_img)
cv2.waitKey(0)
src_pts = np.float32([queryKeypoints[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
dst_pts = np.float32([trainKeypoints[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)
M, _ = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
result = cv2.warpPerspective(img, M, (img2.shape[1], img2.shape[0]))

cv2.imshow("", result)
cv2.waitKey(0)
cv2.destroyAllWindows()