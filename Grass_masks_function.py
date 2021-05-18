import numpy as np
import argparse
import cv2
import matplotlib
import math
from matplotlib import pyplot as plt
import gdal

ds = gdal.Open("/Users/kunal/Desktop/sat_test/"+str(p)+".tif")
band1 = ds.GetRasterBand(1).ReadAsArray()    #Red
band2 = ds.GetRasterBand(2).ReadAsArray()    # Green 
band3 = ds.GetRasterBand(3).ReadAsArray()    #blue
band4 = ds.GetRasterBand(4).ReadAsArray()
band5 = np.zeros((band1.shape[0],band1.shape[1],3))
band5[:,:,0] = band4/np.max(band4)
band5[:,:,1] = band2/np.max(band2) - 