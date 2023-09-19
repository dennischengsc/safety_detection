import cv2
import numpy as np
from params import LOCAL_MODEL_PATH
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from ultralytics import YOLO
from fastapi.middleware.cors import CORSMiddleware
from ultralytics.utils.plotting import Annotator

app = FastAPI()
# app.state.model= load_model()
# Allowing request from any origin, method, headers (ENABLE CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

#model
model= YOLO(LOCAL_MODEL_PATH)

#Setting up detection function for images
@app.post("/detect_image/")
async def detect_image(image_upload: UploadFile = File(...)):
    if image_upload:
        # IMPT** need to read uploaded images as bytes
        image_bytes= await image_upload.read()
                # Convert the bytes to an OpenCV image
        image = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), -1)
        # Perform object detection using the YOLOv8 model
        results = model.predict(image)

        # # Convert images back to bytes
        # _, image_encoded= cv2.imdecode(".jpg", image_with_detections)
        # image_bytes = image_encoded.tobytes()
        return results
    raise HTTPException(status_code=400, detail="No image provided")
