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
<<<<<<< HEAD
import pywhatkit as kit
from datetime import datetime, timedelta
=======
>>>>>>> db7bc89bea552826f72b8fdcc334649edf2e9125


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

<<<<<<< HEAD
# Function to send a WhatsApp message with a longer wait time
def send_whatsapp_message():
    message = 'Alert: Crowds Count Exceeded 10. Please check the work site situation.'
    phone_num = '+6590608458'  # Replace with the recipient's phone number in international format

    # Calculate the desired send time (e.g., 1 minute from now)
    send_time = datetime.now() + timedelta(minutes=0.5)

    # Send the WhatsApp message with a longer wait time (e.g., 10 seconds)
    kit.sendwhatmsg(phone_num, message, send_time.hour, send_time.minute, 10, 15)

=======
>>>>>>> db7bc89bea552826f72b8fdcc334649edf2e9125
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

<<<<<<< HEAD


=======
>>>>>>> db7bc89bea552826f72b8fdcc334649edf2e9125
# Initialize a lock for synchronizing WhatsApp message sending
whatsapp_lock = threading.Lock()

# Define a function to send the WhatsApp message in a separate thread
<<<<<<< HEAD
def send_whatsapp_thread():
    with whatsapp_lock:
        send_whatsapp_message()
=======
# def send_whatsapp_thread():
#     with whatsapp_lock:
#         send_whatsapp_message()
>>>>>>> db7bc89bea552826f72b8fdcc334649edf2e9125

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
    # Initialize timing variables
    start_time = time.time()
    interval = 5  # interval for counting (seconds)

    count_display = st.empty()

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
<<<<<<< HEAD
            if c == 0 or c == 1 or c == 7:
=======
            if c == 1 or c == 7 or c == 0:
>>>>>>> db7bc89bea552826f72b8fdcc334649edf2e9125
                # box_color = (0, 0, 255)  # Red for matching classes
                # Play the alert sound in a separate thread if it's not currently playing
                threading.Thread(target=play_alert_sound).start()
            else:
                pass
                # box_color = (0, 255, 0)  # Green for non-matching classes
<<<<<<< HEAD

    # Check if it's time to count and save
    current_time = time.time()
    if current_time - start_time >= interval:
        start_time = current_time  # Reset the start time

        # Count occurrences of box.cls == 5
        count = 0
        for r in res:
            for box in r.boxes:
                if box.cls == 5:
                    count += 1

        count_display.write(f"Count: {count}")

        # Check if the count exceeds 0 and send a WhatsApp alert in a separate thread
        if count > 0:
            threading.Thread(target=send_whatsapp_thread).start()
        else:
            pass
=======
>>>>>>> db7bc89bea552826f72b8fdcc334649edf2e9125

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
