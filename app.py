
from pathlib import Path
import PIL

# External packages
import streamlit as st

# Local Modules
import settings
import helper

# Setting page layout
st.set_page_config(
    page_title="Safety Object Detection using YOLOv8",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Main page heading
st.title("Safety Object Detection using YOLOv8")

# Sidebar
st.sidebar.header("ML Model Config")



# Model Options
model_type = st.sidebar.radio(
    "Select Task", ['Detection', 'Segmentation'])

confidence = float(st.sidebar.slider(
    "Select Model Confidence", 25, 100, 40)) / 100

# Selecting Detection Or Segmentationmark
if model_type == 'Detection':
    model_path = Path(settings.DETECTION_MODEL)
elif model_type == 'Segmentation':
    model_path = Path(settings.SEGMENTATION_MODEL)

# Load Pre-trained ML Model
try:
    model = helper.load_model(model_path)
except Exception as ex:
    st.error(f"Unable to load model. Check the specified path: {model_path}")
    st.error(ex)

st.sidebar.header("Image/Video Config")
source_radio = st.sidebar.radio(
    "Select Source", settings.SOURCES_LIST)

source_img = None
# If image is selected
if source_radio == settings.IMAGE:
    source_img = st.sidebar.file_uploader(
        "Choose an image...", type=("jpg", "jpeg", "png", 'bmp', 'webp'))

    col1, col2 = st.columns(2)

    with col1:
        try:
            if source_img is None:
                default_image_path = str(settings.DEFAULT_IMAGE)
                default_image = PIL.Image.open(default_image_path)
                st.image(default_image_path, caption="Default Image",
                         use_column_width=True)
            else:
                uploaded_image = PIL.Image.open(source_img)
                st.image(source_img, caption="Uploaded Image",
                         use_column_width=True)
        except Exception as ex:
            st.error("Error occurred while opening the image.")
            st.error(ex)

    with col2:
        if source_img is None:
            default_detected_image_path = str(settings.DEFAULT_DETECT_IMAGE)
            default_detected_image = PIL.Image.open(
                default_detected_image_path)
            st.image(default_detected_image_path, caption='Detected Image',
                     use_column_width=True)
        else:
            if st.sidebar.button('Detect Objects'):
                res = model.predict(uploaded_image,
                                    conf=confidence,
                                    classes=[0,4,5]
                                    )
                boxes = res[0].boxes
                res_plotted = res[0].plot()[:, :, ::-1]
                st.image(res_plotted, caption='Detected Image',
                         use_column_width=True)
                #Initial a counter for calss 5 object
                class_5_count =0

                try:
                    with st.expander("Detection Results"):
                        for box in boxes:
                            # st.write(box.data[:,-1])


                            # Extact class IDs
                            clsss_ids = box.data[:,-1]
                            if 5 in clsss_ids:
                                class_5_count +=1

                            st.write(box.data)
                        # Display the total count of class 5 objects
                    st.write(f"Counter of Person is : {class_5_count}")

                except Exception as ex:
                    # st.write(ex)
                    st.write("No image is uploaded yet!")

elif source_radio == settings.VIDEO:
    helper.play_stored_video(confidence, model)
    class_5_count = 0  # Initialize the counter for class 5 objects

    # Process each frame of the video
    for frame in helper.get_video_frames():  # Assuming you have a function get_video_frames() that returns video frames
        # Detect objects in the frame
        res = model.predict(frame, conf=confidence, classes=[0, 4, 5])
        boxes = res[0].boxes

        for box in boxes:
            class_ids = box.data[:, -1]
            if 5 in class_ids:
                class_5_count += 1

    # Display the total count of class 5 objects after processing the video
    st.write(f"Total Count of Persons: {class_5_count}")

elif source_radio == settings.WEBCAM:
    helper.play_webcam(confidence, model)

elif source_radio == settings.RTSP:
    helper.play_rtsp_stream(confidence, model)

elif source_radio == settings.YOUTUBE:
    helper.play_youtube_video(confidence, model)

else:
    st.error("Please select a valid source type!")
