from pathlib import Path
import PIL
import streamlit as st
# Local Modules
import settings
import requests
import os
from PIL import Image
from io import BytesIO



url = 'https://safetydetection2-mity3tdx3q-ew.a.run.app/detect_image/'

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
st.sidebar.header("Model Configuration")

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

# Initialize model_path to None
model_path = None

# Selecting Detection Or Live Prediction
if model_type == 'Detection':
    model_path = Path(settings.DETECTION_MODEL)

# Ensure the output directory exists
output_directory = 'output_image'
os.makedirs(output_directory, exist_ok=True)


def process_uploaded_image(uploaded_image, selected_class, conf_threshold):
    if uploaded_image is not None:
            try:
                # Convert the uploaded image to bytes
                uploaded_image_bytes = BytesIO(uploaded_image.read())

                # Prepare the image file to send to the API
                files = {'image_upload': ('uploaded_image.jpg', uploaded_image_bytes, 'image/jpeg')}

                # Send a POST request to the API with class selection and confidence threshold
                payload = {
                    'selected_class': selected_class,
                    'conf': conf_threshold
                }
                response = requests.post(url, files=files, data=payload)

                # Check the response status code
                if response.status_code == 200:
                    # The request was successful, and you can save the received image
                    output_file_path = os.path.join(output_directory, 'output.jpg')
                    with open(output_file_path, 'wb') as output_file:
                        output_file.write(response.content)
                    st.image(output_file_path, caption='Received Image', use_column_width=True)
                    st.success("Image processed successfully.")
                    print(f"Image received and saved to {output_file_path}")
                else:
                    # Handle errors or exceptions here
                    st.error(f"Error: {response.status_code}")
                    st.text(response.text)
            except Exception as e:
                # Handle other exceptions, e.g., connection errors
                st.error(f"Exception: {str(e)}")

source_img = None

# If image is selected
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
            selected_class_strings = ','.join(map(str, selected_class_numbers))
            process_uploaded_image(source_img, selected_class_strings, confidence)
