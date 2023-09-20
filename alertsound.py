from pydub import AudioSegment
from pydub.playback import play

#Creation of Alert Sound
def play_alert_sound():
    alert_sound = AudioSegment.from_file("sounds/warningalarm.wav", format="wav")
    duration= 2100
    reminder_sound = AudioSegment.from_file("sounds/SafetyJoviEdited.wav", format="wav")
    alert_sound= alert_sound[:duration]
    reminder_sound_new_start= reminder_sound+10
    combined_sound= alert_sound+reminder_sound_new_start
    play(combined_sound)

#Playing of Alert Sound upon Object Detection
def object_detection_alert():
    detected_classes= ['NO-Hardhat', 'NO-Mask', 'NO-Safety Vest']
    for detection in detected_classes:
        if detection in ['NO-Hardhat', 'NO-Mask', 'NO-Safety Vest']:
            play_alert_sound()
