import cv2
from ultralytics import YOLO

# Load the YOLOv8 pose detection model (adjust 'yolov8n-pose.pt' if using a different model)
model = YOLO("yolov8n-pose.pt")

# Initialize video capture object (0 for default camera)
cap = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Run YOLOv8 pose detection on the frame
    results = model(frame)

    # Extract keypoints (modify based on your model's output structure)
    if results.xyxy[0]:  # Check if any detections are present
        for detection in results.xyxy[0]:
            x_min, y_min, x_max, y_max, conf, class_id, keypoints = detection
            # Access keypoints data here (modify as needed)
            print("Keypoints:", keypoints)

            # Optional: Draw bounding box and keypoints (modify colors and line thickness)
            cv2.rectangle(frame, (int(x_min), int(y_min)), (int(x_max), int(y_max)), (0, 255, 0), 2)
            for kp in keypoints:
                cv2.circle(frame, (int(kp[0]), int(kp[1])), 5, (0, 0, 255), -1)

    # Display the resulting frame
    cv2.imshow('YOLOv8 Pose Estimation', frame)

    # Exit loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release capture object and close windows
cap.release()
cv2.destroyAllWindows()
