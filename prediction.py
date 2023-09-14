from IPython.display import display
import cv2
import os
from ultralytics import YOLO

<<<<<<< HEAD
def make_predictions(best_model, reference_image_dir, output_dir):
    # Load the YOLO model using the provided model path
    model = best_model

    # model.predict(reference_image_dir, save=True, project=output_dir)
=======
# 不可以刪
# def make_predictions(best_model, reference_image_dir, output_dir):
#     # Load the YOLO model using the provided model path
#     model = best_model

#     # Call the predict method with the correct argument format
#     return model.predict(reference_image_dir, save=True, project=output_dir)


def make_predictions(best_model, reference_image_dir, output_dir):
    # Load the YOLO model using the provided model path
    model = best_model

>>>>>>> e312ab68af6859584ce8ffe984d8d5f228db8a4a
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

<<<<<<< HEAD
    # Define the class IDs you want to capture
    target_class_ids = [0,1,2,3,4,5,7]
    filtered_class_names = []

    # Now you can iterate through the filtered results and work with them
    for result in results:
        boxes = result.boxes
        if int(boxes.cls) in target_class_ids:
            if boxes.conf >0.8:
                filtered_class_names.append(classes)

        # for box in boxes:
        #     print(box.cls)
        # Filter and capture boxes.cls elements with specific class IDs

        filtered_class_names = [classes[int(cls)] for cls in boxes.cls if int(cls) in target_class_ids]

        for box in filtered_class_names:
            if box.
        print(filtered_class_names)
=======
    result = results[0]
    box = result.boxes[0]
    print("Object type:",box.cls[0])
    print("Coordinates:",box.xyxy[0])
    print("Probability:",box.conf[0])

    cords = box.xyxy[0].tolist()
    class_id = box.cls[0].item()
    conf = box.conf[0].item()
    print("Object type:", class_id)
    print("Coordinates:", cords)
    print("Probability:", conf)
    print(result.names)


    for box in result.boxes:
        class_id = result.names[box.cls[0].item()]
        cords = box.xyxy[0].tolist()
        cords = [round(x) for x in cords]
        conf = round(box.conf[0].item(), 2)
        print("Object type:", class_id)
        print("Coordinates:", cords)
        print("Probability:", conf)
        print("---")
>>>>>>> e312ab68af6859584ce8ffe984d8d5f228db8a4a
