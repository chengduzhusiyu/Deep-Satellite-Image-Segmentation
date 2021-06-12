import random
import numpy as np

def get_rand_patch(img, mask, sz=160):
    """
    :param img: ndarray with shape (x_sz, y_sz, num_channels)
    :param mask: binary ndarray with shape (x_sz, y_sz, num_classes)
    :param sz: size of random patch
    :return: patch with shape (sz, sz, num_channels)
    """
    try:
        assert len(img.shape) == 3 and img.shape[0] > sz and img.shape[1] > sz and img.shape[0