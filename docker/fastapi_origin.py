import cv2
import io
import os
import numpy as np
from typing import List
from params import LOCAL_MODEL_PATH
from fastapi import FastAPI, UploadFile, File, HTTPException
from ultralytics import YOLO
from fastapi.middleware.cors import CORSMiddleware
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

#model

model_path = os.path.join('docker', 'best.pt')
model= YOLO(model_path)
assert model is not None

@app.post("/detect_image/")

#Setting up detection function for images
async def detect_image(image_upload: UploadFile = File(...)):
    if image_upload:
        # IMPT** need to read uploaded images as bytes
        image_bytes= await image_upload.read()
        # Convert the bytes to an OpenCV image
        image = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), -1)
        # Perform object detection using the YOLOv8 model
        res = model.predict(image)
        # st.write(res)
        # boxes = res[0].boxes
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
    return {'greetings':'This is Docker fastapi'}
