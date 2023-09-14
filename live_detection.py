import cv2

# Open a connection to the default camera (usually 0 or 1 for built-in webcams)
cap = cv2.VideoCapture(1)

while True:
    # Read a frame from the webcam
    ret, frame = cap.read()

    if not ret:
        break

    # Display the frame in a window
    cv2.imshow('Webcam Feed', frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
