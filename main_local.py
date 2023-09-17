# from data_prep import create_data_yaml, count_class_occurrences, display_image_sizes, display_set_sizes
# from model_training import train_yolo_model
from prediction import make_predictions
from model_training import train_yolo_model
from ultralytics import YOLO
from params import *
from data_prep import *




if __name__ == "__main__":

    # # Select the best model


# Make predictions using the best model for all 10 reference images

# 1. Create Data.yaml
#create_data_yaml(LOCAL_INPUT_PATH, LOCAL_WORK_PATH,NUM_CLASSES, CLASS_NAME)
# 2. Train yolo model
#train_yolo_model(LOCAL_WORK_PATH, NUM_CLASSES)
# 3. Get best model
#best_model = YOLO(LOCAL_MODEL_PATH)
# 4. Make prediction
#make_predictions(best_model, LOCAL_REFERENCE_PATH, LOCAL_OUTPUT_PATH)




# 2.
#class_stat, data_len = count_class_occurrences(input_dir, num_classes, classes)
# display_image_sizes(input_dir)
# display_set_sizes(input_dir)
