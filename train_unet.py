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
CLASS_WEIGHTS = [0.1, 0.1, 0.1, 0.4, 0.4, 0.7, 0.55, 0.15]  # 50+30 -- tatti -- 0.0900 training error and validation error = 1.3 to 0.5
# CLASS_WEIGHTS = [ 6.49350649 , 0.87642419 , 0.275558  , 10 ,  0.70921986  ,0.39651071 , 6.02409639 , 1.05374078]   # not tried but have a positive feeling about these weights
# CLASS_WEIGHTS = [ 0.11619276 , 0.01575265 , 0.0049555 , 0.71596023, 0.012749