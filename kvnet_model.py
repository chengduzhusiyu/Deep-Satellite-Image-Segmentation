# u-net model with up-convolution or up-sampling and weighted binary-crossentropy as loss func

from keras.models import Model
from keras.layers import Input, Conv2D, MaxPooling2D, UpSampling2D, concatenate, Conv2DTranspose, BatchNormalization, Dropout
from keras.optimizers import Adam
from keras.utils import plot_model
from keras import backend as K


def unet_model(n_classes=8, im_sz=160, n_channels=4, n_filters_start=32, growth_factor=2, upconv=True,
           