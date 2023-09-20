import cv2
import io
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
model= YOLO(LOCAL_MODEL_PATH)
#Setting up detection function for images
@app.post("/detect_image/")
async def detect_image(
    image_uploads: List[UploadFile] = File(...),
):
    if not image_uploads:
        raise HTTPException(status_code=400, detail="No images provided")

    results = []

    for image_upload in image_uploads:
        # Read the uploaded image as bytes
        image_bytes = await image_upload.read()
        # Convert the bytes to an OpenCV image
        image = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), -1)
        # Perform object detection using the YOLOv8 model
        res = model.predict(image, classes=[2, 3, 4])
        # Plot the filtered results on the image
        res_plotted = res.plot()[:, :, ::-1]
        bgr_image = cv2.cvtColor(res_plotted, cv2.COLOR_RGB2BGR)
        # Encode the image as JPEG (you can use other formats like PNG)
        _, image_encoded = cv2.imencode(".jpg", bgr_image)
        # Convert the image to bytes
        image_results = image_encoded.tobytes()
        results.append(image_results)

    # Return the processed images as a list of StreamingResponse
    return [StreamingResponse(io.BytesIO(image), media_type="image/jpeg") for image in results]

@app.get("/")
def root():
    return {'greetings': 'Hello'}
