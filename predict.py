
import math
import numpy as np
import matplotlib.pyplot as plt
import tifffile as tiff


from train_unet import get_model, normalize, PATCH_SZ, N_CLASSES 


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
        1: 2,
        2: 7,
        3: 5,
        4: 6,
        5: 1,
        6: 0,
        7: 4,
        8: 3
    }
    pict = 255*np.ones(shape=(3, mask.shape[1], mask.shape[2]), dtype=np.uint8)
    for i in range(1, 9):
        cl = z_order[i]
        for ch in range(3):
            pict[ch,:,:][mask[cl,:,:] > threshold] = colors[cl][ch]
    return pict


if __name__ == '__main__':
    model = get_model()
    weights_path = "weights/unet_weights_30_50ep.hdf5"
    model.load_weights(weights_path)
    for i in range(1,15):
        test_id = str(i)
        print('Predicting for data/test/{}.tif'.format(test_id))
        img = normalize(tiff.imread('data/test/{}.tif'.format(test_id)))
        print(img.shape)
    
        for i in range(7):
            if i == 0:  # reverse first dimension
                mymat = predict(img[::-1,:,:], model, patch_sz=PATCH_SZ, n_classes=N_CLASSES).transpose([2,0,1])
                #print(mymat[0][0][0], mymat[3][12][13])
                # print("Case 1",img.shape, mymat.shape)
            elif i == 1:    # reverse second dimension
                temp = predict(img[:,::-1,:], model, patch_sz=PATCH_SZ, n_classes=N_CLASSES).transpose([2,0,1])
                #print(temp[0][0][0], temp[3][12][13])
                print("Case 2", temp.shape, mymat.shape)
                mymat = np.mean( np.array([ temp[:,::-1,:], mymat ]), axis=0 )
            elif i == 2:    # transpose(interchange) first and second dimensions
                temp = predict(img.transpose([1,0,2]), model, patch_sz=PATCH_SZ, n_classes=N_CLASSES).transpose([2,0,1])
                #print(temp[0][0][0], temp[3][12][13])
                print("Case 3", temp.shape, mymat.shape)
                mymat = np.mean( np.array([ temp.transpose(0,2,1), mymat ]), axis=0 )
            elif i == 3:
                temp = predict(np.rot90(img, 1), model, patch_sz=PATCH_SZ, n_classes=N_CLASSES)
                #print(temp.transpose([2,0,1])[0][0][0], temp.transpose([2,0,1])[3][12][13])
                # print("Case 4", temp.shape, mymat.shape)
                mymat = np.mean( np.array([ np.rot90(temp, -1).transpose([2,0,1]), mymat ]), axis=0 )
            elif i == 4:
                temp = predict(np.rot90(img,2), model, patch_sz=PATCH_SZ, n_classes=N_CLASSES)
                #print(temp.transpose([2,0,1])[0][0][0], temp.transpose([2,0,1])[3][12][13])
                # print("Case 5", temp.shape, mymat.shape)
                mymat = np.mean( np.array([ np.rot90(temp,-2).transpose([2,0,1]), mymat ]), axis=0 )
            elif i == 5:
                temp = predict(np.rot90(img,3), model, patch_sz=PATCH_SZ, n_classes=N_CLASSES)
                #print(temp.transpose([2,0,1])[0][0][0], temp.transpose([2,0,1])[3][12][13])
                # print("Case 6", temp.shape, mymat.shape)
                mymat = np.mean( np.array([ np.rot90(temp, -3).transpose(2,0,1), mymat ]), axis=0 )
            else:
                temp = predict(img, model, patch_sz=PATCH_SZ, n_classes=N_CLASSES).transpose([2,0,1])
                #print(temp[0][0][0], temp[3][12][13])
                # print("Case 7", temp.shape, mymat.shape)
                mymat = np.mean( np.array([ temp, mymat ]), axis=0 )
    
        #print(mymat[0][0][0], mymat[3][12][13])
        map = picture_from_mask(mymat, 0.5)
        #mask = predict(img, model, patch_sz=PATCH_SZ, n_classes=N_CLASSES).transpose([2,0,1])  # make channels first
        #map = picture_from_mask(mask, 0.5)
    
        #tiff.imsave('result.tif', (255*mask).astype('uint8'))
        tiff.imsave('data/testout/res{}.tif'.format(test_id), (255*mymat).astype('uint8'))
        tiff.imsave('data/testout/map{}.tif'.format(test_id), map)
    