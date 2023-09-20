SAFETY DETECTION

This project aims to setup a live detection feed.

This live feed will be able to detect people not wearing their safety equipment and if the location is overcrowded.

We have created a streamlit app on our local repository to be able to detect multiple inputs.
This inputs include a active feed through a web camera, images, videos and a youtube link.

Active Feed Features
- Alert sound upon object detection of selected classes
- Count of the people in the feed
- Capturing the different frames where selected class was detected and saving into the 'results' folder (This will allow management to review who did not follow the safety protocols and take action)
Images, Videos, Youtube link feeds
- Able to choose the object to be detected from the prediction model

There will also be deployment of the model on a url that will be able to load multiple images to do object detection.

In the future, we hope to be able to deploy the live feed feature and the uploading of videos.

REPOSITORY CONTENT
safety_detection
- api(folder)
  - fastapi.py
- donot_touch(folder)
  - main_back_donotdelete.py
- images(folder)
- model(folder)
  - model_list(folder)
  - yolov8n_7classes(folder)
- prediction(folder)
  - predict(folder)
  - ... (folders)
- reference_image(folder)
- results(folder)
- safety_detection(folder)
- sounds(folder)
- templates(folder)
- videos(folder)
- weights(folder)
- .gitignore
- Makefile
- README.md
- app.py
- data_prep.py
- flask_app.py
- helper.py
- live_detection.py
- main.py
- model_training.py
- params.py
- prediction.py
- requirements.txt
- settings.py
- setup.py
