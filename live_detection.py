# import cv2

# # Open a connection to the default camera (usually 0 or 1 for built-in webcams)
# cap = cv2.VideoCapture(0)

# while True:
#     # Read a frame from the webcam
#     ret, frame = cap.read()

#     if not ret:
#         break

#     # Display the frame in a window
#     cv2.imshow('Webcam Feed', frame)

#     # Break the loop if 'q' is pressed
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break


import cv2

# Loop through camera indices until no more cameras are found
index = 0
while True:
    # Try to open the camera at the current index
    cap = cv2.VideoCapture(index)

    # Check if the camera was successfully opened
    if not cap.isOpened():
        break

    # Get information about the camera
    camera_info = f"Camera {index}: {cap.get(cv2.CAP_PROP_FRAME_WIDTH)}x{cap.get(cv2.CAP_PROP_FRAME_HEIGHT)}"

    # Print the camera information
    print(camera_info)

    # Release the camera
    cap.release()

    # Increment the index to check the next camera
    index += 1
