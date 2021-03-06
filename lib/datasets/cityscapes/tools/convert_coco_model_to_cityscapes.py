# Convert a detection model trained for COCO into a model that can be fine-tuned
# on cityscapes
#
# cityscapes_to_coco

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from six.moves import cPickle as pickle
import argparse
import os
import sys
import numpy as np
import torch

import datasets.cityscapes.coco_to_cityscapes_id as cs

NUM_CS_CLS = 9
NUM_COCO_CLS = 81


def parse_args():
    parser = argparse.ArgumentParser(
        description='Convert a COCO pre-trained model for use with Cityscapes')
    parser.add_argument(
        '--coco_model', dest='coco_model_file_name',
        help='Pretrained network weights file path',
        default=None, type=str)
    parser.add_argument(
        '--convert_func', dest='convert_func',
        help='Blob conversion function',
        default='cityscapes_to_coco', type=str)
    parser.add_argument(
        '--output', dest='out_file_name',
        help='Output file path',
        default=None, type=str)

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()
    return args


def convert_coco_blobs_to_cityscape_blobs(model_dict):
    for (k, v), i in zip(model_dict['model'].items(), range(len(model_dict['model']))):
        print(i)
        if v.shape[0] == NUM_COCO_CLS or v.shape[0] == 4 * NUM_COCO_CLS:
            coco_blob = model_dict['model'][k]
            print(
                'Converting COCO blob {} with shape {}'.
                format(k, coco_blob.shape)
            )
            cs_blob = convert_coco_blob_to_cityscapes_blob(
                coco_blob, args.convert_func, k
            )
            print(' -> converted shape {}'.format(cs_blob.shape))
            model_dict['model'][k] = cs_blob


def convert_coco_blob_to_cityscapes_blob(coco_blob, convert_func, k):
    # coco blob (81, ...) or (81*4, ...)
    coco_shape = coco_blob.shape
    leading_factor = int(coco_shape[0] / NUM_COCO_CLS)
    tail_shape = list(coco_shape[1:])
    assert leading_factor == 1 or leading_factor == 4

    # Reshape in [num_classes, ...] form for easier manipulations
    coco_blob = coco_blob.reshape([NUM_COCO_CLS, -1] + tail_shape)
    # Default initialization uses Gaussian with mean and std to match the
    # existing parameters
    #std = coco_blob.std()
    #mean = coco_blob.mean()
    cs_shape = [NUM_CS_CLS] + list(coco_blob.shape[1:])
    #cs_blob = (np.random.randn(*cs_shape) * std + mean).astype(np.float32)
    cs_blob = np.random.randn(*cs_shape).astype(np.float32)
    for key, v in panet_weight.items():
        if k == key:
            v = v.reshape(cs_shape)
            cs_blob = v
            break


    # Replace random parameters with COCO parameters if class mapping exists
    for i in range(NUM_CS_CLS):
        coco_cls_id = getattr(cs, convert_func)(i)
        if coco_cls_id >= 0:  # otherwise ignore (rand init)
            cs_blob[i] = coco_blob[coco_cls_id]

    cs_shape = [NUM_CS_CLS * leading_factor] + tail_shape
    return cs_blob.reshape(cs_shape)


def remove_momentum(model_dict):
    model_dict['optimizer'].pop('state')


def load_and_convert_coco_model(args):
    # with open(args.coco_model_file_name, 'r') as f:
    #     model_dict = pickle.load(f)
    model_dict = torch.load(args.coco_model_file_name)
    remove_momentum(model_dict)
    convert_coco_blobs_to_cityscape_blobs(model_dict)
    print('blobs converted.')
    return model_dict


if __name__ == '__main__':
    args = parse_args()
    print(args)
    assert os.path.exists(args.coco_model_file_name), \
        'Weights file does not exist'
    panet_weight = torch.load('/home/abby/Repositories/PANet/data/panet_weight_state_dict')
    Key = 'string'
    weights = load_and_convert_coco_model(args)
    torch.save(weights, '/home/abby/Repositories/PANet/data/pretrained_model/coco_pretrained_weight_convert_for_cityscapes.pth')


    #with open(args.out_file_name, 'w') as f:
     #   torch.save(weights, f)
    print('Wrote blobs to {}:'.format(args.out_file_name))
    print(sorted(weights['blobs'].keys()))
