import math
import numpy as np
import matplotlib.pyplot as plt
import tifffile as tiff
import cv2

from train_KVnet import weights_path, get_model, normalize, PATCH_SZ, N_CLASSES


def predict(x, model, patch_sz=160, n_classes=8):
    img_height = x.shape[0]
    img_w