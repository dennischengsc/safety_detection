'''
updated with whatsapp message but when will press 'q' it will freeze.
'''

import cv2
from ultralytics import YOLO
from pydub import AudioSegment
from pydub.playback import play
from ultralytics.utils.plotting import Annotator
import threading
import time
import pandas as pd
import pywhatkit as kit
from datetime import datetime, timedelta

# Function to send a WhatsApp message with a longer wait time
def send_whatsapp_message():
    message = 'Alert: Crowds Count Exceeded 10. Please check the work site situation.'
    phone_num = '+6590608458'  # Replace with the recipient's phone number in international format

    # Calculate the desired send time (e.g., 1 minute from now)
    send_time = datetime.now() + timedelta(minutes=0.5)

    # Send the WhatsApp message with a longer wait time (e.g., 10 seconds)
    kit.sendwhatmsg(phone_num, message, send_time.hour, send_time.minute, 10, 20)

# Load the YOLOv8 model using the provided model path
model_path = 'best.pt'  # Replace with the path to your YOLOv8 model
model = YOLO(model_path)

# Initialize the webcam capture
cap = cv2.VideoCapture(0)  # 0 represents the default camera (you can change this if you have multiple cameras)

# Define a flag to track whether the alert sound is currently playing
alert_sound_playing = False

# Initialize pandas DataFrame
data = {'Time': [], 'Count': []}
df = pd.DataFrame(data)

# Define a function to play the alert sound in a separate thread
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

# Initialize timing variables
start_time = time.time()
interval = 5  # 15 seconds interval for counting

# Initialize a lock for synchronizing WhatsApp message sending
whatsapp_lock = threading.Lock()

# Define a function to send the WhatsApp message in a separate thread
def send_whatsapp_thread():
    with whatsapp_lock:
        send_whatsapp_message()

# Main loop for webcam capture and object detection
while True:
    _, frame = cap.read()

    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = model.predict(img)

    for r in results:
        annotator = Annotator(frame)
        boxes = r.boxes
        for box in boxes:
            b = box.xyxy[0]  # get box coordinates in (top, left, bottom, right) format
            c = box.cls
            # Define the color based on the class condition
            if c == 0 or c == 1 or c == 6:
                box_color = (0, 0, 255)  # Red for matching classes
                # Play the alert sound in a separate thread if it's not currently playing
                threading.Thread(target=play_alert_sound).start()
            else:
                box_color = (0, 255, 0)  # Green for non-matching classes

            annotator.box_label(b, model.names[int(c)], color=box_color)

    frame = annotator.result()
    cv2.imshow('YOLO V8 Detection', frame)

    # Check if it's time to count and save
    current_time = time.time()
    if current_time - start_time >= interval:
        start_time = current_time  # Reset the start time

        # Count occurrences of box.cls == 5
        count = 0
        for r in results:
            for box in r.boxes:
                if box.cls == 5:
                    count += 1

        # Record the time and count in the DataFrame
        data = {'Time': [time.strftime('%H:%M:%S')], 'Count': [count]}
        df = pd.concat([df, pd.DataFrame(data)], ignore_index=True)


        # Check if the count exceeds 0 and send a WhatsApp alert in a separate thread
        if count > 0:
            threading.Thread(target=send_whatsapp_thread).start()
        else:
            pass

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# Save the DataFrame to a CSV file
df.to_csv('detection_counts.csv', index=False)
