'''
- updated 20230915-2236 Successful predict and trigger sound and with red boxes shown
- update 20230918-1516 Successful play the sound smoothly and incorporated person counting features, set interval = 5 (seconds)
- return dataframe of number of person on site at every 5 sec(adjustable) interval
'''
import cv2
from ultralytics import YOLO
from pydub import AudioSegment
from pydub.playback import play
from ultralytics.utils.plotting import Annotator
import threading
import time
import pandas as pd
import os

# Load the YOLOv8 model using the provided model path
model_path = 'best.pt'  # Replace with the path to your YOLOv8 model
model = YOLO(model_path)

# Creating a folder to save results for live detection
if not os.path.exists('results'):
    os.makedirs('results')

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

# Main loop for webcam capture and object detection
while True:
    _, frame = cap.read()

    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = model.predict(img)

    for r in results:
        annotator = Annotator(frame)
        boxes = r.boxes
        save_frame = False  #testing
        for box in boxes:
            b = box.xyxy[0]  # get box coordinates in (top, left, bottom, right) format
            c = box.cls
            # Define the color based on the class condition
            if c == 0 or c == 1 or c == 6:
                box_color = (0, 0, 255)  # Red for matching classes
                # Define the filename for the saved frame (you can customize this)
                save_frame = True      # testing
                # Play the alert sound in a separate thread if it's not currently playing
                threading.Thread(target=play_alert_sound).start()
            else:
                box_color = (0, 255, 0)  # Green for non-matching classes

            annotator.box_label(b, model.names[int(c)], color=box_color)

    frame = annotator.result()
    cv2.imshow('YOLO V8 Detection', frame)

    # Save the frame if the condition is met
    # if save_frame:                      #testing
    #     filename = f'results/frame_{time.time()}.jpg'
    #     cv2.imwrite(filename, frame)

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

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# Save the DataFrame to a CSV file
df.to_csv('detection_counts.csv', index=False)
