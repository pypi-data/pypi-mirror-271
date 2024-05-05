import numpy as np
import cv2

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

blobParams = cv2.SimpleBlobDetector_Params()
blobParams.minThreshold = 8
blobParams.maxThreshold = 255
blobParams.filterByArea = True
blobParams.minArea = 64
blobParams.maxArea = 2500
blobParams.filterByCircularity = True
blobParams.minCircularity = 0.1
blobParams.filterByConvexity = True
blobParams.minConvexity = 0.87
blobParams.filterByInertia = True
blobParams.minInertiaRatio = 0.01
blobDetector = cv2.SimpleBlobDetector_create(blobParams)

objp = np.zeros((44, 3), np.float32)
objp[:, :2] = np.indices((4, 11)).T.reshape(-1, 2) * 72

objpoints, imgpoints = [], []

cap = cv2.VideoCapture(2)
num, found = 10, 0

while found < num:
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    keypoints = blobDetector.detect(gray)
    im_with_keypoints = cv2.drawKeypoints(img, keypoints, np.array([]), (0,255,0), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    im_with_keypoints_gray = cv2.cvtColor(im_with_keypoints, cv2.COLOR_BGR2GRAY)
    ret, corners = cv2.findCirclesGrid(im_with_keypoints, (4,11), None, flags=cv2.CALIB_CB_ASYMMETRIC_GRID)

    if ret:
        objpoints.append(objp)
        corners2 = cv2.cornerSubPix(im_with_keypoints_gray, corners, (11,11), (-1,-1), criteria)
        imgpoints.append(corners2)
        found += 1
    cv2.imshow("img", im_with_keypoints)
    cv2.waitKey(2)

cap.release()
cv2.destroyAllWindows()

ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)


print('camera_matrix', mtx)
print('dist_coeff', dist)

