
from IPython.display import display

from ultralytics import YOLO

def make_predictions(model_path, reference_image_dir, output_dir):
    # Load the YOLO model using the provided model path
    model = YOLO('best.pt')

    model.predict('reference_image/', save=True)
