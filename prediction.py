from IPython.display import display
import cv2
import os
from ultralytics import YOLO

# 不可以刪
def make_predictions(best_model, reference_path, output_path):
    # Load the YOLO model using the provided model path
    model = best_model

    # Call the predict method with the correct argument format
    return model.predict(reference_path, save=True, project=output_path)


# def make_predictions(best_model, reference_image_dir, output_dir, desired_classes, confidence_threshold=0.5):
#     # Load the YOLO model using the provided model path
#     model = best_model

#     results = model.predict(reference_image_dir, save=True, project=output_dir)  # Assuming 'results' is a list of detection results

#     classes = {
#         0: 'Hardhat',
#         1: 'Mask',
#         2: 'NO-Hardhat',
#         3: 'NO-Mask',
#         4: 'NO-Safety Vest',
#         5: 'Person',
#         6: 'Safety Cone',
#         7: 'Safety Vest',
#         8: 'machinery',
#         9: 'vehicle'
#     }

#     result = results[0]

#     for box in result.boxes:
#         class_name = classes[box.cls[0].item()]  # Map numerical class ID to class name

#         # Check if the detected class is in the list of desired classes and above the confidence threshold
#         if class_name in desired_classes and box.conf[0].item() >= confidence_threshold:
#             cords = [round(x) for x in box.xyxy[0].tolist()]
#             conf = round(box.conf[0].item(), 2)
#             print("Object type:", class_name)
#             print("Coordinates:", cords)
#             print("Probability:", conf)
#             print("---")
