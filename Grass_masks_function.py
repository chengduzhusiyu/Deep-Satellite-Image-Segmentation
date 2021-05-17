import numpy as np
import argparse
import cv2
import matplotlib
import math
from matplotlib import pyplot as plt
import gdal

ds = gdal.Open("/Users/kunal/Desktop/sat_test/"+str(p)+".tif")
band1 = ds.GetRasterBan