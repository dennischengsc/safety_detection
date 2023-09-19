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
model_type = st.sidebar.radio("Select Task", ['Detection'])

confidence = float(st.sidebar.slider(
    "Select Model Confidence", 25, 100, 40)) / 100

class_names = {
    0: 'Hardhat',
    1: 'Mask',
    2: 'NO-Hardhat',
    3: 'NO-Mask',
    4: 'NO-Safety Vest',
    5: 'Person',
    7: 'Safety Vest'
}

# Add a multi-select widget for class selection in the sidebar
selected_classes = st.sidebar.multiselect("Select Classes for Prediction", list(class_names.values()))
st.write(f"Selected Classes: {selected_classes}")

# Selecting Detection Or Segmentation
if model_type == 'Detection':
    model_path = Path(settings.DETECTION_MODEL)

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
                selected_class_numbers = [class_number for class_number, class_name in class_names.items() if class_name in selected_classes]
                res = model.predict(uploaded_image,
                                    conf=confidence,
                                    classes=selected_class_numbers
                                    )
                # st.write(res)
                boxes = res[0].boxes

                res_plotted = res[0].plot()[:, :, ::-1]
                st.image(res_plotted, caption='Detected Image',
                         use_column_width=True)
                # Initialize a counter for class 5 object
                class_5_count = 0

                try:
                    with st.expander("Detection Results"):
                        for box in boxes:
                            # # Print detected class IDs for debugging
                            # detected_class_ids = [int(box.data[0][-1]) for box in boxes]
                            # st.write(f"Detected Class IDs: {detected_class_ids}")

                            # Extract class IDs
                            class_ids = box.data[:, -1]
                            if 5 in class_ids:
                                class_5_count += 1

                            st.write(box.data)

                        # Display the total count of class 5 objects
                    st.write(f"Counter of Person is : {class_5_count}")

                except Exception as ex:
                    st.write("No image is uploaded yet!")




elif source_radio == settings.VIDEO:
    selected_class_numbers = [class_number for class_number, class_name in class_names.items() if class_name in selected_classes]
    helper.play_stored_video(confidence, model, selected_class_numbers)


elif source_radio == settings.WEBCAM:
    selected_class_numbers = [class_number for class_number, class_name in class_names.items() if class_name in selected_classes]
    helper.play_webcam(confidence, model, selected_class_numbers)

elif source_radio == settings.YOUTUBE:
    selected_class_numbers = [class_number for class_number, class_name in class_names.items() if class_name in selected_classes]
    helper.play_youtube_video(confidence, model, selected_class_numbers)

else:
    st.error("Please select a valid source type!")
