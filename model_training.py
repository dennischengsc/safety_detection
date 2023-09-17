from ultralytics import YOLO
import os

def train_yolo_model(work_dir, num_classes, img_size=640, epochs=200, batch=32, save_period=10):
    model = YOLO(os.path.join(work_dir, 'yolov8n.pt'))
    model.train(
        data=os.path.join(work_dir, 'data.yaml'),
        task='detect',
        imgsz=img_size,
        epochs=epochs,
        batch=batch,
        mode='train',
        name='yolov8n_change_path_test',
        resume=False,
        save_period=save_period
    )
