import math
import numpy as np
import matplotlib.pyplot as plt
import tifffile as tiff
import cv2

from train_KVnet import weights_path, get_model, normalize, PATCH_SZ, N_CLASSES


def predict(x, model, patch_sz=160, n_classes=8):
    img_height = x.shape[0]
    img_width = x.shape[1]
    n_channels = x.shape[2]
    # make extended img so that it contains integer number of patches
    npatches_vertical = math.ceil(img_height / patch_sz)
    npatches_horizontal = math.ceil(img_width / patch_sz)
    extended_height = patch_sz * npatches_vertical
    extended_width = patch_sz * npatches_horizontal
    ext_x = np.zeros(shape=(extended_height, extended_width, n_channels), dtype=np.float32)
    # fill extended image with mirrors:
    ext_x[:img_height, :img_width, :] = x
    for i in range(img_height, extended_height):
        ext_x[i, :, :] = ext_x[2 * img_height - i - 1, :, :]
    for j in range(img_width, extended_width):
        ext_x[:, j, :] = ext_x[:, 2 * img_width - j - 1, :]

    # now we assemble all patches in one array
    patches_list = []
    for i in range(0, npatches_vertical):
        for j in range(0, npatches_horizontal):
            x0, x1 = i * patch_sz, (i + 1) * patch_sz
            y0, y1 = j * patch_sz, (j + 1) * patch_sz
            patches_list.append(ext_x[x0:x1, y0:y1, :])
    # model.predict() needs numpy array rather than a list
    patches_array = np.asarray(patches_list)
    # predictions:
    patches_predict = model.predict(patches_array, batch_size=4)
    prediction = np.zeros(shape=(extended_height, extended_width, n_classes), dtype=np.float32)
    print("starting of k")
    print(npatches_horizontal)
    i=0
    j=0
    for k in range(1,1+patches_predict.shape[0]):
        x0, x1 = (i) * patch_sz, (i+1) * patch_sz
        y0, y1 = (j) * patch_sz, (j+1) * patch_sz
        if (k % npatches_horizontal == 0 and k!=0):
            i+=1
            j=0
        else:
            j+=1
        prediction[x0:x1, y0:y1, :] = patches_predict[k-1, :, :, :]
    print("ending of k")
        
    return prediction[:img_height, :img_width, :]


def picture_from_mask(mask, threshold=0):
    colors = {
        0: [150, 80, 0],  # Brown - Bare Soil
        1: [0, 255, 0],  # Light green - Grass
        2: [100, 100, 100],    # Gray - Building
        3: [150, 150, 255],  # Purple - Swimming Pool
        4: [0, 125, 0],   # Dark Green - Trees
        5: [0, 0, 0],     # Black - Roads
        6: [255, 255, 0],  # Yellow - Railway Station
        7: [0, 0, 150]     # Blue - Water
    }
    z_order = {
        1: 0,
        2: 1,
        3: 2,
        4: 3,
        5: 4,
        6: 5,
        7: 6,
        8: 7
    }
    pict = 255*np.ones(shape=(3, mask.shape[1], mask.shape[2]), dtype=np.uint8)
    f