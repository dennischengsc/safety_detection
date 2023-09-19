'''Successful predict but no boxes shown'''
import cv2
from ultralytics import YOLO
from pydub import AudioSegment
from pydub.playback import play
from ultralytics.utils.plotting import Annotator
import time

# Load the YOLOv8 model using the provided model path
model_path = 'best.pt'  # Replace with the path to your YOLOv8 model
model = YOLO(model_path)

# Initialize the webcam capture
cap = cv2.VideoCapture(0)  # 0 represents the default camera (you can change this if you have multiple cameras)

# Define a function to play the alert sound
#Creation of Alert Sound


# play(combined_sound)
#Added delay to alert sound
def play_alert_delayed(delay_seconds=10):
    alert_sound = AudioSegment.from_file("sound/warningalarm.wav", format="wav")
    duration= 2100
    reminder_sound = AudioSegment.from_file("sound/SafetyJoviEdited.wav", format="wav")
    alert_sound_volume= alert_sound[:duration]+ 5 #num is volume
    reminder_sound_volume= reminder_sound+ 10 #num is volume
    combined_sound= alert_sound_volume+reminder_sound_volume
    play(combined_sound)
    #time.sleep(delay_seconds)



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
            annotator.box_label(b, model.names[int(c)], color = (0,0,255)) # red colour box

            # to detect if there is a mask/hardhat/safety-vest then play the alert
            if c == 0 or c == 1 or c == 6:
                play_alert_delayed()
            else:
                pass



    frame = annotator.result()
    cv2.imshow('YOLO V8 Detection', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
