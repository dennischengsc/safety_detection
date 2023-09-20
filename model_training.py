from ultralytics import YOLO
import os

def train_yolo_model(LOCAL_WORK_PATH, img_size=640, epochs=1, batch=32, save_period=10):
    model = YOLO(os.path.join(LOCAL_WORK_PATH, 'yolov8n.pt'))
    model.train(
        data=os.path.join(LOCAL_WORK_PATH, 'data.yaml'),
        task='detect',
        imgsz=img_size,
        epochs=epochs,
        batch=batch,
        mode='train',
        name='yolov8n_train_result',
        save_period=save_period,
        resume=False
    )
