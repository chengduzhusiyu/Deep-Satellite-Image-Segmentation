import numpy as np
import argparse
import cv2
import matplotlib
import math
from matplotlib import pyplot as plt
import gdal



ds = gdal.Open("sat_test/"+str("name")+".tif")
band1 = ds.GetRasterBand(1).ReadAsArray()    #Red
band2 = ds.GetRasterBand(2).ReadAsArray()    #Green 
band3 = ds.GetRasterBand(3).ReadAsArray()   