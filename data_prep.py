import os
import glob
import yaml
from PIL import Image

def create_data_yaml(input_dir, work_dir, num_classes, classes):
    dict_file = {
        'train': os.path.join(input_dir, 'train'),
        'val': os.path.join(input_dir, 'valid'),
        'test': os.path.join(input_dir, 'test'),
        'nc': num_classes,
        'names': classes
    }

    with open(os.path.join(work_dir, 'data.yaml'), 'w+') as file:
        yaml.dump(dict_file, file)

def count_class_occurrences(input_dir, num_classes, classes):
    class_idx = {str(i): classes[i] for i in range(num_classes)}
    class_stat = {}
    data_len = {}

    for mode in ['train', 'valid', 'test']:
        class_count = {classes[i]: 0 for i in range(num_classes)}
        path = os.path.join(input_dir, mode, 'labels')

        for file in os.listdir(path):
            with open(os.path.join(path, file)) as f:
                lines = f.readlines()

                for cls in set([line[0] for line in lines]):
                    class_count[class_idx[cls]] += 1

        data_len[mode] = len(os.listdir(path))
        class_stat[mode] = class_count

    return class_stat, data_len

# to check image sizes, must ensure
def display_image_sizes(input_dir, modes=['train', 'valid', 'test']):
    for mode in modes:
        print(f'\nImage sizes in {mode} set:\n')
        img_size = 0
        for file in glob.glob(os.path.join(input_dir, mode, 'images', '*')):
            image = Image.open(file)
            if image.size != img_size:
                print(f'\t{image.size}')
                img_size = image.size

# to check each data set size
def display_set_sizes(input_dir, modes=['train', 'valid', 'test']):
    for mode in modes:
        files = glob.glob(os.path.join(input_dir, mode, 'images', '*'))
        print(f'{mode} set size: {len(files)}\n')
