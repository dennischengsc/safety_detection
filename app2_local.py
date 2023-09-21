import requests
import os
import streamlit as st
from PIL import Image
from io import BytesIO

# Ensure the output directory exists
output_directory = 'output_image'
os.makedirs(output_directory, exist_ok=True)

# The URL of the FastAPI endpoint
url = 'https://safetydetection-d6yophmzga-ew.a.run.app/detect_image/'

# Prepare the image file
files = {'image_upload': ('image_demo_01.jpg', open('reference_image/image_demo_01.jpg', 'rb'), 'image/jpeg')}

try:
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
        print(f"Error: {response.status_code}")
        print(response.text)
except Exception as e:
    # Handle other exceptions, e.g., connection errors
    print(f"Exception: {str(e)}")
