
from IPython.display import display

from ultralytics import YOLO
from IPython.display import display
from pathlib import Path
from shutil import copy

def make_predictions(best_model, reference_image_dir, output_dir):
    # Load the YOLO model using the provided model path
    model = best_model

    model.predict(reference_image_dir, save=True, project=output_dir)
