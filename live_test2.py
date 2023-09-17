import cv2
import matplotlib.pyplot as plt
from ultralytics import YOLO
from ultralytics.models.yolo.detect.predict import DetectionPredictor
from pydub import AudioSegment
from pydub.playback import play

model = YOLO('best.pt')

# Open the camera
camera = cv2.VideoCapture(0)
img_counter = 0


ret, frame = camera.read()

print(frame[1])


# if not ret:
#     print("Failed to grab frame")
#     break

# # Perform object detection using your YOLO model
# results = model.predict(frame)

# # Process the detection results and draw bounding boxes
# for pred in results.pred[0]:
#     class_id = int(pred[5])
#     class_name = model.names[class_id]
#     confidence = pred[4]

#     if confidence > 0.5:  # You can adjust the confidence threshold
#         x, y, w, h = map(int, pred[:4] * frame.shape[1])  # Scale to frame size
#         cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
#         cv2.putText(frame, f"{class_name}: {confidence:.2f}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

# # Display the frame with detection results
# cv2.imshow("Camera Feed with Detection", frame)

# # Check for key presses
# k = cv2.waitKey(1)
# if k % 256 == 27:
#     # ESC pressed
#     print("Escape hit, closing...")
#     break

# # Save the frame with detections when SPACE is pressed
# elif k % 256 == 32:
#     img_path = "path/opencv_frame_{}.png".format(img_counter)
#     cv2.imwrite(img_path, frame)
#     img_counter += 1

# # Release the camera and close OpenCV windows
# camera.release()
# cv2.destroyAllWindows()
