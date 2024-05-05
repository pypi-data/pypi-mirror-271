import cv2
import numpy as np

class Tracker():
    def __init__(self, id, hsv_frame, track_window):
     
        self.id = id

        self.track_window = track_window
        self.term_crit = (cv2.TERM_CRITERIA_COUNT | cv2.TERM_CRITERIA_EPS, 10, 1)

        x, y, w, h = track_window
        roi = hsv_frame[y:y+h, x:x+w]
        roi_hist = cv2.calcHist([roi], [0, 2], None, [15, 16],[0, 180, 0, 256])
        self.roi_hist = cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)


        self.kalman = cv2.KalmanFilter(4, 2)
        

        self.kalman.measurementMatrix = np.array(
            [[1, 0, 0, 0],
             [0, 1, 0, 0]], np.float32)


        self.kalman.transitionMatrix = np.array(
            [[1, 0, 1, 0],
             [0, 1, 0, 1],
             [0, 0, 1, 0],
             [0, 0, 0, 1]], np.float32)

        self.kalman.processNoiseCov = np.array(
            [[1, 0, 0, 0],
             [0, 1, 0, 0],
             [0, 0, 1, 0],
             [0, 0, 0, 1]], np.float32) * 0.03

        cx = x+w/2
        cy = y+h/2
        
        self.kalman.statePre = np.array([[cx], [cy], [0], [0]], np.float32)
        
        self.kalman.statePost = np.array([[cx], [cy], [0], [0]], np.float32)
