from ultralytics import YOLO
import os

def train_yolo_model(work_path, num_classes, img_size=640, epochs=1, batch=64):
    model = YOLO(os.path.join(work_path, 'yolov8n.pt'))
    model.train(
        data=os.path.join(work_path, 'data.yaml'),
        task='detect',
        imgsz=img_size,
        epochs=epochs,
        batch=batch,
        mode='train',
        name='yolov8n_training_result'
    )
