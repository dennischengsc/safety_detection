# from data_prep import create_data_yaml, count_class_occurrences, display_image_sizes, display_set_sizes
# from model_training import train_yolo_model
from prediction import select_best_model, make_predictions

if __name__ == "__main__":
    input_dir = '/home/dennischeng/code/dennischengsc/safety_detection/raw_data/css-data'
    work_dir = '/home/dennischeng/code/dennischengsc/safety_detection/raw_data/model'
    model_path = 'best.pt'
    output_dir = '/home/dennischeng/code/dennischengsc/safety_detection/raw_data/predict'
    reference_image_dir = '/home/dennischeng/code/dennischengsc/safety_detection/reference_image'  # Specify the path to your reference images

    num_classes = 10
    classes = ['Hardhat', 'Mask', 'NO-Hardhat', 'NO-Mask', 'NO-Safety Vest',
               'Person', 'Safety Cone', 'Safety Vest', 'machinery', 'vehicle']

    # Select the best model
    best_model = select_best_model(model_path)

# Make predictions using the best model for all 10 reference images
    make_predictions(best_model, output_dir, reference_image_dir)



    # create_data_yaml(input_dir, work_dir, num_classes, classes)
    # class_stat, data_len = count_class_occurrences(input_dir, num_classes, classes)
    # display_image_sizes(input_dir)
    # display_set_sizes(input_dir)
    # train_yolo_model(work_dir, num_classes)
