import argparse
import os
import glob
import numpy as np
import shutil

def parse_args():
    """Parse input arguments"""
    parser = argparse.ArgumentParser(description='Split cityscapes_like kitti dataset to training set and validation set in user-defined proportion')

    parser.add_argument(
        '--input_dir', dest='input_dir',required=True,
        help='Input dir for kitti data set include labelsIds and instancesIds')

    parser.add_argument(
        '--output_dir', dest='output_dir',required=True,
        help='Output dir for training set and validation set')

    parser.add_argument(
        '--split_ratio', dest='sr', required=True,
        help='fraction of data used for training')

    return parser.parse_args()

def main():
    args = parse_args()
    print('Called with args:')
    print(args)

    image_path = glob.glob(os.path.join(args.input_dir, '*instanceIds.png'))
    images = [im.split('_')[2] for im in image_path]

    np.random.seed()
    np.random.shuffle(images)
    train_count = (len(images) * int(args.sr)) // 100
    train = images[:train_count]
    val = images[train_count:]

    output_path_name = []
    output_path_name.append(os.path.join(args.output_dir, 'train/kitti'))
    output_path_name.append(os.path.join(args.output_dir, 'val/kitti'))
    for i in output_path_name:
        os.makedirs(i)

    data_ind = [train, val]
    for k, indexset in enumerate(data_ind):
        instanceIds_path = []
        labelIds_path = []
        for ind in indexset:
            instanceIds_path.append(glob.glob(os.path.join(args.input_dir, '*' + ind + '*instanceIds.png')))
            labelIds_path.append(glob.glob(os.path.join(args.input_dir, '*' + ind + '*labelIds.png')))

        for i in instanceIds_path:
            shutil.copy(i[0], output_path_name[k])
        for i in labelIds_path:
            shutil.copy(i[0], output_path_name[k])


if __name__ == '__main__':
    main()