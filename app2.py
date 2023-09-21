import streamlit as st
import requests
import os
from PIL import Image
from io import BytesIO

# Ensure the output directory exists
output_directory = 'output_image'
os.makedirs(output_directory, exist_ok=True)

# The URL of the FastAPI endpoint
url = 'https://safetydetection-d6yophmzga-ew.a.run.app/detect_image/'

# Function to process and display the uploaded image
def process_uploaded_image(uploaded_image):
    if uploaded_image is not None:
        try:
            # Convert the uploaded image to bytes
            uploaded_image_bytes = BytesIO(uploaded_image.read())

            # Prepare the image file to send to the API
            files = {'image_upload': ('uploaded_image.jpg', uploaded_image_bytes, 'image/jpeg')}

            # Send a POST request to the API
            response = requests.post(url, files=files)

            # Check the response status code
            if response.status_code == 200:
                # The request was successful, and you can save the received image
                output_file_path = os.path.join(output_directory, 'output.jpg')
                with open(output_file_path, 'wb') as output_file:
                    output_file.write(response.content)
                st.image(output_file_path, caption='Received Image', use_column_width=True)
                print(f"Image received and saved to {output_file_path}")
            else:
                # Handle errors or exceptions here
                st.error(f"Error: {response.status_code}")
                st.text(response.text)
        except Exception as e:
            # Handle other exceptions, e.g., connection errors
            st.error(f"Exception: {str(e)}")

# Streamlit UI
st.title("Image Upload and Display")
st.sidebar.header("Upload an Image")
source_img = st.sidebar.file_uploader("Choose an image...", type=("jpg", "jpeg", "png", 'bmp', 'webp'))
if st.sidebar.button("Process Image"):
    process_uploaded_image(source_img)
