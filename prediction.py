from ultralytics import YOLO
import os
# import cv2

def select_best_model(model_path):
    # Provide the path to the directory containing the trained model weights
    model = YOLO(model_path)
    return model

def select_best_model(model_path):
    # Provide the path to the directory containing the trained model weights
    model = YOLO(model_path)
    return model

def make_predictions(model, output_dir, reference_image_dir):
    # Create a directory to store the prediction results
    os.makedirs(output_dir, exist_ok=True)

    # Provide the path to the directory containing reference images
    reference_images_dir = reference_image_dir

    # Get a list of all image files in the reference images directory
    reference_image_files = [os.path.join(reference_images_dir, filename) for filename in os.listdir(reference_images_dir)]

    # Make predictions on each reference image and save the results
    for i, reference_image_path in enumerate(reference_image_files):
        results = model(reference_image_path)
        output_image_path = os.path.join(output_dir, f'prediction_{i}.jpg')

        # Draw bounding boxes on the image and save it
        results[0].render()[0].save(output_image_path)
