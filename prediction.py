from IPython.display import display
import cv2
import os
from ultralytics import YOLO

# 不可以刪
# def make_predictions(best_model, reference_image_dir, output_dir):
#     # Load the YOLO model using the provided model path
#     model = best_model

#     # Call the predict method with the correct argument format
#     return model.predict(reference_image_dir, save=True, project=output_dir)


def make_predictions(best_model, reference_image_dir, output_dir):
    # Load the YOLO model using the provided model path
    model = best_model

    results = model.predict(reference_image_dir, save=True, project=output_dir)  # Assuming 'results' is a list of detection results

    classes = {
        0: 'Hardhat',
        1: 'Mask',
        2: 'NO-Hardhat',
        3: 'NO-Mask',
        4: 'NO-Safety Vest',
        5: 'Person',
        6: 'Safety Cone',
        7: 'Safety Vest',
        8: 'machinery',
        9: 'vehicle'
    }

    # Define the class IDs you want to capture
    target_class_ids = [4, 5, 3]

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Now you can iterate through the filtered results and work with them
    for result in results:
        image = cv2.imread(os.path.join(reference_image_dir, result["image_path"]))  # Load the image using OpenCV
        boxes = result.boxes
        masks = result.masks
        keypoints = result.keypoints
        probs = result.probs

        # Iterate through detected objects and draw bounding boxes and labels for filtered classes
        for box, cls, prob in zip(boxes, boxes.cls, probs):
            if int(cls) in target_class_ids:
                class_name = classes[int(cls)]
                score = f"{class_name}: {prob:.2f}"
                x, y, w, h = box.xyxy[0].tolist()
                x, y, w, h = int(x), int(y), int(w), int(h)
                color = (0, 255, 0)  # Green color for bounding boxes
                cv2.rectangle(image, (x, y), (w, h), color, 2)
                cv2.putText(image, score, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        # Save the modified image with only filtered classes
        image_name = os.path.basename(result["image_path"])
        modified_image_path = os.path.join(output_dir, f"filtered_{image_name}")
        cv2.imwrite(modified_image_path, image)

        print(f"Filtered image saved at {modified_image_path}")
