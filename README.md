# Deep-Satellite-Image-Segmentation

A project for Satellite Image Segmentation using Deep Learning. Satellite images are an essential tool used by meteorologists. They offer a high resolution view of the earth from the sky. This project focuses on classifying eight classes, namely Water, Grass, Roads, Building, Trees, Swimming pool, Railway, and Bare Soil.

No previous experience in Deep Learning is required. Just follow the steps and you should be able to see it in action.

## Setup Instructions

1. Place your satellite images in the data/sat5band/ folder.
2. Run the scripts in the following order to train the model for all images:
   - `python3 edgeGen.py` - to generate edge data
   - `python3 water_mask_function.py` - to generate water data
   - `python3 Grass_mask_function.py` - to generate vegetation data
   - `python3 genpatches.py` - to generate patches for above generated data
   - `python3 train_unet.py` - begins the training of the UNET model
   - `python3 train_kvnet.py` - begins the training of the KV_Net
   - `python3 predict_kvnet.py` - Outputs will be stored in ./outputs/ of data/test/

## Required Libraries
  - cv2
  - tifffile
  - numpy
  - keras-gpu
  - tensorflow-gpu
  - glob

Alternatively, you can use preset weights saved [here](https://drive.google.com/file/d/10xldHiPczByAbWKMJ3Ov0uusbUY5Ve53/view?usp=sharing) and [here](https://drive.google.