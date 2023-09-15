import cv2
from ultralytics import YOLO
from pydub import AudioSegment
from pydub.playback import play

# Load the YOLOv8 model using the provided model path
model_path = 'best.pt'  # Replace with the path to your YOLOv8 model
model = YOLO(model_path)

# return the predicted results
model.predict(source="0",show=True)

'''after this line is voice incorporation, code still in progress'''
#Creation of Alert Sound
# def play_alert_sound():
#     alert_sound = AudioSegment.from_file("sound.wav", format="wav")
#     duration= 2100
#     reminder_sound = AudioSegment.from_file("sounds/SafetyJoviEdited.wav", format="wav")
#     alert_sound= alert_sound[:duration]
#     reminder_sound_new_start= reminder_sound+10
#     combined_sound= alert_sound+reminder_sound_new_start
#     play(combined_sound)

# #Playing of Alert Sound upon Object Detection
# def object_detection_alert():
#     detected_classes= ['NO-Hardhat', 'NO-Mask', 'NO-Safety Vest']
#     for detection in detected_classes:
#         if detection in ['NO-Hardhat', 'NO-Mask', 'NO-Safety Vest']:
#             play_alert_sound()
