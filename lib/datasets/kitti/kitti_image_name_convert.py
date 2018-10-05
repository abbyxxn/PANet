import argparse
import os
import glob
import numpy as np
import shutil

def parse_args():
    """Parse input arguments"""
    parser = argparse.ArgumentParser(description='convert kitti image name to end with leftImg8bit.png')

    parser.add_argument(
        '--input_dir', dest='input_dir',required=True,
        help='Input dir for kitti data set include labelsIds and instancesIds')

    return parser.parse_args()

def main():
    args = parse_args()
    print('Called with args:')
    print(args)

    image_path = glob.glob(os.path.join(args.input_dir, '*.png'))
    images = [im.split('/')[6] for im in image_path]
    images = [im.split('.')[0] for im in images]

    for i, j in enumerate(image_path):
        os.rename(j, args.input_dir + 'kitti_' + images[i] + '_leftImg8bit.png')



if __name__ == '__main__':
    main()