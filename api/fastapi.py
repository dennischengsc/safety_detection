import cv2
import io
import numpy as np
from typing import List
from params import LOCAL_MODEL_PATH
from fastapi import FastAPI, UploadFile, File, HTTPException, Form, Depends, Request
from ultralytics import YOLO
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from starlette.responses import StreamingResponse

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

<<<<<<< HEAD
model= YOLO('best.pt')
#Setting up detection function for images
@app.post("/detect_image/")
async def detect_image(image_upload: UploadFile = File(...),
                       selected_class: str = Form(...),
                       conf: float = Form(...)
                    #    selected_class1: List[int] = Form(...)
                       ):

=======
model= YOLO(LOCAL_MODEL_PATH)
#Setting up detection function for images
@app.post("/detect_image/")
async def detect_image(image_upload: UploadFile = File(...),
                       selected_classes: List[int] = Form(...)
):
>>>>>>> db7bc89bea552826f72b8fdcc334649edf2e9125
    if image_upload:
        selected_class = [int(number) for number in selected_class.split(",")]
        # IMPT** need to read uploaded images as bytes
        image_bytes= await image_upload.read()
        # Convert the bytes to an OpenCV image
        image = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), -1)
        # Perform object detection using the YOLOv8 model
<<<<<<< HEAD
        res = model.predict(image, classes = selected_class, conf = conf)
=======
        res = model.predict(image, classes = selected_classes)
>>>>>>> db7bc89bea552826f72b8fdcc334649edf2e9125
        res_plotted = res[0].plot()[:, :, ::-1]
        bgr_image = cv2.cvtColor(res_plotted, cv2.COLOR_RGB2BGR)
        # Encode the image as JPEG (you can use other formats like PNG)
        _, image_encoded = cv2.imencode(".jpg",bgr_image)
        # Convert the image to bytes
        image_results = image_encoded.tobytes()
        # Return the image as a response
        return StreamingResponse(io.BytesIO(image_results), media_type="image/jpeg")
    raise HTTPException(status_code=400, detail="No image provided")

@app.get("/")
def root():
<<<<<<< HEAD
    return {
    'greeting':'Hello'
    }
=======
    return {'greeting':'Hello, this is local machine fastapi'}
>>>>>>> db7bc89bea552826f72b8fdcc334649edf2e9125
