from pathlib import Path
import sys

# Get the absolute path of the current file
file_path = Path(__file__).resolve()

# Get the parent directory of the current file
root_path = file_path.parent

# Add the root path to the sys.path list if it is not already there
if root_path not in sys.path:
    sys.path.append(str(root_path))

# Get the relative path of the root directory with respect to the current working directory
ROOT = root_path.relative_to(Path.cwd())
print(ROOT)

# Select Sources
IMAGE = 'Image'
# VIDEO = 'Video'
WEBCAM = 'Webcam'
YOUTUBE = 'YouTube'

SOURCES_LIST = [IMAGE, WEBCAM, YOUTUBE]
# SOURCES_LIST = [IMAGE, VIDEO, WEBCAM, YOUTUBE]
# Images config
IMAGES_DIR = ROOT
DEFAULT_IMAGE = IMAGES_DIR / 'reference_image/image_01.jpg'
DEFAULT_DETECT_IMAGE = IMAGES_DIR / 'prediction//predict/image_01.jpg'

# Videos config
# VIDEO_DIR = ROOT / 'videos'
# VIDEO_1_PATH = VIDEO_DIR / 'video_01.mp4'
# VIDEO_2_PATH = VIDEO_DIR / 'video_02.mp4'
# VIDEO_3_PATH = VIDEO_DIR / 'video_03.mp4'
# VIDEO_4_PATH = VIDEO_DIR / 'video_04.mp4'
# VIDEOS_DICT = {
#     'video_1': VIDEO_1_PATH,
#     'video_2': VIDEO_2_PATH,
#     'video_3': VIDEO_3_PATH,
#     'video_4': VIDEO_4_PATH,
# }

# ML Model config
MODEL_DIR = ROOT
DETECTION_MODEL = MODEL_DIR / 'best.pt'
print(DETECTION_MODEL)
# SEGMENTATION_MODEL = MODEL_DIR / 'yolov8n-seg.pt'

# Webcam
WEBCAM_PATH = 0
