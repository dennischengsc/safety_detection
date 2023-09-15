# from data_prep import create_data_yaml, count_class_occurrences, display_image_sizes, display_set_sizes
# from model_training import train_yolo_model
from prediction import make_predictions
from ultralytics import YOLO
import os



if __name__ == "__main__":

<<<<<<< HEAD
    input_dir = '/home/code/dennischengsc/safety_detection/raw_data/css-data'
    work_dir = '/home/code/dennischengsc/safety_detection/raw_data/model'
    model_path = 'best.pt'
    output_dir = 'detection/image' # to save prediction image
    # reference_image_dir = '/home/dennischeng/code/dennischengsc/safety_detection/reference_image'  # Specify the path to your reference images
    reference_image_dir = 'reference_image'
=======
    user_home = os.path.expanduser("~")
    safety_detection_path = 'code/dennischengsc/safety_detection'
    input_dir = os.path.join(user_home, safety_detection_path, 'raw_data/css-data')
    work_dir = os.path.join(user_home, safety_detection_path, 'raw_data/model')
    model_path = os.path.join(user_home, safety_detection_path, 'best.pt')
    output_dir = os.path.join(user_home, safety_detection_path, 'prediction')
    reference_image_dir = os.path.join(user_home, safety_detection_path, 'reference_image')
>>>>>>> 6103078a9a9757006fcfbe4256d407ea1f4e99ef

    num_classes = 10
    classes = ['Hardhat', 'Mask', 'NO-Hardhat', 'NO-Mask', 'NO-Safety Vest',
               'Person', 'Safety Cone', 'Safety Vest', 'machinery', 'vehicle']

    # # Select the best model
    best_model = YOLO(model_path)

# Make predictions using the best model for all 10 reference images
    make_predictions(best_model, reference_image_dir, output_dir)





    # create_data_yaml(input_dir, work_dir, num_classes, classes)
    # class_stat, data_len = count_class_occurrences(input_dir, num_classes, classes)
    # display_image_sizes(input_dir)
    # display_set_sizes(input_dir)
    # train_yolo_model(work_dir, num_classes)
