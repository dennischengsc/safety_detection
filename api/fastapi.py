import cv2
import io
import numpy as np
from params import LOCAL_MODEL_PATH
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
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

    # for r in results:

    #     annotator = Annotator(frame)

    #     boxes = r.boxes
    #     for box in boxes:
    #         b = box.xyxy[0]  # get box coordinates in (top, left, bottom, right) format
    #         c = box.cls
    #         annotator.box_label(b, model.names[int(c)], color = (0,0,255)) # red colour box

    #         # to detect if there is a mask/hardhat/safety-vest then play the alert
    #         if c == 0 or c == 1 or c == 6:
    #             play_alert_delayed()
    #         else:
    #             pass

    # frame = annotator.result()
    # cv2.imshow('YOLO V8 Detection', frame)

#Setting up detection function for videos
@app.post("/detect_video/")
async def detect_video(video_upload: UploadFile= None):
    if video_upload:
        if video_upload:
            # IMPT** Reading uploaded videos as bytes
            video_bytes= await video_upload.read()
            # Save video to temp folder
            video_path= "/temp/uploaded_video.mp4"
            with open(video_path, 'wb') as video_file:
                video_file.write(video_bytes)
            cap= cv2.VideoCapture(video_path)
            #if no video is uploaded
            if not cap.isOpened():
                raise HTTPException(status_code=500, detail="Unable to open the uploaded video")

            frames_with_detection= []
            while True:
                ret, frames= cap.read()
                if not ret:
                    break
                #Object detection on each frames
                detections= model.predict(frames)
                frames_with_detection.append({"frame":frames, "detections": detections})
            cap.release()
            return {"frames_with_detections": frames_with_detection}

        else:
            raise HTTPException(status_code=400, detail="No video file provided")

    raise HTTPException(status_code=400, detail="Invalid request or missing options")

@app.get("/")
def root():
    return {'greetings': 'Hello'}
