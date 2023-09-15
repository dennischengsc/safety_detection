# from data_prep import create_data_yaml, count_class_occurrences, display_image_sizes, display_set_sizes
# from model_training import train_yolo_model
from prediction import make_predictions
from ultralytics import YOLO
from params import *



if __name__ == "__main__":

    num_classes = 10
    classes = ['Hardhat', 'Mask', 'NO-Hardhat', 'NO-Mask', 'NO-Safety Vest',
               'Person', 'Safety Cone', 'Safety Vest', 'machinery', 'vehicle']

    # # Select the best model
    best_model = YOLO(LOCAL_MODEL_PATH)

# Make predictions using the best model for all 10 reference images
    make_predictions(best_model, LOCAL_REFERENCE_PATH, LOCAL_OUTPUT_PATH)





    # create_data_yaml(input_dir, work_dir, num_classes, classes)
    # class_stat, data_len = count_class_occurrences(input_dir, num_classes, classes)
    # display_image_sizes(input_dir)
    # display_set_sizes(input_dir)
    # train_yolo_model(work_dir, num_classes)
