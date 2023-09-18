import glob
import os
import time
import pickle
import yaml

from colorama import Fore, Style
from google.cloud import storage
from params import *
from ultralytics import YOLO


def create_data_yaml(num_classes, classes):

    if MODEL_TARGET == 'local':
        dict_file = {
            'train': os.path.join(LOCAL_INPUT_PATH, 'train'),
            'val': os.path.join(LOCAL_INPUT_PATH, 'valid'),
            'test': os.path.join(LOCAL_INPUT_PATH, 'test'),
            'nc': num_classes,
            'names': classes
        }
        output_path = os.path.join(LOCAL_WORK_PATH, 'data.yaml')
        with open(output_path, 'w+') as file:
            yaml.dump(dict_file, file)

    elif MODEL_TARGET == 'gcs':
        # Set up Google Cloud Storage client
        client = storage.Client()

        # Define the GCS paths for input data
        gcs_train_path = f'gs://{BUCKET_NAME}/css-data/train'
        gcs_valid_path = f'gs://{BUCKET_NAME}/css-data/valid'
        gcs_test_path = f'gs://{BUCKET_NAME}/css-data/test'

        dict_file = {
            'train': gcs_train_path,
            'val': gcs_valid_path,
            'test': gcs_test_path,
            'nc': num_classes,
            'names': classes
        }

        # Define the GCS object path for data.yaml
        gcs_object_path = 'model/data.yaml'

        # Serialize the YAML data to a string
        yaml_data = yaml.dump(dict_file)

        # Upload the data.yaml to GCS
        bucket = client.bucket(BUCKET_NAME)
        blob = bucket.blob(gcs_object_path)
        blob.upload_from_string(yaml_data, 'data.yaml')

def train_yolo_model(img_size=640, epochs=1, batch=64, save_period=10):
    if MODEL_TARGET == 'local':
        model_path = os.path.join(LOCAL_WORK_PATH, 'yolov8n.pt')
        data_path = os.path.join(LOCAL_WORK_PATH, 'data.yaml')

        model = YOLO(model_path)
        model.train(
        data=data_path,
        task='detect',
        imgsz=img_size,
        epochs=epochs,
        batch=batch,
        mode='train',
        name='yolov8n_change_path_test',
        resume=False,
        save_period=save_period,
        project = os.path.join(LOCAL_DATA_PATH, 'model')
        )

    elif MODEL_TARGET == 'gcs':
        # Set up Google Cloud Storage client
        client = storage.Client()

        # Define the GCS paths for model and data
        gcs_bucket_name = BUCKET_NAME
        model_path = f'gs://{gcs_bucket_name}/model/yolov8n.pt'
        data_path = f'gs://{gcs_bucket_name}/model/data.yaml'

        model = YOLO(model_path)
        model.train(
        data=data_path,
        task='detect',
        imgsz=img_size,
        epochs=epochs,
        batch=batch,
        mode='train',
        name='yolov8n_change_path_test',
        resume=False,
        save_period=save_period,
        project = os.path.join(gcs_bucket_name, 'model')
    )

create_data_yaml(NUM_CLASSES,CLASS_NAME)
train_yolo_model()

# def load_image_gcs ():
#     client = storage.Client()
#     bucket_name = BUCKET_NAME
#     object_path = GCS_INPUT_PATH

# def save_model(model: keras.Model = None) -> None:
#     """
#     Persist trained model locally on the hard drive at f"{LOCAL_REGISTRY_PATH}/models/{timestamp}.h5"
#     - if MODEL_TARGET='gcs', also persist it in your bucket on GCS at "models/{timestamp}.h5" --> unit 02 only
#     - if MODEL_TARGET='mlflow', also persist it on MLflow instead of GCS (for unit 0703 only) --> unit 03 only
#     """

#     timestamp = time.strftime("%Y%m%d-%H%M%S")

#     # Save model locally
#     model_path = os.path.join(LOCAL_MODEL_PATH, f"{timestamp}.pt")
#     model.save(model_path)

#     print("✅ Model saved locally")

#     if MODEL_TARGET == "gcs":
#         # 🎁 We give you this piece of code as a gift. Please read it carefully! Add a breakpoint if needed!

#         model_filename = model_path.split("/")[-1] # e.g. "20230208-161047.h5" for instance
#         client = storage.Client()
#         bucket = client.bucket(BUCKET_NAME)
#         blob = bucket.blob(f"models/{model_filename}")
#         blob.upload_from_filename(model_path)

#         print("✅ Model saved to GCS")

#         return None

#     return None

# def load_model(stage="Production") -> keras.Model:
#     """
#     Return a saved model:
#     - locally (latest one in alphabetical order)
#     - or from GCS (most recent one) if MODEL_TARGET=='gcs'  --> for unit 02 only
#     - or from MLFLOW (by "stage") if MODEL_TARGET=='mlflow' --> for unit 03 only

#     Return None (but do not Raise) if no model is found

#     """

#     if MODEL_TARGET == "local":
#         print(Fore.BLUE + f"\nLoad latest model from local registry..." + Style.RESET_ALL)

#         # Get the latest model version name by the timestamp on disk
#         local_model_directory = os.path.join(LOCAL_REGISTRY_PATH, "models")
#         local_model_paths = glob.glob(f"{local_model_directory}/*")

#         if not local_model_paths:
#             return None

#         most_recent_model_path_on_disk = sorted(local_model_paths)[-1]

#         print(Fore.BLUE + f"\nLoad latest model from disk..." + Style.RESET_ALL)

#         latest_model = keras.models.load_model(most_recent_model_path_on_disk)

#         print("✅ Model loaded from local disk")

#         return latest_model

#     elif MODEL_TARGET == "gcs":
#         # 🎁 We give you this piece of code as a gift. Please read it carefully! Add a breakpoint if needed!
#         print(Fore.BLUE + f"\nLoad latest model from GCS..." + Style.RESET_ALL)

#         client = storage.Client()
#         blobs = list(client.get_bucket(BUCKET_NAME).list_blobs(prefix="model"))

#         try:
#             latest_blob = max(blobs, key=lambda x: x.updated)
#             latest_model_path_to_save = os.path.join(LOCAL_REGISTRY_PATH, latest_blob.name)
#             latest_blob.download_to_filename(latest_model_path_to_save)

#             latest_model = keras.models.load_model(latest_model_path_to_save)

#             print("✅ Latest model downloaded from cloud storage")

#             return latest_model
#         except:
#             print(f"\n❌ No model found in GCS bucket {BUCKET_NAME}")

#             return None

# Upload data & model to GCS
# Set Params & .env python files
# Write code to get data from gcs

# write code to get model from gcs
# Using the gcs data to do a training with gcs model
# Predict on a image from local & save it in gcs predict folder
