from unet_model import *
from gen_patches import *

import os.path
import numpy as np
import tifffile as tiff
from keras.callbacks import CSVLogger
from keras.callbacks import TensorBoard
from keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau


def normalize(img):
    min = img.min()
    max = img.max()
    x = 2.0 * (img - min) / (max - min) - 1.0
    return x



N_BANDS = 4 
N_CLASSES = 8  # Brown - Bare Soil, Light green - Grass, Gray - Building, Purple - Swimming Pool, Dark Green - Trees, Black - Roads , Yellow - Railway Station and Blue - Water
CLA