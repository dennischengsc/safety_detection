import cv2
from ultralytics import YOLO

# Load the YOLOv8 model using the provided model path
model_path = 'best.pt'  # Replace with the path to your YOLOv8 model
model = YOLO(model_path)

# return the predicted results
model.predict(source="vscode-camera",show=True)
