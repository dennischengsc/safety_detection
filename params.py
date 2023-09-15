import os


##################  VARIABLES  ##################
MODEL_TARGET = os.environ.get('MODEL_TARGET')
GCP_PROJECT = os.environ.get('GCP_PROJECT')
GCP_REGION = os.environ.get('GCP_REGION')
BUCKET_NAME = os.environ.get('BUCKET_NAME')

##################  CONSTANTS  #####################
LOCAL_DATA_PATH = os.path.join(os.path.expanduser("~"), 'code/dennischengsc/safety_detection')
LOCAL_INPUT_PATH = os.path.join(LOCAL_DATA_PATH, 'raw_data/css-data')
LOCAL_WORK_PATH = os.path.join(LOCAL_DATA_PATH, 'raw_data/model')
LOCAL_MODEL_PATH = os.path.join(LOCAL_DATA_PATH, 'model','yolov8n_7_classes', 'weights','best.pt')
LOCAL_OUTPUT_PATH = os.path.join(LOCAL_DATA_PATH, 'prediction')
LOCAL_REFERENCE_PATH = os.path.join(LOCAL_DATA_PATH, 'reference_image')
