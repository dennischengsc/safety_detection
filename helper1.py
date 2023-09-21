import cv2
import time
import threading
import pandas as pd
import streamlit as st
from pytube import YouTube
from ultralytics import YOLO
from pydub.playback import play
from pydub import AudioSegment
from ultralytics.utils.plotting import Annotator
import threading


# Local Modules
import helper
import settings


def load_model(model_path):
    """
    Loads a YOLO object detection model from the specified model_path.

    Parameters:
        model_path (str): The path to the YOLO model file.

    Returns:
        A YOLO object detection model.
    """
    model = YOLO(model_path)
    return model


def display_tracker_options():
    display_tracker = st.radio("Display Tracker", ('Yes', 'No'))
    is_display_tracker = True if display_tracker == 'Yes' else False
    if is_display_tracker:
        tracker_type = st.radio("Tracker", ("bytetrack.yaml", "botsort.yaml"))
        return is_display_tracker, tracker_type
    return is_display_tracker, None

alert_sound_playing = False # alert sound flag

def play_alert_sound():
    global alert_sound_playing
    if not alert_sound_playing:
        alert_sound_playing = True
        alert_sound = AudioSegment.from_file("sounds/warningalarm.wav", format="wav")
        duration = 2100
        reminder_sound = AudioSegment.from_file("sounds/SafetyJoviEdited.wav", format="wav")
        alert_sound_volume = alert_sound[:duration] + 5  # Adjust volume
        reminder_sound_volume = reminder_sound + 10  # Adjust volume
        combined_sound = alert_sound_volume + reminder_sound_volume
        play(combined_sound)
        alert_sound_playing = False

# Initialize a lock for synchronizing WhatsApp message sending
whatsapp_lock = threading.Lock()

# Define a function to send the WhatsApp message in a separate thread
def send_whatsapp_thread():
    with whatsapp_lock:
        send_whatsapp_message()

def _display_detected_frames(conf, model, st_frame, image, is_display_tracking=None, tracker=None, selected_classes=None):
    """
    Display the detected objects on a video frame using the YOLOv8 model.

    Args:
    - conf (float): Confidence threshold for object detection.
    - model (YoloV8): A YOLOv8 object detection model.
    - st_frame (Streamlit object): A Streamlit object to display the detected video.
    - image (numpy array): A numpy array representing the video frame.
    - is_display_tracking (bool): A flag indicating whether to display object tracking (default=None).

    Returns:
    None
    """

    # Resize the image to a standard size
    image = cv2.resize(image, (720, int(720*(9/16))))

    # Display object tracking, if specified
    if is_display_tracking:
        res = model.track(image, conf=conf, persist=True, tracker=tracker, classes=selected_classes)
    else:
        # Predict the objects in the image using the YOLOv8 model
        res = model.predict(image, conf=conf, classes=selected_classes)

    for r in res:
        boxes = r.boxes
        for box in boxes:
            # b = box.xyxy[0]  # get box coordinates in (top, left, bottom, right) format
            c = box.cls
            # Define the color based on the class condition
            if c == 1 or c == 7 or c == 0:
                # box_color = (0, 0, 255)  # Red for matching classes
                # Play the alert sound in a separate thread if it's not currently playing
                threading.Thread(target=play_alert_sound).start()
            else:
                pass
                # box_color = (0, 255, 0)  # Green for non-matching classes

    # Plot the detected objects on the video frame
    res_plotted = res[0].plot()
    st_frame.image(res_plotted,
                   caption='Detected Video',
                   channels="BGR",
                   use_column_width=True
                   )


def play_youtube_video(conf, model, selected_classes=None):
    """
    Plays a webcam stream. Detects Objects in real-time using the YOLOv8 object detection model.

    Parameters:
        conf: Confidence of YOLOv8 model.
        model: An instance of the `YOLOv8` class containing the YOLOv8 model.

    Returns:
        None

    Raises:
        None
    """
    source_youtube = st.sidebar.text_input("YouTube Video url")

    is_display_tracker, tracker = display_tracker_options()

    if st.sidebar.button('Detect Objects'):
        try:
            yt = YouTube(source_youtube)
            stream = yt.streams.filter(file_extension="mp4", res=720).first()
            vid_cap = cv2.VideoCapture(stream.url)

            st_frame = st.empty()
            while (vid_cap.isOpened()):
                success, image = vid_cap.read()
                if success:
                    _display_detected_frames(conf,
                                             model,
                                             st_frame,
                                             image,
                                             is_display_tracker,
                                             tracker,
                                             selected_classes
                                             )
                else:
                    vid_cap.release()
                    break
        except Exception as e:
            st.sidebar.error("Error loading youtube video: " + str(e))


def play_webcam(conf, model, selected_classes=None):
    """
    Plays a webcam stream. Detects Objects in real-time using the YOLOv8 object detection model.

    Parameters:
        conf: Confidence of YOLOv8 model.
        model: An instance of the `YOLOv8` class containing the YOLOv8 model.

    Returns:
        None

    Raises:
        None
    """
    source_webcam = settings.WEBCAM_PATH
    is_display_tracker, tracker = display_tracker_options()
    if st.sidebar.button('Detect Objects'):
        try:
            vid_cap = cv2.VideoCapture(source_webcam)
            st_frame = st.empty()
            while (vid_cap.isOpened()):
                success, image = vid_cap.read()
                if success:
                    _display_detected_frames(conf,
                                             model,
                                             st_frame,
                                             image,
                                             is_display_tracker,
                                             tracker,
                                             selected_classes
                                             )
                else:
                    vid_cap.release()
                    break
        except Exception as e:
            st.sidebar.error("Error loading webcam: " + str(e))



def play_live_prediction(conf, model, selected_classes=None):
    """
    Plays a stored video file. Tracks and detects objects in real-time using the YOLOv8 object detection model.

    Parameters:
        conf: Confidence of YOLOv8 model.
        model: An instance of the `YOLOv8` class containing the YOLOv8 model.
        selected_classes: List of selected classes for detection (optional).

    Returns:
        None
    """

    # Initialize the webcam capture
    cap = cv2.VideoCapture(0)  # 0 represents the default camera (you can change this if you have multiple cameras)

    # Define a flag to track whether the alert sound is currently playing
    alert_sound_playing = False

    while True:
        # Capture a frame from the webcam
        ret, frame = cap.read()

        # Check if the frame capture was successful
        if not ret:
            st.error("Error capturing frame from the webcam.")
            break

        # Check if the frame is empty or None
        if frame is not None and not frame.empty():
            # Convert the frame from BGR to RGB color space
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Perform object detection using the YOLOv8 model
            results = model.predict(img)

            for r in results:
                for box in r.boxes:
                    c = box.cls
                    # Define the color based on the class condition
                    if c == 0 or c == 1 or c == 6:
                        box_color = (0, 0, 255)  # Red for matching classes
                        # Play the alert sound in a separate thread if it's not currently playing
                        if not alert_sound_playing:
                            alert_sound_playing = True
                            threading.Thread(target=play_alert_sound).start()
                    else:
                        box_color = (0, 255, 0)  # Green for non-matching classes

            # Display the frame with annotations
            cv2.imshow('YOLO V8 Detection', frame)

            if count > 0:
                threading.Thread(target=send_whatsapp_thread).start()
            else:
                pass

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            st.warning("Invalid frame received. Skipping frame processing.")

    # Release the webcam and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()
