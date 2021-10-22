
from kvnet_model import *
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



N_BANDS = 8
N_CLASSES = 8  # buildings(grey), roads(black), grass(light green), trees(dark green), bare soil(brown),swimming pool(purple),railway station(yellow) and blue (water)
# CLASS_WEIGHTS = [0.2, 0.2, 0.2, 0.2, 0.5, 0.7, 0.4, 0.15]     # 0.7 and 0.6
# CLASS_WEIGHTS = [0.1, 0.1, 0.1, 0.4, 0.4, 0.7, 0.55, 0.15]  # 50+30 -- tatti -- 0.0900 training error and validation error = 1.3 to 0.5
CLASS_WEIGHTS = 0.9-np.array([0.1, 0.1, 0.2, 0.2, 0.3, 0.7, 0.4, 0.15] )
# CLASS_WEIGHTS = [0.1, 0.1, 0.1, 0.1, 0.7, 0.7, 0.4, 0.15]  # 30  -- good -- 0.14 -- None

N_EPOCHS = 30
UPCONV = True
PATCH_SZ = 160   # should divide by 16
BATCH_SIZE = 15
TRAIN_SZ = int(2500/10)  # train size
VAL_SZ = int(500/10)    # validation size


def get_model():
    return unet_model(N_CLASSES, PATCH_SZ, n_channels=N_BANDS, upconv=UPCONV, class_weights=CLASS_WEIGHTS)