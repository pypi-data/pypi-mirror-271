from ultralytics import YOLO
import cv2
model = YOLO('yolov8n-pose.pt')
d = cv2.imread('man.jpg')
results = model(d, save=True, conf=0.6)