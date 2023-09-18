import os
import glob
import yaml
from PIL import Image

def create_data_yaml(input_path, work_path, num_classes, classes):
    dict_file = {
        'train': os.path.join(input_path, 'train'),
        'val': os.path.join(input_path, 'valid'),
        'test': os.path.join(input_path, 'test'),
        'nc': num_classes,
        'names': classes
    }

    with open(os.path.join(work_path, 'data.yaml'), 'w+') as file:
        yaml.dump(dict_file, file)

def count_class_occurrences(input_path, num_classes, classes):
    class_idx = {str(i): classes[i] for i in range(num_classes)}
    class_stat = {}
    data_len = {}

    for mode in ['train', 'valid', 'test']:
        class_count = {classes[i]: 0 for i in range(num_classes)}
        path = os.path.join(input_path, mode, 'labels')

        for file in os.listdir(path):
            with open(os.path.join(path, file)) as f:
                lines = f.readlines()

                for cls in set([line[0] for line in lines]):
                    class_count[class_idx[cls]] += 1

        data_len[mode] = len(os.listdir(path))
        class_stat[mode] = class_count

    return class_stat, data_len

# to check image sizes, must ensure
def display_image_sizes(input_path, modes=['train', 'valid', 'test']):
    for mode in modes:
        print(f'\nImage sizes in {mode} set:\n')
        img_size = 0
        for file in glob.glob(os.path.join(input_path, mode, 'images', '*')):
            image = Image.open(file)
            if image.size != img_size:
                print(f'\t{image.size}')
                img_size = image.size

# to check each data set size
def display_set_sizes(input_path, modes=['train', 'valid', 'test']):
    for mode in modes:
        files = glob.glob(os.path.join(input_path, mode, 'images', '*'))
        print(f'{mode} set size: {len(files)}\n')
